# -*- coding: utf-8 -*-
# /***************************************************************************
# Irmt
#                                 A QGIS plugin
# OpenQuake Integrated Risk Modelling Toolkit
#                              -------------------
#        begin                : 2013-10-24
#        copyright            : (C) 2019 by GEM Foundation
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

# import os
# import tempfile
import zipfile
import json
import os
import configparser
from qgis.core import (
    QgsProject, QgsSymbol, QgsMarkerSymbol, QgsGradientColorRamp, QgsStyle,
    QgsGraduatedSymbolRenderer, NULL, QgsExpression, QgsRendererCategory,
    QgsCategorizedSymbolRenderer, QgsSingleSymbolRenderer)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QDialogButtonBox, QGroupBox, QCheckBox)
from svir.utilities.utils import import_layer_from_csv, log_msg, get_style
from svir.utilities.shared import (RAMP_EXTREME_COLORS,)


class LoadInputsDialog(QDialog):
    """
    Dialog to browse zipped input files
    """
    def __init__(self, zip_filepath, iface, parent=None):
        super().__init__(parent)
        self.zip_filepath = zip_filepath
        self.iface = iface
        ini_str = self.get_ini_str(self.zip_filepath)
        self.multi_peril_csv_dict = self.get_multi_peril_csv_dict(ini_str)
        self.setWindowTitle('Load peril data from csv')
        self.peril_gbx = QGroupBox('Peril')
        self.peril_vlayout = QVBoxLayout()
        self.peril_gbx.setLayout(self.peril_vlayout)
        for peril in self.multi_peril_csv_dict.keys():
            chk = QCheckBox(peril)
            chk.setChecked(True)
            self.peril_vlayout.addWidget(chk)
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.ok_button = self.button_box.button(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.peril_gbx)
        vlayout.addWidget(self.button_box)
        self.setLayout(vlayout)

    @staticmethod
    def get_ini_str(filepath):
        zfile = zipfile.ZipFile(filepath)
        for fname in zfile.namelist():
            if os.path.splitext(fname)[1] == '.ini':
                ini_str = zfile.open(
                    zfile.NameToInfo[fname]).read().decode('utf8')
                break
        return ini_str

    @staticmethod
    def get_multi_peril_csv_dict(ini_str):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read_string(ini_str)
        multi_peril_csv_str = config['volcano_hazard']['multi_peril_csv']
        multi_peril_csv_dict = json.loads(
            multi_peril_csv_str.replace('\'', '"'))
        return multi_peril_csv_dict

    def load_from_csv(self, csv_path):
        # extract the name of the csv file and remove the extension
        layer_name = os.path.splitext(os.path.basename(csv_path))[0]
        try:
            self.layer = import_layer_from_csv(
                self, csv_path, layer_name, self.iface)
        except RuntimeError as exc:
            log_msg(str(exc), level='C', message_bar=self.iface.messageBar(),
                    exception=exc)
            return
        self.style_maps(layer=self.layer, style_by='intensity')
        QgsProject.instance().addMapLayer(self.layer)
        self.iface.setActiveLayer(self.layer)
        self.iface.zoomToActiveLayer()
        # log_msg('Layer %s was loaded successfully' % layer_name,
        #         level='S', message_bar=self.iface.messageBar())

    def style_maps(self, layer=None, style_by=None):
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        # see properties at:
        # https://qgis.org/api/qgsmarkersymbollayerv2_8cpp_source.html#l01073
        symbol.setOpacity(1)
        if isinstance(symbol, QgsMarkerSymbol):
            # do it only for the layer with points
            symbol.symbolLayer(0).setStrokeStyle(Qt.PenStyle(Qt.NoPen))

        style = get_style(layer, self.iface.messageBar())

        # this is the default, as specified in the user settings
        ramp = QgsGradientColorRamp(
            style['color_from'], style['color_to'])
        mode = style['mode']

        default_qgs_style = QgsStyle().defaultStyle()
        default_color_ramp_names = default_qgs_style.colorRampNames()
        # options are EqualInterval, Quantile, Jenks, StdDev, Pretty
        # jenks = natural breaks
        mode = QgsGraduatedSymbolRenderer.EqualInterval
        colors = self.get_colors(style_by)
        single_color = colors['single']
        ramp_name = colors['ramp_name']
        ramp_type_idx = default_color_ramp_names.index(ramp_name)
        inverted = False
        symbol.setColor(QColor(single_color))
        ramp = default_qgs_style.colorRamp(
            default_color_ramp_names[ramp_type_idx])
        if inverted:
            ramp.invert()
        # get unique values
        fni = layer.fields().indexOf(style_by)
        unique_values = layer.dataProvider().uniqueValues(fni)
        num_unique_values = len(unique_values - {NULL})
        if num_unique_values > 2:
            renderer = QgsGraduatedSymbolRenderer.createRenderer(
                layer,
                QgsExpression.quotedColumnRef(style_by),
                min(num_unique_values, style['classes']),
                mode,
                symbol.clone(),
                ramp)
            label_format = renderer.labelFormat()
            # label_format.setTrimTrailingZeroes(True)  # it might be useful
            label_format.setPrecision(2)
            renderer.setLabelFormat(label_format, updateRanges=True)
        elif num_unique_values == 2:
            categories = []
            for unique_value in unique_values:
                symbol = symbol.clone()
                try:
                    symbol.setColor(QColor(RAMP_EXTREME_COLORS[ramp_name][
                        'bottom' if unique_value == min(unique_values)
                        else 'top']))
                except Exception:
                    symbol.setColor(QColor(
                        style['color_from']
                        if unique_value == min(unique_values)
                        else style['color_to']))
                category = QgsRendererCategory(
                    unique_value, symbol, str(unique_value))
                # entry for the list of category items
                categories.append(category)
            renderer = QgsCategorizedSymbolRenderer(
                QgsExpression.quotedColumnRef(style_by), categories)
        else:
            renderer = QgsSingleSymbolRenderer(symbol.clone())
        layer.setRenderer(renderer)
        layer.setOpacity(0.7)
        layer.triggerRepaint()
        self.iface.setActiveLayer(layer)
        self.iface.zoomToActiveLayer()
        log_msg('Layer %s was created successfully' % layer.name(), level='S',
                message_bar=self.iface.messageBar())
        # NOTE QGIS3: probably not needed
        # self.iface.layerTreeView().refreshLayerSymbology(layer.id())

        self.iface.mapCanvas().refresh()

    def get_colors(self, style_by):
        # exposure_strings = ['number', 'occupants', 'value']
        # setting exposure colors by default
        color_dict = {'single': RAMP_EXTREME_COLORS['Blues']['top'],
                      'ramp_name': 'Blues'}
        damage_strings = ['LAHAR', 'LAVA', 'PYRO', 'ASH']
        for damage_string in damage_strings:
            if damage_string in style_by:
                color_dict = {'single': RAMP_EXTREME_COLORS['Reds']['top'],
                              'ramp_name': 'Reds'}
                break
        return color_dict

    def accept(self):
        super().accept()
        for chk in self.peril_gbx.findChildren(QCheckBox):
            if chk.isChecked():
                chosen_peril = chk.text()
                zfile = zipfile.ZipFile(self.zip_filepath)
                extracted_csv_path = zfile.extract(
                    self.multi_peril_csv_dict[chosen_peril],
                    path=os.path.dirname(self.zip_filepath))
                self.load_from_csv(extracted_csv_path)
