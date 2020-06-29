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

class exergyAnalysisDialog(QDialog):
    def __init__(self,fillData, editData=0, parent=None):
        super(exergyAnalysisDialog,self).__init__(parent)
        ui_file = QFile('exergyAnalysis/exergyAnalysisDataEntryDialog.ui')
        ui_file.open(QFile.ReadOnly)
        self.data = fillData
        self.widgetDict = defaultdict(list)
        self.editData = editData
        
        loader = QUiLoader()
        self.window = loader.load(ui_file) # self.window is ui
        
        self.tagName=["Process Parameters","Biomass Composition","Biochar Composition", "Bio-Oil Composition","Flue-gas Composition","Flue gas property Composition"]

        self.lineEditStartIndex = [2,0,0,0,0,0]
        
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
        
        ######################## Bio mass composition #############
        self.bmc_carbon_LE = self.window.lineEdit_17 
        self.bmc_hydrogen_LE = self.window.lineEdit_18 
        self.bmc_oxygen_LE = self.window.lineEdit_19 
        self.bmc_nitrogen_LE = self.window.lineEdit_20 
        self.bmc_sulpher_LE = self.window.lineEdit_23 
        self.bmc_phosphrous_LE = self.window.lineEdit_24 
        ######################## Bio char composition #############
        self.bcc_carbon_LE = self.window.lineEdit_25
        self.bcc_hydrogen_LE = self.window.lineEdit_26 
        self.bcc_oxygen_LE = self.window.lineEdit_27 
        self.bcc_nitrogen_LE = self.window.lineEdit_28 
        self.bcc_sulpher_LE = self.window.lineEdit_29 
        self.bcc_phosphrous_LE = self.window.lineEdit_30
        ######################## Bio-oil composition #############
        self.boc_carbon_LE = self.window.lineEdit_31 
        self.boc_hydrogen_LE = self.window.lineEdit_32 
        self.boc_oxygen_LE = self.window.lineEdit_33 
        self.boc_nitrogen_LE = self.window.lineEdit_34 
        self.boc_sulpher_LE = self.window.lineEdit_35 
        self.boc_phosphrous_LE = self.window.lineEdit_36 
        ################## Flue gas composition ###########
        self.fgc_co2_LE = self.window.lineEdit_37 
        self.fgc_ch4_LE = self.window.lineEdit_38 
        self.fgc_co_LE = self.window.lineEdit_39 
        self.fgc_sox_LE = self.window.lineEdit_40 
        self.fgc_nox_LE = self.window.lineEdit_41 
        self.fgc_pox_LE = self.window.lineEdit_42
        self.fgc_ppe_LE = self.window.lineEdit_43
        ################## Flue gas composition ###########
        self.fgpc_pt_LE = self.window.lineEdit_44 
        self.fgpc_at_LE = self.window.lineEdit_45 
        self.fgpc_hpt_LE = self.window.lineEdit_46 
        self.fgpc_hat_LE = self.window.lineEdit_47 
        self.fgpc_spt_LE = self.window.lineEdit_48 
        self.fgpc_sat_LE = self.window.lineEdit_49
        
        # Buttons
        self.okButton = self.window.buttonBox.button(QDialogButtonBox.Ok)
        self.okCancel = self.window.buttonBox.button(QDialogButtonBox.Cancel)        
        self.entryValidation()
        
    def entryValidation(self):
        self.lineEditValidator = QtGui.QDoubleValidator(self, 0,999999999,4)
        self.lineEditValidator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        
        self.ps_feedsize_LE.setValidator(self.lineEditValidator)
        self.ps_feedamount_LE.setValidator(self.lineEditValidator)
        self.ps_temp_LE.setValidator(self.lineEditValidator)               
        self.ps_residensetime_LE.setValidator(self.lineEditValidator)
        self.ps_heatingrate_LE.setValidator(self.lineEditValidator)      
        ######################## Bio mass composition #############
        self.bmc_carbon_LE.setValidator(self.lineEditValidator)    
        self.bmc_hydrogen_LE.setValidator(self.lineEditValidator)   
        self.bmc_oxygen_LE.setValidator(self.lineEditValidator)   
        self.bmc_nitrogen_LE.setValidator(self.lineEditValidator)   
        self.bmc_sulpher_LE.setValidator(self.lineEditValidator)   
        self.bmc_phosphrous_LE.setValidator(self.lineEditValidator)   
        ######################## Bio char composition #############
        self.bcc_carbon_LE.setValidator(self.lineEditValidator)   
        self.bcc_hydrogen_LE.setValidator(self.lineEditValidator)   
        self.bcc_oxygen_LE.setValidator(self.lineEditValidator)   
        self.bcc_nitrogen_LE.setValidator(self.lineEditValidator)   
        self.bcc_sulpher_LE.setValidator(self.lineEditValidator)   
        self.bcc_phosphrous_LE.setValidator(self.lineEditValidator)   
        ######################## Bio-oil composition #############
        self.boc_carbon_LE.setValidator(self.lineEditValidator)   
        self.boc_hydrogen_LE.setValidator(self.lineEditValidator)   
        self.boc_oxygen_LE.setValidator(self.lineEditValidator)   
        self.boc_nitrogen_LE.setValidator(self.lineEditValidator)   
        self.boc_sulpher_LE.setValidator(self.lineEditValidator)   
        self.boc_phosphrous_LE.setValidator(self.lineEditValidator)   
        ################## Flue gas composition ###########
        self.fgc_co2_LE.setValidator(self.lineEditValidator)   
        self.fgc_ch4_LE.setValidator(self.lineEditValidator)   
        self.fgc_co_LE.setValidator(self.lineEditValidator)   
        self.fgc_sox_LE.setValidator(self.lineEditValidator)   
        self.fgc_nox_LE.setValidator(self.lineEditValidator)   
        self.fgc_pox_LE.setValidator(self.lineEditValidator)   
        self.fgc_ppe_LE.setValidator(self.lineEditValidator)   
        ################## Flue gas composition ###########
        self.fgpc_pt_LE.setValidator(self.lineEditValidator)  
        self.fgpc_at_LE.setValidator(self.lineEditValidator)  
        self.fgpc_hpt_LE.setValidator(self.lineEditValidator)  
        self.fgpc_hat_LE.setValidator(self.lineEditValidator)  
        self.fgpc_spt_LE.setValidator(self.lineEditValidator)  
        self.fgpc_sat_LE.setValidator(self.lineEditValidator)  
        
        ################## add to dict ######################
        self.widgetDict[self.tagName[0]].append(self.ps_productsystem_CB)
        self.widgetDict[self.tagName[0]].append(self.ps_feedtype_CB)
        self.widgetDict[self.tagName[0]].append(self.ps_feedsize_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_feedamount_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_temp_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_residensetime_LE)
        self.widgetDict[self.tagName[0]].append(self.ps_heatingrate_LE)
        ######################## Bio mass composition #############
        self.widgetDict[self.tagName[1]].append(self.bmc_carbon_LE)
        self.widgetDict[self.tagName[1]].append(self.bmc_hydrogen_LE)
        self.widgetDict[self.tagName[1]].append(self.bmc_oxygen_LE)
        self.widgetDict[self.tagName[1]].append(self.bmc_nitrogen_LE)
        self.widgetDict[self.tagName[1]].append(self.bmc_sulpher_LE)
        self.widgetDict[self.tagName[1]].append(self.bmc_phosphrous_LE)
        ######################## Bio char composition #############
        self.widgetDict[self.tagName[2]].append(self.bcc_carbon_LE)
        self.widgetDict[self.tagName[2]].append(self.bcc_hydrogen_LE)
        self.widgetDict[self.tagName[2]].append(self.bcc_oxygen_LE) 
        self.widgetDict[self.tagName[2]].append(self.bcc_nitrogen_LE)
        self.widgetDict[self.tagName[2]].append(self.bcc_sulpher_LE)
        self.widgetDict[self.tagName[2]].append(self.bcc_phosphrous_LE)
        ######################## Bio-oil composition #############
        self.widgetDict[self.tagName[3]].append(self.boc_carbon_LE)
        self.widgetDict[self.tagName[3]].append(self.boc_hydrogen_LE)
        self.widgetDict[self.tagName[3]].append(self.boc_oxygen_LE)
        self.widgetDict[self.tagName[3]].append(self.boc_nitrogen_LE)
        self.widgetDict[self.tagName[3]].append(self.boc_sulpher_LE)
        self.widgetDict[self.tagName[3]].append(self.boc_phosphrous_LE)
        ################## Flue gas composition ###########
        self.widgetDict[self.tagName[4]].append(self.fgc_co2_LE)
        self.widgetDict[self.tagName[4]].append(self.fgc_ch4_LE)
        self.widgetDict[self.tagName[4]].append(self.fgc_co_LE)
        self.widgetDict[self.tagName[4]].append(self.fgc_sox_LE)
        self.widgetDict[self.tagName[4]].append(self.fgc_nox_LE)
        self.widgetDict[self.tagName[4]].append(self.fgc_pox_LE)
        self.widgetDict[self.tagName[4]].append(self.fgc_ppe_LE) 
        ################## Flue gas composition ###########
        self.widgetDict[self.tagName[5]].append(self.fgpc_pt_LE)
        self.widgetDict[self.tagName[5]].append(self.fgpc_at_LE)
        self.widgetDict[self.tagName[5]].append(self.fgpc_hpt_LE)
        self.widgetDict[self.tagName[5]].append(self.fgpc_hat_LE)
        self.widgetDict[self.tagName[5]].append(self.fgpc_spt_LE)
        self.widgetDict[self.tagName[5]].append(self.fgpc_sat_LE)
    
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
