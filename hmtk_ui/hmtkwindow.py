# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hmtk_ui/hmtkwindow.ui'
#
# Created: Tue Sep 10 18:17:07 2013
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_HMTKWindow(object):
    def setupUi(self, HMTKWindow):
        HMTKWindow.setObjectName(_fromUtf8("HMTKWindow"))
        HMTKWindow.resize(1220, 756)
        self.centralWidget = QtGui.QWidget(HMTKWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.stackedFormWidget = QtGui.QStackedWidget(self.centralWidget)
        self.stackedFormWidget.setObjectName(_fromUtf8("stackedFormWidget"))
        self.stackedWidgetDeclustering = QtGui.QWidget()
        self.stackedWidgetDeclustering.setObjectName(_fromUtf8("stackedWidgetDeclustering"))
        self.gridLayout_2 = QtGui.QGridLayout(self.stackedWidgetDeclustering)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.declusteringGroupBox = QtGui.QGroupBox(self.stackedWidgetDeclustering)
        self.declusteringGroupBox.setObjectName(_fromUtf8("declusteringGroupBox"))
        self.declusteringFormLayout = QtGui.QVBoxLayout(self.declusteringGroupBox)
        self.declusteringFormLayout.setObjectName(_fromUtf8("declusteringFormLayout"))
        self.declusteringButtons = QtGui.QHBoxLayout()
        self.declusteringButtons.setObjectName(_fromUtf8("declusteringButtons"))
        self.declusterButton = QtGui.QPushButton(self.declusteringGroupBox)
        self.declusterButton.setObjectName(_fromUtf8("declusterButton"))
        self.declusteringButtons.addWidget(self.declusterButton)
        self.declusteringPurgeButton = QtGui.QPushButton(self.declusteringGroupBox)
        self.declusteringPurgeButton.setObjectName(_fromUtf8("declusteringPurgeButton"))
        self.declusteringButtons.addWidget(self.declusteringPurgeButton)
        self.declusteringFormLayout.addLayout(self.declusteringButtons)
        self.declusteringChart = FigureCanvasQTAggWidget(self.declusteringGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.declusteringChart.sizePolicy().hasHeightForWidth())
        self.declusteringChart.setSizePolicy(sizePolicy)
        self.declusteringChart.setMinimumSize(QtCore.QSize(0, 300))
        self.declusteringChart.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.declusteringChart.setObjectName(_fromUtf8("declusteringChart"))
        self.declusteringFormLayout.addWidget(self.declusteringChart)
        self.gridLayout_2.addWidget(self.declusteringGroupBox, 0, 0, 1, 1)
        self.stackedFormWidget.addWidget(self.stackedWidgetDeclustering)
        self.stackedWidgetCompleteness = QtGui.QWidget()
        self.stackedWidgetCompleteness.setObjectName(_fromUtf8("stackedWidgetCompleteness"))
        self.gridLayout_3 = QtGui.QGridLayout(self.stackedWidgetCompleteness)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.completenessGroupBox = QtGui.QGroupBox(self.stackedWidgetCompleteness)
        self.completenessGroupBox.setObjectName(_fromUtf8("completenessGroupBox"))
        self.completenessFormLayout = QtGui.QVBoxLayout(self.completenessGroupBox)
        self.completenessFormLayout.setObjectName(_fromUtf8("completenessFormLayout"))
        self.completenessButtons = QtGui.QHBoxLayout()
        self.completenessButtons.setObjectName(_fromUtf8("completenessButtons"))
        self.completenessButton = QtGui.QPushButton(self.completenessGroupBox)
        self.completenessButton.setObjectName(_fromUtf8("completenessButton"))
        self.completenessButtons.addWidget(self.completenessButton)
        self.completenessPurgeButton = QtGui.QPushButton(self.completenessGroupBox)
        self.completenessPurgeButton.setObjectName(_fromUtf8("completenessPurgeButton"))
        self.completenessButtons.addWidget(self.completenessPurgeButton)
        self.completenessFormLayout.addLayout(self.completenessButtons)
        self.completenessChart = FigureCanvasQTAggWidget(self.completenessGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.completenessChart.sizePolicy().hasHeightForWidth())
        self.completenessChart.setSizePolicy(sizePolicy)
        self.completenessChart.setMinimumSize(QtCore.QSize(0, 300))
        self.completenessChart.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.completenessChart.setObjectName(_fromUtf8("completenessChart"))
        self.completenessFormLayout.addWidget(self.completenessChart)
        self.gridLayout_3.addWidget(self.completenessGroupBox, 0, 0, 1, 1)
        self.stackedFormWidget.addWidget(self.stackedWidgetCompleteness)
        self.stackedWidgetRecurrenceModel = QtGui.QWidget()
        self.stackedWidgetRecurrenceModel.setObjectName(_fromUtf8("stackedWidgetRecurrenceModel"))
        self.gridLayout_4 = QtGui.QGridLayout(self.stackedWidgetRecurrenceModel)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.recurrenceModelGroupBox = QtGui.QGroupBox(self.stackedWidgetRecurrenceModel)
        self.recurrenceModelGroupBox.setObjectName(_fromUtf8("recurrenceModelGroupBox"))
        self.recurrenceModelFormLayout = QtGui.QVBoxLayout(self.recurrenceModelGroupBox)
        self.recurrenceModelFormLayout.setObjectName(_fromUtf8("recurrenceModelFormLayout"))
        self.recurrenceModelChart = FigureCanvasQTAggWidget(self.recurrenceModelGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recurrenceModelChart.sizePolicy().hasHeightForWidth())
        self.recurrenceModelChart.setSizePolicy(sizePolicy)
        self.recurrenceModelChart.setMinimumSize(QtCore.QSize(0, 300))
        self.recurrenceModelChart.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.recurrenceModelChart.setObjectName(_fromUtf8("recurrenceModelChart"))
        self.recurrenceModelFormLayout.addWidget(self.recurrenceModelChart)
        self.recurrenceModelButton = QtGui.QPushButton(self.recurrenceModelGroupBox)
        self.recurrenceModelButton.setObjectName(_fromUtf8("recurrenceModelButton"))
        self.recurrenceModelFormLayout.addWidget(self.recurrenceModelButton)
        self.gridLayout_4.addWidget(self.recurrenceModelGroupBox, 0, 0, 1, 1)
        self.stackedFormWidget.addWidget(self.stackedWidgetRecurrenceModel)
        self.stackedWidgetMaxMagnitude = QtGui.QWidget()
        self.stackedWidgetMaxMagnitude.setObjectName(_fromUtf8("stackedWidgetMaxMagnitude"))
        self.gridLayout_5 = QtGui.QGridLayout(self.stackedWidgetMaxMagnitude)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.maxMagnitudeGroupBox = QtGui.QGroupBox(self.stackedWidgetMaxMagnitude)
        self.maxMagnitudeGroupBox.setObjectName(_fromUtf8("maxMagnitudeGroupBox"))
        self.maxMagnitudeFormLayout = QtGui.QVBoxLayout(self.maxMagnitudeGroupBox)
        self.maxMagnitudeFormLayout.setObjectName(_fromUtf8("maxMagnitudeFormLayout"))
        self.maxMagnitudeChart = FigureCanvasQTAggWidget(self.maxMagnitudeGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxMagnitudeChart.sizePolicy().hasHeightForWidth())
        self.maxMagnitudeChart.setSizePolicy(sizePolicy)
        self.maxMagnitudeChart.setMinimumSize(QtCore.QSize(0, 300))
        self.maxMagnitudeChart.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.maxMagnitudeChart.setObjectName(_fromUtf8("maxMagnitudeChart"))
        self.maxMagnitudeFormLayout.addWidget(self.maxMagnitudeChart)
        self.maxMagnitudeButton = QtGui.QPushButton(self.maxMagnitudeGroupBox)
        self.maxMagnitudeButton.setObjectName(_fromUtf8("maxMagnitudeButton"))
        self.maxMagnitudeFormLayout.addWidget(self.maxMagnitudeButton)
        self.gridLayout_5.addWidget(self.maxMagnitudeGroupBox, 0, 0, 1, 1)
        self.stackedFormWidget.addWidget(self.stackedWidgetMaxMagnitude)
        self.stackedWidgetSmoothedSeismicity = QtGui.QWidget()
        self.stackedWidgetSmoothedSeismicity.setObjectName(_fromUtf8("stackedWidgetSmoothedSeismicity"))
        self.gridLayout_6 = QtGui.QGridLayout(self.stackedWidgetSmoothedSeismicity)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.smoothedSeismicityGroupBox = QtGui.QGroupBox(self.stackedWidgetSmoothedSeismicity)
        self.smoothedSeismicityGroupBox.setObjectName(_fromUtf8("smoothedSeismicityGroupBox"))
        self.smoothedSeismicityFormLayout = QtGui.QVBoxLayout(self.smoothedSeismicityGroupBox)
        self.smoothedSeismicityFormLayout.setObjectName(_fromUtf8("smoothedSeismicityFormLayout"))
        self.smoothedSeismicityChart = FigureCanvasQTAggWidget(self.smoothedSeismicityGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smoothedSeismicityChart.sizePolicy().hasHeightForWidth())
        self.smoothedSeismicityChart.setSizePolicy(sizePolicy)
        self.smoothedSeismicityChart.setMinimumSize(QtCore.QSize(0, 300))
        self.smoothedSeismicityChart.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.smoothedSeismicityChart.setObjectName(_fromUtf8("smoothedSeismicityChart"))
        self.smoothedSeismicityFormLayout.addWidget(self.smoothedSeismicityChart)
        self.smoothedSeismicityButton = QtGui.QPushButton(self.smoothedSeismicityGroupBox)
        self.smoothedSeismicityButton.setObjectName(_fromUtf8("smoothedSeismicityButton"))
        self.smoothedSeismicityFormLayout.addWidget(self.smoothedSeismicityButton)
        self.gridLayout_6.addWidget(self.smoothedSeismicityGroupBox, 0, 0, 1, 1)
        self.stackedFormWidget.addWidget(self.stackedWidgetSmoothedSeismicity)
        self.horizontalLayout.addWidget(self.stackedFormWidget)
        self.outputVerticalLayout = QtGui.QVBoxLayout()
        self.outputVerticalLayout.setObjectName(_fromUtf8("outputVerticalLayout"))
        self.mapWidget = QgsMapCanvas(self.centralWidget)
        self.mapWidget.setMinimumSize(QtCore.QSize(300, 300))
        self.mapWidget.setObjectName(_fromUtf8("mapWidget"))
        self.outputVerticalLayout.addWidget(self.mapWidget)
        self.outputTableView = QtGui.QTableView(self.centralWidget)
        self.outputTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.outputTableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.outputTableView.setSortingEnabled(True)
        self.outputTableView.setObjectName(_fromUtf8("outputTableView"))
        self.outputTableView.verticalHeader().setVisible(False)
        self.outputVerticalLayout.addWidget(self.outputTableView)
        self.horizontalLayout.addLayout(self.outputVerticalLayout)
        HMTKWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(HMTKWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1220, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        self.menuTools = QtGui.QMenu(self.menuBar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        HMTKWindow.setMenuBar(self.menuBar)
        self.toolBar = QtGui.QToolBar(HMTKWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        HMTKWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLoad_catalogue = QtGui.QAction(HMTKWindow)
        self.actionLoad_catalogue.setObjectName(_fromUtf8("actionLoad_catalogue"))
        self.actionDeclustering = QtGui.QAction(HMTKWindow)
        self.actionDeclustering.setObjectName(_fromUtf8("actionDeclustering"))
        self.actionRecurrenceModel = QtGui.QAction(HMTKWindow)
        self.actionRecurrenceModel.setObjectName(_fromUtf8("actionRecurrenceModel"))
        self.actionCompleteness = QtGui.QAction(HMTKWindow)
        self.actionCompleteness.setObjectName(_fromUtf8("actionCompleteness"))
        self.actionMaximumMagnitude = QtGui.QAction(HMTKWindow)
        self.actionMaximumMagnitude.setObjectName(_fromUtf8("actionMaximumMagnitude"))
        self.actionSmoothedSeismicity = QtGui.QAction(HMTKWindow)
        self.actionSmoothedSeismicity.setObjectName(_fromUtf8("actionSmoothedSeismicity"))
        self.actionSave_catalogue = QtGui.QAction(HMTKWindow)
        self.actionSave_catalogue.setObjectName(_fromUtf8("actionSave_catalogue"))
        self.menuFile.addAction(self.actionLoad_catalogue)
        self.menuFile.addAction(self.actionSave_catalogue)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuTools.addAction(self.actionDeclustering)
        self.menuTools.addAction(self.actionCompleteness)
        self.menuTools.addAction(self.actionRecurrenceModel)
        self.menuTools.addAction(self.actionMaximumMagnitude)
        self.menuTools.addAction(self.actionSmoothedSeismicity)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())

        self.retranslateUi(HMTKWindow)
        self.stackedFormWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HMTKWindow)

    def retranslateUi(self, HMTKWindow):
        HMTKWindow.setWindowTitle(QtGui.QApplication.translate("HMTKWindow", "HMTKWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.declusteringGroupBox.setTitle(QtGui.QApplication.translate("HMTKWindow", "Declustering", None, QtGui.QApplication.UnicodeUTF8))
        self.declusterButton.setText(QtGui.QApplication.translate("HMTKWindow", "Decluster", None, QtGui.QApplication.UnicodeUTF8))
        self.declusteringPurgeButton.setText(QtGui.QApplication.translate("HMTKWindow", "Purge Catalogue", None, QtGui.QApplication.UnicodeUTF8))
        self.completenessGroupBox.setTitle(QtGui.QApplication.translate("HMTKWindow", "Completeness", None, QtGui.QApplication.UnicodeUTF8))
        self.completenessButton.setText(QtGui.QApplication.translate("HMTKWindow", "Run Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.completenessPurgeButton.setText(QtGui.QApplication.translate("HMTKWindow", "Purge Catalogue", None, QtGui.QApplication.UnicodeUTF8))
        self.recurrenceModelGroupBox.setTitle(QtGui.QApplication.translate("HMTKWindow", "Recurrence Model", None, QtGui.QApplication.UnicodeUTF8))
        self.recurrenceModelButton.setText(QtGui.QApplication.translate("HMTKWindow", "Run Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.maxMagnitudeGroupBox.setTitle(QtGui.QApplication.translate("HMTKWindow", "Maximum Magnitude", None, QtGui.QApplication.UnicodeUTF8))
        self.maxMagnitudeButton.setText(QtGui.QApplication.translate("HMTKWindow", "Run Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.smoothedSeismicityGroupBox.setTitle(QtGui.QApplication.translate("HMTKWindow", "Smoothed Seismicity", None, QtGui.QApplication.UnicodeUTF8))
        self.smoothedSeismicityButton.setText(QtGui.QApplication.translate("HMTKWindow", "Run Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("HMTKWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuExport.setTitle(QtGui.QApplication.translate("HMTKWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("HMTKWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("HMTKWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_catalogue.setText(QtGui.QApplication.translate("HMTKWindow", "Load catalogue", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_catalogue.setShortcut(QtGui.QApplication.translate("HMTKWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeclustering.setText(QtGui.QApplication.translate("HMTKWindow", "Declustering", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeclustering.setShortcut(QtGui.QApplication.translate("HMTKWindow", "Ctrl+1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRecurrenceModel.setText(QtGui.QApplication.translate("HMTKWindow", "Recurrence Model", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRecurrenceModel.setShortcut(QtGui.QApplication.translate("HMTKWindow", "Ctrl+3", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCompleteness.setText(QtGui.QApplication.translate("HMTKWindow", "Completeness", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCompleteness.setShortcut(QtGui.QApplication.translate("HMTKWindow", "Ctrl+2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMaximumMagnitude.setText(QtGui.QApplication.translate("HMTKWindow", "Maximum Magnitude", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMaximumMagnitude.setShortcut(QtGui.QApplication.translate("HMTKWindow", "Ctrl+4", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSmoothedSeismicity.setText(QtGui.QApplication.translate("HMTKWindow", "Smoothed Seismicity", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSmoothedSeismicity.setShortcut(QtGui.QApplication.translate("HMTKWindow", "Ctrl+5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_catalogue.setText(QtGui.QApplication.translate("HMTKWindow", "Save catalogue", None, QtGui.QApplication.UnicodeUTF8))

from widgets import FigureCanvasQTAggWidget
from qgis.gui import QgsMapCanvas
