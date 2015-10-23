# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'elkamainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ElkaMainWindow(object):
    def setupUi(self, ElkaMainWindow):
        ElkaMainWindow.setObjectName("ElkaMainWindow")
        ElkaMainWindow.resize(800, 457)
        self.centralWidget = QtWidgets.QWidget(ElkaMainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.tab_widget = QtWidgets.QTabWidget(self.centralWidget)
        self.tab_widget.setGeometry(QtCore.QRect(0, 0, 801, 431))
        self.tab_widget.setDocumentMode(False)
        self.tab_widget.setObjectName("tab_widget")
        self.Command = QtWidgets.QWidget()
        self.Command.setObjectName("Command")
        self.frame = QtWidgets.QFrame(self.Command)
        self.frame.setGeometry(QtCore.QRect(0, 0, 801, 401))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gains_kpp = QtWidgets.QSpinBox(self.frame)
        self.gains_kpp.setGeometry(QtCore.QRect(10, 290, 44, 27))
        self.gains_kpp.setObjectName("gains_kpp")
        self.gains_label = QtWidgets.QLabel(self.frame)
        self.gains_label.setGeometry(QtCore.QRect(10, 270, 251, 17))
        self.gains_label.setObjectName("gains_label")
        self.gains_kip = QtWidgets.QSpinBox(self.frame)
        self.gains_kip.setGeometry(QtCore.QRect(60, 290, 44, 27))
        self.gains_kip.setObjectName("gains_kip")
        self.gains_kdp = QtWidgets.QSpinBox(self.frame)
        self.gains_kdp.setGeometry(QtCore.QRect(110, 290, 44, 27))
        self.gains_kdp.setObjectName("gains_kdp")
        self.gains_kpr = QtWidgets.QSpinBox(self.frame)
        self.gains_kpr.setGeometry(QtCore.QRect(160, 290, 44, 27))
        self.gains_kpr.setObjectName("gains_kpr")
        self.gains_kir = QtWidgets.QSpinBox(self.frame)
        self.gains_kir.setGeometry(QtCore.QRect(210, 290, 44, 27))
        self.gains_kir.setObjectName("gains_kir")
        self.gains_kdr = QtWidgets.QSpinBox(self.frame)
        self.gains_kdr.setGeometry(QtCore.QRect(260, 290, 44, 27))
        self.gains_kdr.setObjectName("gains_kdr")
        self.gains_kpy = QtWidgets.QSpinBox(self.frame)
        self.gains_kpy.setGeometry(QtCore.QRect(310, 290, 44, 27))
        self.gains_kpy.setObjectName("gains_kpy")
        self.input_label = QtWidgets.QLabel(self.frame)
        self.input_label.setGeometry(QtCore.QRect(20, 10, 71, 17))
        self.input_label.setObjectName("input_label")
        self.joystick_input_button = QtWidgets.QRadioButton(self.frame)
        self.joystick_input_button.setGeometry(QtCore.QRect(10, 30, 105, 22))
        self.joystick_input_button.setObjectName("joystick_input_button")
        self.keyboard_input_button = QtWidgets.QRadioButton(self.frame)
        self.keyboard_input_button.setGeometry(QtCore.QRect(10, 50, 105, 22))
        self.keyboard_input_button.setObjectName("keyboard_input_button")
        self.manual_input_line = QtWidgets.QLineEdit(self.frame)
        self.manual_input_line.setGeometry(QtCore.QRect(10, 360, 781, 27))
        self.manual_input_line.setObjectName("manual_input_line")
        self.manual_input_label = QtWidgets.QLabel(self.frame)
        self.manual_input_label.setGeometry(QtCore.QRect(338, 330, 111, 20))
        self.manual_input_label.setObjectName("manual_input_label")
        self.stop_elka_button = QtWidgets.QPushButton(self.frame)
        self.stop_elka_button.setGeometry(QtCore.QRect(670, 80, 85, 27))
        self.stop_elka_button.setObjectName("stop_elka_button")
        self.start_elka_button = QtWidgets.QPushButton(self.frame)
        self.start_elka_button.setGeometry(QtCore.QRect(670, 20, 85, 27))
        self.start_elka_button.setObjectName("start_elka_button")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(670, 140, 85, 27))
        self.pushButton.setObjectName("pushButton")
        self.tab_widget.addTab(self.Command, "")
        self.Plot = QtWidgets.QWidget()
        self.Plot.setObjectName("Plot")
        self.parse_log_button = QtWidgets.QPushButton(self.Plot)
        self.parse_log_button.setGeometry(QtCore.QRect(10, 30, 85, 27))
        self.parse_log_button.setObjectName("parse_log_button")
        self.data_sets_tree = QtWidgets.QTreeWidget(self.Plot)
        self.data_sets_tree.setGeometry(QtCore.QRect(510, 10, 281, 191))
        self.data_sets_tree.setObjectName("data_sets_tree")
        item_0 = QtWidgets.QTreeWidgetItem(self.data_sets_tree)
        item_0 = QtWidgets.QTreeWidgetItem(self.data_sets_tree)
        item_0 = QtWidgets.QTreeWidgetItem(self.data_sets_tree)
        item_0 = QtWidgets.QTreeWidgetItem(self.data_sets_tree)
        item_0 = QtWidgets.QTreeWidgetItem(self.data_sets_tree)
        self.save_log_button = QtWidgets.QPushButton(self.Plot)
        self.save_log_button.setGeometry(QtCore.QRect(10, 90, 85, 27))
        self.save_log_button.setObjectName("save_log_button")
        self.export_data_button = QtWidgets.QPushButton(self.Plot)
        self.export_data_button.setGeometry(QtCore.QRect(10, 150, 85, 27))
        self.export_data_button.setObjectName("export_data_button")
        self.pushButton_2 = QtWidgets.QPushButton(self.Plot)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 210, 85, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tab_widget.addTab(self.Plot, "")
        self.Editor = QtWidgets.QWidget()
        self.Editor.setObjectName("Editor")
        self.scripts_text_browser = QtWidgets.QTextBrowser(self.Editor)
        self.scripts_text_browser.setGeometry(QtCore.QRect(0, 0, 801, 401))
        self.scripts_text_browser.setFrameShape(QtWidgets.QFrame.Box)
        self.scripts_text_browser.setUndoRedoEnabled(True)
        self.scripts_text_browser.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.scripts_text_browser.setReadOnly(False)
        self.scripts_text_browser.setObjectName("scripts_text_browser")
        self.tab_widget.addTab(self.Editor, "")
        ElkaMainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(ElkaMainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtWidgets.QMenu(self.menuBar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Edit = QtWidgets.QMenu(self.menuBar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menu_Run = QtWidgets.QMenu(self.menuBar)
        self.menu_Run.setObjectName("menu_Run")
        self.menuInput_Mode = QtWidgets.QMenu(self.menu_Run)
        self.menuInput_Mode.setObjectName("menuInput_Mode")
        self.menu_Help = QtWidgets.QMenu(self.menuBar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_Plot = QtWidgets.QMenu(self.menuBar)
        self.menu_Plot.setObjectName("menu_Plot")
        ElkaMainWindow.setMenuBar(self.menuBar)
        self.action_Open = QtWidgets.QAction(ElkaMainWindow)
        self.action_Open.setObjectName("action_Open")
        self.action_Open_2 = QtWidgets.QAction(ElkaMainWindow)
        self.action_Open_2.setObjectName("action_Open_2")
        self.action_New = QtWidgets.QAction(ElkaMainWindow)
        self.action_New.setObjectName("action_New")
        self.action_Save_As = QtWidgets.QAction(ElkaMainWindow)
        self.action_Save_As.setObjectName("action_Save_As")
        self.action_Save = QtWidgets.QAction(ElkaMainWindow)
        self.action_Save.setObjectName("action_Save")
        self.action_Exit = QtWidgets.QAction(ElkaMainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.action_Exit_2 = QtWidgets.QAction(ElkaMainWindow)
        self.action_Exit_2.setObjectName("action_Exit_2")
        self.action_Exit_3 = QtWidgets.QAction(ElkaMainWindow)
        self.action_Exit_3.setObjectName("action_Exit_3")
        self.action_Undo = QtWidgets.QAction(ElkaMainWindow)
        self.action_Undo.setObjectName("action_Undo")
        self.action_Redo = QtWidgets.QAction(ElkaMainWindow)
        self.action_Redo.setObjectName("action_Redo")
        self.action_Cut = QtWidgets.QAction(ElkaMainWindow)
        self.action_Cut.setObjectName("action_Cut")
        self.action_Paste = QtWidgets.QAction(ElkaMainWindow)
        self.action_Paste.setObjectName("action_Paste")
        self.action_Paste_2 = QtWidgets.QAction(ElkaMainWindow)
        self.action_Paste_2.setObjectName("action_Paste_2")
        self.action_Joystick = QtWidgets.QAction(ElkaMainWindow)
        self.action_Joystick.setCheckable(True)
        self.action_Joystick.setObjectName("action_Joystick")
        self.action_Keyboard = QtWidgets.QAction(ElkaMainWindow)
        self.action_Keyboard.setCheckable(True)
        self.action_Keyboard.setObjectName("action_Keyboard")
        self.action_Help_Dialogs = QtWidgets.QAction(ElkaMainWindow)
        self.action_Help_Dialogs.setObjectName("action_Help_Dialogs")
        self.actionProperties = QtWidgets.QAction(ElkaMainWindow)
        self.actionProperties.setObjectName("actionProperties")
        self.action_Start_Elka = QtWidgets.QAction(ElkaMainWindow)
        self.action_Start_Elka.setObjectName("action_Start_Elka")
        self.action_Parse_Log = QtWidgets.QAction(ElkaMainWindow)
        self.action_Parse_Log.setObjectName("action_Parse_Log")
        self.action_Save_Log = QtWidgets.QAction(ElkaMainWindow)
        self.action_Save_Log.setObjectName("action_Save_Log")
        self.action_Export_Data = QtWidgets.QAction(ElkaMainWindow)
        self.action_Export_Data.setObjectName("action_Export_Data")
        self.action_Plot_Data = QtWidgets.QAction(ElkaMainWindow)
        self.action_Plot_Data.setObjectName("action_Plot_Data")
        self.actionProperties_2 = QtWidgets.QAction(ElkaMainWindow)
        self.actionProperties_2.setObjectName("actionProperties_2")
        self.actionStart_Elka = QtWidgets.QAction(ElkaMainWindow)
        self.actionStart_Elka.setObjectName("actionStart_Elka")
        self.action_Stop_Elka = QtWidgets.QAction(ElkaMainWindow)
        self.action_Stop_Elka.setObjectName("action_Stop_Elka")
        self.action_Set_Gains = QtWidgets.QAction(ElkaMainWindow)
        self.action_Set_Gains.setObjectName("action_Set_Gains")
        self.menu_File.addAction(self.action_New)
        self.menu_File.addAction(self.action_Open_2)
        self.menu_File.addAction(self.action_Save_As)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit_3)
        self.menu_Edit.addAction(self.action_Undo)
        self.menu_Edit.addAction(self.action_Redo)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Cut)
        self.menu_Edit.addAction(self.action_Paste)
        self.menu_Edit.addAction(self.action_Paste_2)
        self.menuInput_Mode.addAction(self.action_Joystick)
        self.menuInput_Mode.addAction(self.action_Keyboard)
        self.menu_Run.addAction(self.menuInput_Mode.menuAction())
        self.menu_Run.addAction(self.action_Set_Gains)
        self.menu_Run.addSeparator()
        self.menu_Run.addAction(self.actionStart_Elka)
        self.menu_Run.addAction(self.action_Stop_Elka)
        self.menu_Run.addSeparator()
        self.menu_Run.addAction(self.actionProperties_2)
        self.menu_Help.addAction(self.action_Help_Dialogs)
        self.menu_Help.addAction(self.actionProperties)
        self.menu_Plot.addAction(self.action_Parse_Log)
        self.menu_Plot.addAction(self.action_Save_Log)
        self.menu_Plot.addAction(self.action_Export_Data)
        self.menu_Plot.addAction(self.action_Plot_Data)
        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menu_Edit.menuAction())
        self.menuBar.addAction(self.menu_Run.menuAction())
        self.menuBar.addAction(self.menu_Plot.menuAction())
        self.menuBar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(ElkaMainWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ElkaMainWindow)

    def retranslateUi(self, ElkaMainWindow):
        _translate = QtCore.QCoreApplication.translate
        ElkaMainWindow.setWindowTitle(_translate("ElkaMainWindow", "ElkaMainWindow"))
        self.gains_label.setText(_translate("ElkaMainWindow", "Gains: kpp,kip,kdp,kpr,kir,kdr,kpy"))
        self.input_label.setText(_translate("ElkaMainWindow", "Input Mode"))
        self.joystick_input_button.setText(_translate("ElkaMainWindow", "Joystick"))
        self.keyboard_input_button.setText(_translate("ElkaMainWindow", "Keyboard"))
        self.manual_input_label.setText(_translate("ElkaMainWindow", "Manual Command"))
        self.stop_elka_button.setText(_translate("ElkaMainWindow", "Stop Elka"))
        self.start_elka_button.setText(_translate("ElkaMainWindow", "Start Elka"))
        self.pushButton.setText(_translate("ElkaMainWindow", "Properties"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.Command), _translate("ElkaMainWindow", "Command"))
        self.parse_log_button.setText(_translate("ElkaMainWindow", "Parse Log"))
        self.data_sets_tree.headerItem().setText(0, _translate("ElkaMainWindow", "Current Data Sets"))
        __sortingEnabled = self.data_sets_tree.isSortingEnabled()
        self.data_sets_tree.setSortingEnabled(False)
        self.data_sets_tree.topLevelItem(0).setText(0, _translate("ElkaMainWindow", "Inputs"))
        self.data_sets_tree.topLevelItem(1).setText(0, _translate("ElkaMainWindow", "Outputs"))
        self.data_sets_tree.topLevelItem(2).setText(0, _translate("ElkaMainWindow", "Gains"))
        self.data_sets_tree.topLevelItem(3).setText(0, _translate("ElkaMainWindow", "Acks"))
        self.data_sets_tree.topLevelItem(4).setText(0, _translate("ElkaMainWindow", "Drops"))
        self.data_sets_tree.setSortingEnabled(__sortingEnabled)
        self.save_log_button.setText(_translate("ElkaMainWindow", "Save Log"))
        self.export_data_button.setText(_translate("ElkaMainWindow", "Export Data"))
        self.pushButton_2.setText(_translate("ElkaMainWindow", "Plot Data"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.Plot), _translate("ElkaMainWindow", "Plot"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.Editor), _translate("ElkaMainWindow", "Editor"))
        self.menu_File.setTitle(_translate("ElkaMainWindow", "&File"))
        self.menu_Edit.setTitle(_translate("ElkaMainWindow", "&Edit"))
        self.menu_Run.setTitle(_translate("ElkaMainWindow", "&Run"))
        self.menuInput_Mode.setTitle(_translate("ElkaMainWindow", "Input Mode"))
        self.menu_Help.setTitle(_translate("ElkaMainWindow", "&Help"))
        self.menu_Plot.setTitle(_translate("ElkaMainWindow", "&Plot"))
        self.action_Open.setText(_translate("ElkaMainWindow", "&Open"))
        self.action_Open_2.setText(_translate("ElkaMainWindow", "&Open"))
        self.action_New.setText(_translate("ElkaMainWindow", "&New"))
        self.action_Save_As.setText(_translate("ElkaMainWindow", "&Save As"))
        self.action_Save.setText(_translate("ElkaMainWindow", "&Save"))
        self.action_Exit.setText(_translate("ElkaMainWindow", "&Exit"))
        self.action_Exit_2.setText(_translate("ElkaMainWindow", "&Help"))
        self.action_Exit_3.setText(_translate("ElkaMainWindow", "&Exit"))
        self.action_Undo.setText(_translate("ElkaMainWindow", "&Undo"))
        self.action_Redo.setText(_translate("ElkaMainWindow", "&Redo"))
        self.action_Cut.setText(_translate("ElkaMainWindow", "&Cut"))
        self.action_Paste.setText(_translate("ElkaMainWindow", "&Copy"))
        self.action_Paste_2.setText(_translate("ElkaMainWindow", "&Paste"))
        self.action_Joystick.setText(_translate("ElkaMainWindow", "&Joystick"))
        self.action_Keyboard.setText(_translate("ElkaMainWindow", "&Keyboard"))
        self.action_Help_Dialogs.setText(_translate("ElkaMainWindow", "&Help Dialogs"))
        self.actionProperties.setText(_translate("ElkaMainWindow", "Properties"))
        self.action_Start_Elka.setText(_translate("ElkaMainWindow", "&Start Elka"))
        self.action_Parse_Log.setText(_translate("ElkaMainWindow", "&Parse Log"))
        self.action_Save_Log.setText(_translate("ElkaMainWindow", "&Save Log"))
        self.action_Export_Data.setText(_translate("ElkaMainWindow", "&Export Data"))
        self.action_Plot_Data.setText(_translate("ElkaMainWindow", "&Plot Data"))
        self.actionProperties_2.setText(_translate("ElkaMainWindow", "Properties"))
        self.actionStart_Elka.setText(_translate("ElkaMainWindow", "Start Elka"))
        self.action_Stop_Elka.setText(_translate("ElkaMainWindow", "&Stop Elka"))
        self.action_Set_Gains.setText(_translate("ElkaMainWindow", "&Set Gains"))

