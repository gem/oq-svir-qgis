# -*- coding: utf-8 -*-
# /***************************************************************************
# Irmt
#                                 A QGIS plugin
# OpenQuake Integrated Risk Modelling Toolkit
#                              -------------------
#        begin                : 2014-10-24
#        copyright            : (C) 2014-2017 by GEM Foundation
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

# import qgis libs so that we set the correct sip api version
import os
import sys
import traceback
import tempfile
import copy
import csv
import time
import operator
import requests
from qgis.core import QgsApplication
from qgis.utils import iface
from qgis.testing import unittest
from svir.irmt import Irmt
from svir.utilities.shared import (
                                   OQ_CSV_TO_LAYER_TYPES,
                                   OQ_EXTRACT_TO_LAYER_TYPES,
                                   OQ_RST_TYPES,
                                   OQ_EXTRACT_TO_VIEW_TYPES,
                                   OQ_ZIPPED_TYPES,
                                   OQ_ALL_TYPES,
                                   )
from svir.test.utilities import assert_and_emit
from svir.dialogs.drive_oq_engine_server_dialog import OUTPUT_TYPE_LOADERS
from svir.dialogs.show_full_report_dialog import ShowFullReportDialog
from svir.dialogs.load_inputs_dialog import LoadInputsDialog


QGIS_APP = QgsApplication([], True)

LONG_LOADING_TIME = 10  # seconds


def run_all():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(
        LoadOqEngineOutputsTestCase, 'test'))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)


class FailedAttempts(Exception):
    pass


class LoadOqEngineOutputsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.irmt = Irmt(iface)
        cls.irmt.initGui()
        cls.hostname = os.environ.get('OQ_ENGINE_HOST',
                                      'http://localhost:8800')
        cls.global_failed_attempts = []
        cls.global_skipped_attempts = []
        cls.global_time_consuming_outputs = []
        cls.irmt.drive_oq_engine_server(show=False, hostname=cls.hostname)
        # NOTE: calc_list must be retrieved BEFORE starting any test
        cls.calc_list = cls.irmt.drive_oq_engine_server_dlg.calc_list
        cls.output_list = {}
        try:
            selected_calc_id = int(os.environ.get('SELECTED_CALC_ID'))
        except (ValueError, TypeError):
            print('SELECTED_CALC_ID was not set or is not an integer'
                  ' value. Running tests for all the available calculations')
            selected_calc_id = None
        else:
            print('SELECTED_CALC_ID is set.'
                  ' Running tests only for calculation #%s'
                  % selected_calc_id)
        if selected_calc_id is not None:
            cls.calc_list = [calc for calc in cls.calc_list
                             if calc['id'] == selected_calc_id]
        print("List of tested OQ-Engine demo calculations:")
        for calc in cls.calc_list:
            print('\tCalculation %s (%s): %s' % (calc['id'],
                                                 calc['calculation_mode'],
                                                 calc['description']))
            calc_output_list = \
                cls.irmt.drive_oq_engine_server_dlg.get_output_list(calc['id'])
            cls.output_list[calc['id']] = calc_output_list
            print('\t\tOutput types: %s' % ', '.join(
                [output['type'] for output in calc_output_list]))

    @classmethod
    def tearDownClass(cls):
        print("\n\nGLOBAL SUMMARY")
        print("==============\n")
        if cls.global_skipped_attempts:
            print('\nSkipped:')
            for skipped_attempt in cls.global_skipped_attempts:
                print('\tCalculation %s: %s'
                      % (skipped_attempt['calc_id'],
                         skipped_attempt['calc_description']))
                print('\t\tOutput type: %s' % skipped_attempt['output_type'])
        if not cls.global_failed_attempts:
            print("All the outputs were loaded successfully")
        else:
            print('\nFailed attempts:')
            for failed_attempt in cls.global_failed_attempts:
                print('\tCalculation %s (%s): %s'
                      % (failed_attempt['calc_id'],
                         failed_attempt['calc_mode'],
                         failed_attempt['calc_description']))
                print('\t\tOutput type: %s' % failed_attempt['output_type'])
        if cls.global_time_consuming_outputs:
            print('\n\nSome loaders took longer than %s seconds:' %
                  LONG_LOADING_TIME)
            for output in sorted(cls.global_time_consuming_outputs,
                                 key=operator.itemgetter('loading_time'),
                                 reverse=True):
                print('\t%s' % output)

    @unittest.skip("TODO")
    def test_run_calculation(self):
        # We should:
        #   1) have input files available
        #   2) start the calculation
        #   3) in a loop, print the console log until finished
        #   4) remove the calculation
        pass

    def test_all_loadable_output_types_found_in_demos(self):
        loadable_output_types_found = set()
        loadable_output_types_not_found = set()
        for loadable_output_type in OQ_ALL_TYPES:
            loadable_output_type_found = False
            for calc in self.calc_list:
                for output in self.output_list[calc['id']]:
                    if loadable_output_type == output['type']:
                        loadable_output_type_found = True
                        loadable_output_types_found.add(loadable_output_type)
                        break
                if loadable_output_type_found:
                    break
            if not loadable_output_type_found:
                loadable_output_types_not_found.add(loadable_output_type)
        if loadable_output_types_found:
            print("\nOutput_types found at least in one demo:\n\t%s" %
                  "\n\t".join(loadable_output_types_found))
        else:
            raise RuntimeError("No loadable output type was found in any demo")
        if loadable_output_types_not_found:
            print("\nOutput_types not found in any demo:\n\t%s" %
                  "\n\t".join(loadable_output_types_not_found))
            if all([output_type.endswith('_aggr')
                    for output_type in loadable_output_types_not_found]):
                print("\nThe only missing output types are '_aggr', which are"
                      " not actual outputs exposed by the engine, but"
                      " derived outputs accessed through the extract API."
                      " Therefore, is is ok.")
            else:
                print("\nSome missing output types are '_aggr', which are"
                      " not actual outputs exposed by the engine, but"
                      " derived outputs accessed through the extract API."
                      " Therefore, is is ok:\n\t%s" % "\n\t".join([
                          output_type
                          for output_type in loadable_output_types_not_found
                          if output_type.endswith('_aggr')]))
                raise RuntimeError(
                    "\nThe following loadable output types were not found in"
                    " any demo:\n%s" % "\n\t".join([
                        output_type
                        for output_type in loadable_output_types_not_found
                        if not output_type.endswith('_aggr')]))

    def test_all_loaders_are_implemented(self):
        not_implemented_loaders = set()
        for calc in self.calc_list:
            for output in self.output_list[calc['id']]:
                if output['type'] not in OQ_ALL_TYPES:
                    not_implemented_loaders.add(output['type'])
        if not_implemented_loaders:
            print('\n\nLoaders for the following output types found in the'
                  ' available calculations have not been implemented yet:')
            print(", ".join(not_implemented_loaders))
        else:
            print("All outputs in the demos have a corresponding loader")
        # NOTE: We want green tests even when loaders are still missing

    def download_output(self, output_id, outtype):
        dest_folder = tempfile.gettempdir()
        output_download_url = (
            "%s/v1/calc/result/%s?export_type=%s&dload=true" % (self.hostname,
                                                                output_id,
                                                                outtype))
        print('\t\tGET: %s' % output_download_url, file=sys.stderr)
        # FIXME: enable the user to set verify=True
        resp = requests.get(output_download_url, verify=False)
        if not resp.ok:
            raise Exception(resp.text)
        filename = resp.headers['content-disposition'].split('filename=')[1]
        filepath = os.path.join(dest_folder, filename)
        with open(filepath, "wb") as f:
            f.write(resp.content)
        return filepath

    def _on_loading_ko(self, output_dict):
        ex_type, ex, tb = sys.exc_info()
        failed_attempt = copy.deepcopy(output_dict)
        failed_attempt['traceback'] = tb
        self.failed_attempts.append(failed_attempt)
        self.global_failed_attempts.append(failed_attempt)
        traceback.print_tb(failed_attempt['traceback'])
        print(ex)

    def _on_loading_ok(self, start_time, output_dict):
        loading_time = time.time() - start_time
        print('\t\t(loading time: %.4f sec)' % loading_time)
        if loading_time > LONG_LOADING_TIME:
            output_dict['loading_time'] = loading_time
            self.time_consuming_outputs.append(output_dict)
            self.global_time_consuming_outputs.append(output_dict)

    def load_calc_output(self, calc, selected_output_type):
        calc_id = calc['id']
        for output in self.output_list[calc_id]:
            if (output['type'] != selected_output_type and
                    "%s_aggr" % output['type'] != selected_output_type):
                continue
            output_dict = {'calc_id': calc_id,
                           'calc_mode': calc['calculation_mode'],
                           'calc_description': calc['description'],
                           'output_type': selected_output_type}
            start_time = time.time()
            print('\n\tCalculation %s (%s): %s' % (
                calc['id'], calc['calculation_mode'], calc['description']))
            # NOTE: aggregated outputs use an existing OQ-Engine output and
            #       virtually transforms it postfixing its type with '_aggr'
            output_copy = copy.deepcopy(output)
            output_copy['type'] = selected_output_type
            try:
                loading_resp = self.load_output(calc, output_copy)
            except Exception:
                self._on_loading_ko(output_dict)
            else:
                if loading_resp != 'skipped':
                    self._on_loading_ok(start_time, output_dict)

    def on_init_done(self, dlg):
        # set dialog options and accept
        if dlg.output_type == 'uhs':
            dlg.load_selected_only_ckb.setChecked(True)
            assert_and_emit(
                dlg.loading_exception, self.assertGreater,
                dlg.poe_cbx.count(), 0, 'No PoE was found')
            dlg.poe_cbx.setCurrentIndex(0)
        elif dlg.output_type == 'losses_by_asset':
            # FIXME: testing only for the first taxonomy that is found
            dlg.load_selected_only_ckb.setChecked(True)
            assert_and_emit(
                dlg.loading_exception, self.assertGreater,
                dlg.taxonomy_cbx.count(), 0, 'No taxonomy was found')
            dlg.taxonomy_cbx.setCurrentIndex(0)
            assert_and_emit(
                dlg.loading_exception, self.assertGreater,
                dlg.loss_type_cbx.count(), 0, 'No loss type was found')
            dlg.loss_type_cbx.setCurrentIndex(0)

            # # FIXME: we need to do dlg.accept() also for the case
            #          loading all taxonomies, and performing the
            #          aggregation by zone

            # # test all taxonomies
            # dlg.load_selected_only_ckb.setChecked(True)
            # taxonomy_idx = dlg.taxonomy_cbx.findText('All')
            # self.assertNotEqual(taxonomy_idx, -1,
            #                     'Taxonomy All was not found')
            # dlg.taxonomy_cbx.setCurrentIndex(taxonomy_idx)
            # loss_type_idx = dlg.loss_type_cbx.findText('structural')
            # self.assertNotEqual(loss_type_idx, -1,
            #                     'Loss type structural was not found')
            # dlg.loss_type_cbx.setCurrentIndex(loss_type_idx)
            # dlg.accept()

            # FIXME: copied/pasted from skipped unit test
            #        that was causing segfault
            # loss_layer_path = os.path.join(
            #     self.data_dir_name, 'risk',
            #     'output-399-losses_by_asset_123.npz')
            # zonal_layer_path = os.path.join(
            #     self.data_dir_name, 'risk', 'zonal_layer.shp')
            # dlg = LoadLossesByAssetAsLayerDialog(
            #     self.irmt.iface, self.irmt.viewer_dock,
            #     Mock(), Mock(), Mock(),
            #     'losses_by_asset', loss_layer_path,
            #     zonal_layer_path=zonal_layer_path)
            # dlg.load_selected_only_ckb.setChecked(True)
            # dlg.zonal_layer_gbx.setChecked(True)
            # taxonomy_idx = dlg.taxonomy_cbx.findText('All')
            # self.assertNotEqual(taxonomy_idx, -1,
            #                    'Taxonomy All was not found')
            # dlg.taxonomy_cbx.setCurrentIndex(taxonomy_idx)
            # loss_type_idx = dlg.loss_type_cbx.findText('structural')
            # self.assertNotEqual(loss_type_idx, -1,
            #                     'Loss type structural was not found')
            # dlg.loss_type_cbx.setCurrentIndex(loss_type_idx)
            # self.assertTrue(dlg.zonal_layer_cbx.currentText(),
            #                 'The zonal layer was not loaded')
            # dlg.accept()
            # zonal_layer_plus_stats = [
            #     layer for layer in self.irmt.iface.layers()
            #     if layer.name() == 'Zonal data (copy)'][0]
            # zonal_layer_plus_stats_first_feat = \
            #     zonal_layer_plus_stats.getFeatures().next()
            # expected_zonal_layer_path = os.path.join(
            #     self.data_dir_name, 'risk',
            #     'zonal_layer_plus_losses_by_asset_stats.shp')
            # expected_zonal_layer = QgsVectorLayer(
            #     expected_zonal_layer_path, 'Zonal data', 'ogr')
            # expected_zonal_layer_first_feat = \
            #     expected_zonal_layer.getFeatures().next()
            # assert_almost_equal(
            #     zonal_layer_plus_stats_first_feat.attributes(),
            #     expected_zonal_layer_first_feat.attributes())
        elif dlg.output_type == 'dmg_by_asset':
            # FIXME: testing only for selected taxonomy
            dlg.load_selected_only_ckb.setChecked(True)
            assert_and_emit(
                dlg.loading_exception, self.assertGreater,
                dlg.taxonomy_cbx.count(), 0, 'No taxonomy was found')
            dlg.taxonomy_cbx.setCurrentIndex(0)
            assert_and_emit(
                dlg.loading_exception, self.assertGreater,
                dlg.loss_type_cbx.count(), 0, 'No loss_type was found')
            dlg.loss_type_cbx.setCurrentIndex(0)
            assert_and_emit(
                dlg.loading_exception, self.assertGreater,
                dlg.dmg_state_cbx.count(), 0, 'No damage state was found')
            dlg.dmg_state_cbx.setCurrentIndex(0)

            # # FIXME: we need to do dlg.accept() also for the case
            #          loading all taxonomies, and performing the
            #          aggregation by zone
            # dlg.load_selected_only_ckb.setChecked(True)
            # taxonomy_idx = dlg.taxonomy_cbx.findText('All')
            # self.assertNotEqual(
            #     taxonomy_idx, -1, 'Taxonomy All was not found')
            # dlg.taxonomy_cbx.setCurrentIndex(taxonomy_idx)
            # loss_type_idx = dlg.loss_type_cbx.findText('structural')
            # self.assertNotEqual(loss_type_idx, -1,
            #                     'Loss type structural was not found')
            # dlg.loss_type_cbx.setCurrentIndex(loss_type_idx)
            # dmg_state_idx = dlg.dmg_state_cbx.findText('moderate')
            # self.assertNotEqual(
            #     dmg_state_idx, -1,
            #     'Damage state moderate was not found')
            # dlg.dmg_state_cbx.setCurrentIndex(dmg_state_idx)

            # FIXME: copied/pasted from skipped unit test
            #        that was causing segfault
            #        (test_load_dmg_by_asset_aggregate_by_zone)
            # dmg_layer_path = os.path.join(
            #     self.data_dir_name, 'risk',
            #     'output-1614-dmg_by_asset_356.npz')
            # zonal_layer_path = os.path.join(
            #     self.data_dir_name, 'risk',
            #     'zonal_layer.shp')
            # dlg.load_selected_only_ckb.setChecked(True)
            # dlg.zonal_layer_gbx.setChecked(True)
            # taxonomy_idx = dlg.taxonomy_cbx.findText('All')
            # self.assertNotEqual(
            #     taxonomy_idx, -1, 'Taxonomy All was not found')
            # dlg.taxonomy_cbx.setCurrentIndex(taxonomy_idx)
            # loss_type_idx = dlg.loss_type_cbx.findText('structural')
            # self.assertNotEqual(loss_type_idx, -1,
            #                     'Loss type structural was not found')
            # dlg.loss_type_cbx.setCurrentIndex(loss_type_idx)
            # dmg_state_idx = dlg.dmg_state_cbx.findText('moderate')
            # self.assertNotEqual(
            #     dmg_state_idx, -1,
            #     'Damage state moderate was not found')
            # dlg.dmg_state_cbx.setCurrentIndex(dmg_state_idx)
            # dlg.accept()
            # zonal_layer_plus_stats = [
            #     layer for layer in self.irmt.iface.layers()
            #     if layer.name() == 'Zonal data (copy)'][0]
            # zonal_layer_plus_stats_first_feat = \
            #     zonal_layer_plus_stats.getFeatures().next()
            # expected_zonal_layer_path = os.path.join(
            #     self.data_dir_name, 'risk',
            #     'zonal_layer_plus_dmg_by_asset_stats.shp')
            # expected_zonal_layer = QgsVectorLayer(
            #     expected_zonal_layer_path, 'Zonal data', 'ogr')
            # expected_zonal_layer_first_feat = \
            #     expected_zonal_layer.getFeatures().next()
            # assert_almost_equal(
            #     zonal_layer_plus_stats_first_feat.attributes(),
            #     expected_zonal_layer_first_feat.attributes())
        elif dlg.output_type == 'asset_risk':
            num_selected_taxonomies = len(
                list(dlg.taxonomies_multisel.get_selected_items()))
            num_unselected_taxonomies = len(
                list(dlg.taxonomies_multisel.get_unselected_items()))
            num_taxonomies = (
                num_selected_taxonomies + num_unselected_taxonomies)
            assert_and_emit(
                dlg.loading_exception, self.assertGreater,
                num_taxonomies, 0, 'No taxonomy was found')
            assert_and_emit(
                dlg.loading_exception, self.assertGreater,
                dlg.category_cbx.count(), 0, 'No category was found')
            dlg.category_cbx.setCurrentIndex(0)
        if dlg.ok_button.isEnabled():
            dlg.accept()
            if dlg.output_type == 'asset_risk':
                # NOTE: avoiding to emit loading_completed for asset_risk,
                # because in this case there's a second asynchronous call to
                # the extract api, and the signal is emitted by the callback
                return
        else:
            raise RuntimeError('The ok button is disabled')
        if dlg.output_type == 'hcurves':
            self.load_hcurves()
        elif dlg.output_type == 'uhs':
            self._set_output_type('Uniform Hazard Spectra')
            self._change_selection()
            # test exporting the current selection to csv
            self._test_export()
        dlg.loading_completed.emit()

    def _store_skipped_attempt(self, id, calculation_mode, description, type):
        skipped_attempt = {
            'calc_id': id,
            'calc_mode': calculation_mode,
            'calc_description': description,
            'output_type': type}
        self.skipped_attempts.append(skipped_attempt)
        self.global_skipped_attempts.append(skipped_attempt)

    def load_output(self, calc, output):
        # NOTE: it is better to avoid resetting the project here, because some
        # outputs might be skipped, therefore it would not be needed
        calc_id = calc['id']
        output_type = output['type']
        # NOTE: loading zipped output only for multi_risk
        if output_type == 'input' and calc['calculation_mode'] != 'multi_risk':
            self._store_skipped_attempt(
                calc_id, calc['calculation_mode'],
                calc['description'], output_type)
            print('\t\tSKIPPED')
            return 'skipped'
        if output_type in (OQ_CSV_TO_LAYER_TYPES |
                           OQ_RST_TYPES | OQ_ZIPPED_TYPES):
            if output_type in OQ_CSV_TO_LAYER_TYPES:
                filetype = 'csv'
            elif output_type in OQ_RST_TYPES:
                filetype = 'rst'
            else:  # OQ_ZIPPED_TYPES
                filetype = 'zip'
            # TODO: we should test the actual downloader, asynchronously
            filepath = self.download_output(output['id'], filetype)
            assert filepath is not None
            self.irmt.iface.newProject()
            if output_type == 'fullreport':
                dlg = ShowFullReportDialog(filepath)
                dlg.accept()
                print('\t\tok')
                return 'ok'
            if output_type in OQ_ZIPPED_TYPES:
                dlg = LoadInputsDialog(filepath, self.irmt.iface)
                dlg.accept()
                print('\t\tok')
                return 'ok'
            dlg = OUTPUT_TYPE_LOADERS[output_type](
                self.irmt.iface, self.irmt.viewer_dock,
                self.irmt.drive_oq_engine_server_dlg.session,
                self.hostname, calc_id, output_type, filepath)
            if dlg.ok_button.isEnabled():
                dlg.accept()
                print('\t\tok')
                return 'ok'
            else:
                raise RuntimeError('The ok button is disabled')
                return 'ko'
        elif output_type in OQ_EXTRACT_TO_LAYER_TYPES:
            self.irmt.iface.newProject()
            dlg = OUTPUT_TYPE_LOADERS[output_type](
                self.irmt.iface, self.irmt.viewer_dock,
                self.irmt.drive_oq_engine_server_dlg.session,
                self.hostname, calc_id, output_type)
            self.loading_completed = False
            self.loading_exception = None
            dlg.loading_completed.connect(self.on_loading_completed)
            dlg.loading_exception[Exception].connect(self.on_loading_exception)
            dlg.init_done.connect(
                lambda: self.on_init_done(dlg))
            timeout = 10
            start_time = time.time()
            while time.time() - start_time < timeout:
                QGIS_APP.processEvents()
                if self.loading_completed:
                    print('\t\tok')
                    return 'ok'
                if self.loading_exception:
                    raise self.loading_exception
                    return 'ok'
                time.sleep(0.1)
            raise TimeoutError(
                'Loading time exceeded %s seconds' % timeout)
            return 'ko'
        elif output_type in OQ_EXTRACT_TO_VIEW_TYPES:
            self.irmt.iface.newProject()
            self.irmt.viewer_dock.load_no_map_output(
                calc_id, self.irmt.drive_oq_engine_server_dlg.session,
                self.hostname, output_type,
                self.irmt.drive_oq_engine_server_dlg.engine_version)
            tmpfile_handler, tmpfile_name = tempfile.mkstemp()
            self.irmt.viewer_dock.write_export_file(tmpfile_name)
            os.close(tmpfile_handler)
            print('\t\tok')
            return 'ok'

    def on_loading_completed(self):
        self.loading_completed = True

    def on_loading_exception(self, exception):
        self.loading_exception = exception

    def load_output_type(self, selected_output_type):
        self.failed_attempts = []
        self.skipped_attempts = []
        self.time_consuming_outputs = []
        for calc in self.calc_list:
            self.load_calc_output(calc, selected_output_type)
        if self.skipped_attempts:
            print('\nSkipped:')
            for skipped_attempt in self.skipped_attempts:
                print('\tCalculation %s: %s'
                      % (skipped_attempt['calc_id'],
                         skipped_attempt['calc_description']))
                print('\t\tOutput type: %s' % skipped_attempt['output_type'])
        if not self.failed_attempts:
            print('\n%s successfully loaded for all calculations' %
                  selected_output_type)
        else:
            failing_summary = ''
            for failed_attempt in self.failed_attempts:
                failing_summary += '\n\tCalculation %s (%s): %s\n%s' % (
                    failed_attempt['calc_id'],
                    failed_attempt['calc_mode'],
                    failed_attempt['calc_description'],
                    ''.join(traceback.format_tb(failed_attempt['traceback'])))
            raise FailedAttempts(failing_summary)
        if self.time_consuming_outputs:
            print('\n\nSome loaders took longer than %s seconds:' %
                  LONG_LOADING_TIME)
            for output in sorted(self.time_consuming_outputs,
                                 key=operator.itemgetter('loading_time'),
                                 reverse=True):
                print('\t%s' % output)

    def load_hcurves(self):
        self._set_output_type('Hazard Curves')
        self._change_selection()
        # test changing intensity measure type
        layer = self.irmt.iface.activeLayer()
        # select the first 2 features (the same used to produce the reference
        # csv)
        num_feats = layer.featureCount()
        self.assertGreater(
            num_feats, 0, 'The layer does not contain any feature!')
        if num_feats > 1:
            layer.select([1, 2])
        else:
            layer.select([1])
        self.assertGreater(
            self.irmt.viewer_dock.imt_cbx.count(), 0, 'No IMT was found!')
        self.irmt.viewer_dock.imt_cbx.setCurrentIndex(0)
        # test exporting the current selection to csv
        _, exported_file_path = tempfile.mkstemp(suffix=".csv")
        self._test_export()

    def _test_export(self):
        _, exported_file_path = tempfile.mkstemp(suffix=".csv")
        layer = self.irmt.iface.activeLayer()
        # select the first 2 features (the same used to produce the reference
        # csv)
        num_feats = layer.featureCount()
        self.assertGreater(
            num_feats, 0, 'The layer does not contain any feature!')
        if num_feats > 1:
            layer.select([1, 2])
        else:
            layer.select([1])
        # probably we have the wrong layer selected (uhs produce many layers)
        self.irmt.viewer_dock.write_export_file(exported_file_path)
        # NOTE: we are only checking that the exported CSV has at least 2 rows
        # and 3 columns per row. We are avoiding more precise checks, because
        # CSV tests are very fragile. On different platforms the numbers could
        # be slightly different. With different versions of
        # shapely/libgeos/numpy/etc the numbers could be slightly different.
        # The parameters of the demos could change in the future and the
        # numbers (even the number of rows and columns) could change.
        with open(exported_file_path, 'r', newline='') as got:
            got_reader = csv.reader(got)
            n_rows = 0
            for got_line in got_reader:
                if got_line[0].startswith('#'):
                    continue
                n_rows += 1
                n_cols = 0
                for got_element in got_line:
                    n_cols += 1
                self.assertGreaterEqual(
                    n_cols, 3,
                    "The following line of the exported file %s has"
                    " only %s columns:\n%s" % (
                        exported_file_path, n_cols, got_line))
            self.assertGreaterEqual(
                n_rows, 2,
                "The exported file %s has only %s rows" % (
                    exported_file_path, n_rows))

    def _set_output_type(self, output_type):
        idx = self.irmt.viewer_dock.output_type_cbx.findText(output_type)
        self.assertNotEqual(idx, -1, 'Output type %s not found' % output_type)
        self.irmt.viewer_dock.output_type_cbx.setCurrentIndex(idx)

    def _change_selection(self):
        layer = self.irmt.iface.activeLayer()
        # the behavior should be slightly different (pluralizing labels, etc)
        # depending on the amount of features selected
        num_feats = layer.featureCount()
        self.assertGreater(
            num_feats, 0, 'The layer does not contain any feature!')
        # select first feature only
        layer.select(1)
        layer.removeSelection()
        # select first and last features (just one if there is only one)
        layer.select([1, num_feats])
        layer.removeSelection()
        # NOTE: in the past, we were also selecting all features, but it was
        # not necessary ant it made tests much slower in case of many features


# For each loadable output type, create dinamically a test that loads it from
# all available demo calculations
for output_type in OQ_ALL_TYPES:
    def test_func(output_type):
        return lambda self: self.load_output_type(output_type)
    setattr(LoadOqEngineOutputsTestCase,
            "test_load_%s" % output_type,
            test_func(output_type))
