# -*- coding: utf-8 -*-
# /***************************************************************************
# Irmt
#                                 A QGIS plugin
# OpenQuake Integrated Risk Modelling Toolkit
#                              -------------------
#        begin                : 2013-10-24
#        copyright            : (C) 2020 by GEM Foundation
#        email                : devops@openquake.org
# ***************************************************************************/
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.

import copy
import json
import numpy as np
from qgis.core import (
    QgsFeature, QgsGeometry, edit, QgsProject, QgsVectorLayer, QgsPointXY)
from svir.utilities.utils import (
    log_msg, WaitCursorManager, extract_npz, get_irmt_version,
    write_metadata_to_layer)
from svir.dialogs.load_output_as_layer_dialog import LoadOutputAsLayerDialog


class LoadDisaggAsLayerDialog(LoadOutputAsLayerDialog):
    """
    Dialog to load disaggregation from an oq-engine output, as layer
    """

    def __init__(self, drive_engine_dlg, iface, viewer_dock, session, hostname,
                 calc_id, output_type='disagg', path=None, mode=None,
                 engine_version=None, calculation_mode=None):
        assert output_type == 'disagg'
        LoadOutputAsLayerDialog.__init__(
            self, drive_engine_dlg, iface, viewer_dock, session, hostname,
            calc_id, output_type=output_type, path=path, mode=mode,
            engine_version=engine_version, calculation_mode=calculation_mode)
        # self.setWindowTitle('Load disaggregation as layer')
        # self.populate_out_dep_widgets()
        # self.adjustSize()
        self.ok_button.setEnabled(True)
        self.accept()

    def accept(self):
        with WaitCursorManager(
                'Extracting disagg_layer...',
                message_bar=self.iface.messageBar()):
            log_msg('Extracting disagg_layer', level='I',
                    print_to_stdout=True)
            disagg = extract_npz(
                self.session, self.hostname, self.calc_id,
                'disagg_layer',
                message_bar=self.iface.messageBar())
        if disagg is None:
            return
        with WaitCursorManager(
                'Creating disaggregation layer',
                self.iface.messageBar()):
            log_msg('Creating disagg_layer', level='I',
                    print_to_stdout=True)
            self.build_layer(disagg)
            self.style_curves()

    def get_field_types(self, disagg_array):
        # field_types = {name: disagg['array'][name].dtype.char
        #                for name in disagg['array'].dtype.names}
        field_types = {}
        for field_name in disagg_array.dtype.names:
            field_type = disagg_array[field_name].dtype.char
            # FIXME: lists of floats are declared as 'f', but we need to store
            # them as strings
            if field_type == 'f' and field_name not in ('lon', 'lat'):
                field_type = 'S'
            field_types[field_name] = field_type
        return field_types

    def build_layer(self, disagg):
        log_msg('Getting disagg array', level='I', print_to_stdout=True)
        disagg_array = disagg['array']
        log_msg('Done getting disagg array', level='I', print_to_stdout=True)
        layer_name = '%s_%s' % (self.output_type, self.calc_id)
        # log_msg('Getting field types', level='I', print_to_stdout=True)
        field_types = self.get_field_types(disagg_array)
        self.layer = QgsVectorLayer(
            "%s?crs=epsg:4326" % 'point', layer_name, "memory")
        modified_field_types = copy.copy(field_types)
        for field_name, field_type in field_types.items():
            if field_name in ['lon', 'lat']:
                continue
            # log_msg('Adding field %s of type %s' % (field_name, field_type),
            #         level='I', print_to_stdout=True)
            added_field_name = self.add_field_to_layer(field_name, field_type)
            # log_msg('\tDone adding field', level='I', print_to_stdout=True)
            if field_name != added_field_name:
                # replace field_name with the actual added_field_name
                del modified_field_types[field_name]
                modified_field_types[added_field_name] = field_type
        field_types = copy.copy(modified_field_types)

        self.read_npz_into_layer(field_types, disagg_array)
        self.layer.setCustomProperty('output_type', self.output_type)
        if self.engine_version is not None:
            self.layer.setCustomProperty('engine_version', self.engine_version)
        irmt_version = get_irmt_version()
        self.layer.setCustomProperty('irmt_version', irmt_version)
        self.layer.setCustomProperty('calc_id', self.calc_id)
        self.layer.setCustomProperty(
            'investigation_time', self.oqparam['investigation_time'])
        disagg_params = {}
        for k, v in disagg.items():
            if k == 'array':
                continue
            v = [value.item().decode('utf8')
                 if isinstance(value.item(), bytes)
                 else value.item()
                 for value in v]
            self.layer.setCustomProperty(k, v)
            disagg_params[k] = v
        write_metadata_to_layer(
            self.drive_engine_dlg, self.output_type, self.layer,
            disagg_params=disagg_params)
        QgsProject.instance().addMapLayer(self.layer, False)
        tree_node = QgsProject.instance().layerTreeRoot()
        tree_node.insertLayer(0, self.layer)
        self.iface.setActiveLayer(self.layer)
        log_msg('Layer %s was created successfully' % layer_name, level='S',
                message_bar=self.iface.messageBar(),
                print_to_stdout=True)

    def read_npz_into_layer(self, field_types, disagg_array):
        with edit(self.layer):
            lons = disagg_array['lon']
            lats = disagg_array['lat']
            feats = []
            # tot_feats = len(disagg_array)
            for row_idx, row in enumerate(disagg_array):
                # log_msg('Site %s of %s' % (row_idx, tot_feats), level='I',
                #         print_to_stdout=True)
                feat = QgsFeature(self.layer.fields())
                for field_name_idx, field_name in enumerate(field_types):
                    if field_name in ('lon', 'lat'):
                        continue
                    if isinstance(disagg_array[field_name][row_idx],
                                  np.ndarray):
                        value = disagg_array[field_name][row_idx]
                        # log_msg('\t\tDumping json', level='I',
                        #         print_to_stdout=True)
                        if np.any(value < 0):
                            log_msg('Negative values were found for field %s:'
                                    ' %s' % (field_name, value),
                                    level='I', print_to_stdout=True)
                        value = json.dumps(value.tolist())
                        # log_msg('\t\tDone dumping json', level='I',
                        #         print_to_stdout=True)
                    else:  # scalar
                        value = disagg_array[field_name][row_idx].item()
                    feat.setAttribute(field_name, value)
                feat.setGeometry(QgsGeometry.fromPointXY(
                    QgsPointXY(lons[row_idx], lats[row_idx])))
                feats.append(feat)
                # log_msg('\tAdding feature', level='I',
                #         print_to_stdout=True)
                # added_ok = self.layer.addFeature(feat)
                # log_msg('\t\tDone adding feature', level='I',
                #         print_to_stdout=True)
                # if not added_ok:
                #     msg = 'There was a problem adding features to the layer.'
                #     log_msg(msg, level='C',
                #             message_bar=self.iface.messageBar(),
                #             print_to_stderr=True)
            added_ok = self.layer.addFeatures(feats)
            if not added_ok:
                msg = 'There was a problem adding features to the layer.'
                log_msg(msg, level='C', message_bar=self.iface.messageBar())
