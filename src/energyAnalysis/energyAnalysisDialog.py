# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 08:16:14 2020

@author: spark
"""
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt
from PySide2.QtWidgets import QDialog, QDialogButtonBox
from PySide2 import QtGui
from collections import defaultdict

class energyAnalysisDialog(QDialog):
    def __init__(self,fillData, editData=0, parent=None):
        super(energyAnalysisDialog,self).__init__(parent)
        ui_file = QFile('energyAnalysis/energyAnalysisDataEntryDialog.ui')
        ui_file.open(QFile.ReadOnly)
        self.data = fillData
        self.widgetDict = defaultdict(list)
        self.editData = editData
        
        loader = QUiLoader()
        self.window = loader.load(ui_file) # self.window is ui
        
        self.tagName=["Process Parameters","Energy","Pyrolysis Products"]
        self.lineEditStartIndex = [2,1,0]
        
        self.createwidgets()
        self.fillDataToEntry()
        
        ui_file.close()
        
    def showWindow(self):
        #self.window.show()
        self.window.showMaximized()
        
    def createwidgets(self):
         ####################### product systems #######################
        self.ps_productsystem_CB = self.window.comboBox_2
        self.ps_feedtype_CB = self.window.comboBox_3
        self.ps_feedsize_LE = self.window.lineEdit_21
        self.ps_feedamount_LE = self.window.lineEdit_22
        self.ps_temp_LE = self.window.lineEdit
        self.ps_residensetime_LE = self.window.lineEdit_2
        self.ps_heatingrate_LE = self.window.lineEdit_3      

        self.ec_energy_type_CB = self.window.comboBox_4
        self.ec_energy_value_LE = self.window.lineEdit_17
        self.ec_energyrecoveryfrombiooil_LE = self.window.lineEdit_18
        self.ec_energyrecoveryfromfluegases_LE = self.window.lineEdit_19
        self.ec_netenergyconsumption_LE = self.window.lineEdit_20
        ######################## products #####################################
        self.pd_biochar_LE = self.window.lineEdit_34
        self.pd_biochar_HHV_LE = self.window.lineEdit_37
        self.pd_biochar_LHV_LE = self.window.lineEdit_40
        self.pd_biochar_EV_LE = self.window.lineEdit_43
        
        self.pd_biooil_LE = self.window.lineEdit_35
        self.pd_biooil_HHV_LE = self.window.lineEdit_38
        self.pd_biooil_LHV_LE = self.window.lineEdit_41
        self.pd_biooil_EV_LE = self.window.lineEdit_44
        
        self.pd_fluegas_LE = self.window.lineEdit_36
        self.pd_fluegas_HHV_LE = self.window.lineEdit_39
        self.pd_fluegas_LHV_LE = self.window.lineEdit_42
        self.pd_fluegas_EV_LE = self.window.lineEdit_45
        
        # Buttons
        self.okButton = self.window.buttonBox.button(QDialogButtonBox.Ok)
        self.okCancel = self.window.buttonBox.button(QDialogButtonBox.Cancel)
        
        ######### energy auto fill##############       
        self.ec_energy_value_LE.editingFinished.connect(self.fillNetEnergyConsumption)
        self.ec_energyrecoveryfrombiooil_LE.editingFinished.connect(self.fillNetEnergyConsumption)
        self.ec_energyrecoveryfromfluegases_LE.editingFinished.connect(self.fillNetEnergyConsumption)
        
        self.entryValidation()
        
    def entryValidation(self):
        self.lineEditValidator = QtGui.QDoubleValidator(self, 0,999999999,4)
        self.lineEditValidator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        
        self.ps_feedsize_LE.setValidator(self.lineEditValidator)
        self.ps_feedamount_LE.setValidator(self.lineEditValidator)
        self.ps_temp_LE.setValidator(self.lineEditValidator)               
        self.ps_residensetime_LE.setValidator(self.lineEditValidator)
        self.ps_heatingrate_LE.setValidator(self.lineEditValidator)
        
        self.ec_energy_value_LE.setValidator(self.lineEditValidator)
        self.ec_energyrecoveryfrombiooil_LE.setValidator(self.lineEditValidator)
        self.ec_energyrecoveryfromfluegases_LE.setValidator(self.lineEditValidator)
        self.ec_netenergyconsumption_LE.setValidator(self.lineEditValidator)
 
        self.pd_biochar_LE.setValidator(self.lineEditValidator)
        self.pd_biooil_LE.setValidator(self.lineEditValidator)
        self.pd_fluegas_LE.setValidator(self.lineEditValidator)
        self.pd_biochar_HHV_LE.setValidator(self.lineEditValidator)
        self.pd_biooil_HHV_LE.setValidator(self.lineEditValidator)
        self.pd_fluegas_HHV_LE.setValidator(self.lineEditValidator)
        self.pd_biochar_LHV_LE.setValidator(self.lineEditValidator)
        self.pd_biooil_LHV_LE.setValidator(self.lineEditValidator)
        self.pd_fluegas_LHV_LE.setValidator(self.lineEditValidator)
        self.pd_biochar_EV_LE.setValidator(self.lineEditValidator)
        self.pd_biooil_EV_LE.setValidator(self.lineEditValidator)
        self.pd_fluegas_EV_LE.setValidator(self.lineEditValidator)
        
        
        ################## add to lineEdit List ######################
        self.widgetDict[self.tagName[0]].append(self.ps_productsystem_CB)
        self.widgetDict[self.tagName[0]].append(self.ps_feedtype_CB)
        self.widgetDict[self.tagName[0]].append(self.ps_feedsize_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_feedamount_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_temp_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_residensetime_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_heatingrate_LE)
        
        
        self.widgetDict[self.tagName[1]].append(self.ec_energy_type_CB)
        self.widgetDict[self.tagName[1]].append(self.ec_energy_value_LE)
        self.widgetDict[self.tagName[1]].append(self.ec_energyrecoveryfrombiooil_LE)
        self.widgetDict[self.tagName[1]].append(self.ec_energyrecoveryfromfluegases_LE)
        self.widgetDict[self.tagName[1]].append(self.ec_netenergyconsumption_LE)

        self.widgetDict[self.tagName[2]].append(self.pd_biochar_LE)
        self.widgetDict[self.tagName[2]].append(self.pd_biochar_HHV_LE)
        self.widgetDict[self.tagName[2]].append(self.pd_biochar_LHV_LE)
        self.widgetDict[self.tagName[2]].append(self.pd_biochar_EV_LE)
        
        self.widgetDict[self.tagName[2]].append(self.pd_biooil_LE)
        self.widgetDict[self.tagName[2]].append(self.pd_biooil_HHV_LE)
        self.widgetDict[self.tagName[2]].append(self.pd_biooil_LHV_LE)
        self.widgetDict[self.tagName[2]].append(self.pd_biooil_EV_LE)
        
        self.widgetDict[self.tagName[2]].append(self.pd_fluegas_LE)
        self.widgetDict[self.tagName[2]].append(self.pd_fluegas_HHV_LE)
        self.widgetDict[self.tagName[2]].append(self.pd_fluegas_LHV_LE)
        self.widgetDict[self.tagName[2]].append(self.pd_fluegas_EV_LE)

        
    def fillNetEnergyConsumption(self):
        energyvalue=0
        biooilvalue=0
        fluegasvalue=0
        if(self.ec_energy_value_LE.text()!=""):
            energyvalue = float(self.ec_energy_value_LE.text())
        if(self.ec_energyrecoveryfrombiooil_LE.text()!=""):
            biooilvalue = float(self.ec_energyrecoveryfrombiooil_LE.text())
        if(self.ec_energyrecoveryfromfluegases_LE.text()!=""):
            fluegasvalue = float(self.ec_energyrecoveryfromfluegases_LE.text())
        
        netEnergyConsumption = energyvalue - biooilvalue - fluegasvalue
        self.ec_netenergyconsumption_LE.setText(str(netEnergyConsumption))
    
    def fillDataToEntry(self):    
        if(self.editData==1):
            for i in range(len(self.tagName)):
                for j in range(self.lineEditStartIndex[i]):                
                    setIndex = self.widgetDict[self.tagName[i]][j].findText(self.data[self.tagName[i]][j],flags=Qt.MatchExactly)
                    self.widgetDict[self.tagName[i]][j].setCurrentIndex(setIndex)
                 
            for i in range(len(self.tagName)):
                for j in range(self.lineEditStartIndex[i], len(self.widgetDict[self.tagName[i]]), 1):
                    self.widgetDict[self.tagName[i]][j].setText(self.data[self.tagName[i]][j])
            
                
    def fetchData(self):
        for i in range(len(self.tagName)):
            for j in range(self.lineEditStartIndex[i]):
                self.data[self.tagName[i]][j] = self.widgetDict[self.tagName[i]][j].currentText()
                 
        for i in range(len(self.tagName)):
            for j in range(self.lineEditStartIndex[i], len(self.widgetDict[self.tagName[i]]), 1):
                self.data[self.tagName[i]][j] = self.widgetDict[self.tagName[i]][j].text()
