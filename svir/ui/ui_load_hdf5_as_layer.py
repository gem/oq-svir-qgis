# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_load_hdf5_as_layer.ui'
#
# Created: Thu Jul 14 14:03:55 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LoadHdf5AsLayerDialog(object):
    def setupUi(self, LoadHdf5AsLayerDialog):
        LoadHdf5AsLayerDialog.setObjectName(_fromUtf8("LoadHdf5AsLayerDialog"))
        LoadHdf5AsLayerDialog.resize(474, 250)
        self.verticalLayout_2 = QtGui.QVBoxLayout(LoadHdf5AsLayerDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.hdf5_lbl = QtGui.QLabel(LoadHdf5AsLayerDialog)
        self.hdf5_lbl.setObjectName(_fromUtf8("hdf5_lbl"))
        self.horizontalLayout.addWidget(self.hdf5_lbl)
        self.file_browser_tbn = QtGui.QToolButton(LoadHdf5AsLayerDialog)
        self.file_browser_tbn.setObjectName(_fromUtf8("file_browser_tbn"))
        self.horizontalLayout.addWidget(self.file_browser_tbn)
        self.hdf5_path_le = QtGui.QLineEdit(LoadHdf5AsLayerDialog)
        self.hdf5_path_le.setEnabled(False)
        self.hdf5_path_le.setObjectName(_fromUtf8("hdf5_path_le"))
        self.horizontalLayout.addWidget(self.hdf5_path_le)
        self.open_hdfview_btn = QtGui.QPushButton(LoadHdf5AsLayerDialog)
        self.open_hdfview_btn.setEnabled(False)
        self.open_hdfview_btn.setObjectName(_fromUtf8("open_hdfview_btn"))
        self.horizontalLayout.addWidget(self.open_hdfview_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.rlz_lbl = QtGui.QLabel(LoadHdf5AsLayerDialog)
        self.rlz_lbl.setObjectName(_fromUtf8("rlz_lbl"))
        self.verticalLayout.addWidget(self.rlz_lbl)
        self.rlz_cbx = QtGui.QComboBox(LoadHdf5AsLayerDialog)
        self.rlz_cbx.setEnabled(False)
        self.rlz_cbx.setObjectName(_fromUtf8("rlz_cbx"))
        self.verticalLayout.addWidget(self.rlz_cbx)
        self.imt_lbl = QtGui.QLabel(LoadHdf5AsLayerDialog)
        self.imt_lbl.setObjectName(_fromUtf8("imt_lbl"))
        self.verticalLayout.addWidget(self.imt_lbl)
        self.imt_cbx = QtGui.QComboBox(LoadHdf5AsLayerDialog)
        self.imt_cbx.setEnabled(False)
        self.imt_cbx.setObjectName(_fromUtf8("imt_cbx"))
        self.verticalLayout.addWidget(self.imt_cbx)
        self.poe_lbl = QtGui.QLabel(LoadHdf5AsLayerDialog)
        self.poe_lbl.setObjectName(_fromUtf8("poe_lbl"))
        self.verticalLayout.addWidget(self.poe_lbl)
        self.poe_cbx = QtGui.QComboBox(LoadHdf5AsLayerDialog)
        self.poe_cbx.setEnabled(False)
        self.poe_cbx.setObjectName(_fromUtf8("poe_cbx"))
        self.verticalLayout.addWidget(self.poe_cbx)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(LoadHdf5AsLayerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(LoadHdf5AsLayerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LoadHdf5AsLayerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LoadHdf5AsLayerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LoadHdf5AsLayerDialog)

    def retranslateUi(self, LoadHdf5AsLayerDialog):
        LoadHdf5AsLayerDialog.setWindowTitle(_translate("LoadHdf5AsLayerDialog", "Load hdf5 as layer", None))
        self.hdf5_lbl.setText(_translate("LoadHdf5AsLayerDialog", "Hdf5 file", None))
        self.file_browser_tbn.setText(_translate("LoadHdf5AsLayerDialog", "...", None))
        self.open_hdfview_btn.setText(_translate("LoadHdf5AsLayerDialog", "Open with HDFView", None))
        self.rlz_lbl.setText(_translate("LoadHdf5AsLayerDialog", "Realization (only the chosen realization will be loaded into the layer)", None))
        self.imt_lbl.setText(_translate("LoadHdf5AsLayerDialog", "Intensity Measure Type (used for default styling)", None))
        self.poe_lbl.setText(_translate("LoadHdf5AsLayerDialog", "Probability of Exceedance (used for default styling)", None))

