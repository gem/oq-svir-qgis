# -*- coding: utf-8 -*-
# /***************************************************************************
# Irmt
#                                 A QGIS plugin
# OpenQuake Integrated Risk Modelling Toolkit
#                              -------------------
#        begin                : 2016-06-29
#        copyright            : (C) 2016 by GEM Foundation
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

import json
from qgis.PyQt.QtCore import QUrl, QObject, pyqtSlot
from qgis.PyQt.QtGui import (QDialog,
                             QVBoxLayout,
                             QPushButton,
                             QSizePolicy,
                             )
from qgis.gui import QgsMessageBar
from svir.ui.gem_qwebview import GemQWebView


class StandaloneAppDialog(QDialog):
    """FIXME Docstring for StandaloneAppDialog. """

    def __init__(self, app_name, app_descr, taxonomy_dlg=None):
        super(StandaloneAppDialog, self).__init__()

        self.message_bar = QgsMessageBar(self)
        self.app_name = app_name
        self.app_descr = app_descr
        self.taxonomy_dlg = taxonomy_dlg
        if app_name == 'ipt':
            self.gem_api = IptPythonApi(self.message_bar)
            self.gem_header_name = "Gem--Qgis-Oq-Irmt--Ipt"
            self.gem_header_value = "0.1.0"
        elif app_name == 'taxtweb':
            # sanity check (we need a reference to the taxonomy dialog, to
            # point to taxonomies selected in the TaxtWEB app)
            assert(self.taxonomy_dlg is not None)
            self.gem_api = TaxtwebPythonApi(
                self.message_bar, self.taxonomy_dlg)
            self.gem_header_name = "Gem--Qgis-Oq-Irmt--Taxtweb"
            self.gem_header_value = "0.1.0"
        elif app_name == 'taxonomy':
            self.gem_api = TaxonomyPythonApi(self.message_bar)
            self.gem_header_name = "Gem--Qgis-Oq-Irmt--Taxonomy"
            self.gem_header_value = "0.1.0"
        else:
            raise NotImplementedError(app_name)

        self.resize(1200, self.width())
        self.web_view = GemQWebView(self.gem_header_name,
                                    self.gem_header_value,
                                    self.gem_api)
        self.web_view.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                                QSizePolicy.MinimumExpanding))
        self.set_example_btn = QPushButton("Set example")
        self.set_example_btn.clicked.connect(self.on_set_example_btn_clicked)
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.message_bar)
        self.vlayout.addWidget(self.web_view)
        if app_name == 'ipt':
            self.vlayout.addWidget(self.set_example_btn)
        self.setLayout(self.vlayout)
        self.setWindowTitle(self.app_descr)

        qurl = QUrl('http://localhost:8800/%s' % self.app_name)
        # # Uncomment to use the dummy example instead
        # if self.app_name == 'taxtweb':
        #     qurl = QUrl('http://localhost:8000')
        self.web_view.load(qurl)

    def on_set_example_btn_clicked(self):
        qurl = QUrl('http://localhost:8800/ipt?tab_id=1&example_id=99')
        self.web_view.load(qurl)


class GemApi(QObject):
    def __init__(self, message_bar):
        super(GemApi, self).__init__()
        self.message_bar = message_bar

    # return the sum of two integers
    @pyqtSlot(int, int, result=int)
    def add(self, a, b):
        return a + b

    # take a list of strings and return a string
    # because of setapi line above, we get a list of python strings as input
    @pyqtSlot('QStringList', result=str)
    def concat(self, strlist):
        return ''.join(strlist)

    # take a javascript object and return string
    # javascript objects come into python as dictionaries
    # functions are represented by an empty dictionary
    @pyqtSlot('QVariantMap', result=str)
    def json_encode(self, jsobj):
        # import is here to keep it separate from 'required' import
        return json.dumps(jsobj)

    # take a string and return an object (which is represented in python
    # by a dictionary
    @pyqtSlot(str, result='QVariantMap')
    def json_decode(self, jsstr):
        return json.loads(jsstr)

    @pyqtSlot()
    def notify_click(self):
        self.message_bar.pushMessage('Clicked!')


class IptPythonApi(GemApi):
    pass


class TaxtwebPythonApi(GemApi):
    def __init__(self, message_bar, taxonomy_dlg):
        super(TaxtwebPythonApi, self).__init__(message_bar)
        self.message_bar = message_bar
        self.taxonomy_dlg = taxonomy_dlg

    @pyqtSlot(str)
    def point_to_taxonomy(self, url):
        qurl = QUrl(url)
        self.taxonomy_dlg.web_view.load(qurl)
        self.taxonomy_dlg.show()
        self.taxonomy_dlg.raise_()


class TaxonomyPythonApi(GemApi):
    pass
