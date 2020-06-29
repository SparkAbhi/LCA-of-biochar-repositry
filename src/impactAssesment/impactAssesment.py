# -*- coding: utf-8 -*-
"""
Created on Sun May 31 12:18:47 2020

@author: spark
"""
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QObject, Qt
from PySide2 import QtGui
from PySide2.QtWidgets import QMessageBox
import rc_appMainGui
from collections import defaultdict

class impactAssesmentWindow(QObject):
    def __init__(self,data, parent=None):
        super(impactAssesmentWindow,self).__init__(parent)
        ui_file = QFile('impactAssesment/impactAssesment.ui')
        ui_file.open(QFile.ReadOnly)
        
        loader = QUiLoader()
        self.window = loader.load(ui_file) # self.window is ui
        
        self.data = data  # one element array
        self.tagName=["Process Parameters","Energy","Pyrolysis Products", "Emissions", "EA sampleNo and Assesment method"]
        self.lineEditStartIndex = [2,1,0,0,1]
        self.widgetDict = defaultdict(list)
        
        self.createwidgets()
        
        self.fillDataToEntry()
                
        ui_file.close()
        
    def showWindow(self):
        #self.window.show()
        self.window.showMaximized()
    def showMessageBox(self, text):
        infoMsgBox = QMessageBox()
        infoMsgBox.setText(text)
        infoMsgBox.exec_()
        
    def closeWindow(self):
        self.window.close()
        
        
    def createwidgets(self):
        self.energyAnalysisSampleNo_LE = self.window.lineEdit_28
        ####################### product systems #######################
        self.ps_productsystem_CB = self.window.comboBox_2
        self.ps_feedtype_CB = self.window.comboBox_3
        self.ps_feedsize_LE = self.window.lineEdit_21
        self.ps_feedamount_LE = self.window.lineEdit_22
        self.ps_temp_LE = self.window.lineEdit
        self.ps_residensetime_LE = self.window.lineEdit_2
        self.ps_heatingrate_LE = self.window.lineEdit_3      

        ######################composition bio char, bio oil, flue gas ####################################
        self.comp_bc_carbon_LE = self.window.lineEdit_4
        self.comp_bc_nitrogen_LE = self.window.lineEdit_5
        self.comp_bc_sulphur_LE = self.window.lineEdit_6
        self.comp_bc_phos_LE = self.window.lineEdit_26
        self.comp_bc_heavymetals_LE = self.window.lineEdit_27
        
        self.comp_bo_hydrocarbon_LE = self.window.lineEdit_7
        self.comp_bo_pofour_LE = self.window.lineEdit_23
        self.comp_bo_nothree_LE = self.window.lineEdit_24
        self.comp_bo_sofour_LE = self.window.lineEdit_25
        
        self.comp_fg_ch4_LE = self.window.lineEdit_8
        self.comp_fg_co2_LE = self.window.lineEdit_9
        self.comp_fg_co_LE = self.window.lineEdit_10
        self.comp_fg_nox_LE = self.window.lineEdit_11
        self.comp_fg_sox_LE = self.window.lineEdit_12
        self.comp_fg_h2s_LE = self.window.lineEdit_13
        ######################## products #####################################
        self.pd_biochar_LE = self.window.lineEdit_14
        self.pd_biooil_LE = self.window.lineEdit_15
        self.pd_fluegas_LE = self.window.lineEdit_16
        
        self.pd_biochar_HHV_LE = self.window.lineEdit_29
        self.pd_biooil_HHV_LE = self.window.lineEdit_35
        self.pd_fluegas_HHV_LE = self.window.lineEdit_32
        
        self.pd_biochar_LHV_LE = self.window.lineEdit_30
        self.pd_biooil_LHV_LE = self.window.lineEdit_33
        self.pd_fluegas_LHV_LE = self.window.lineEdit_36
        
        self.pd_biochar_EV_LE = self.window.lineEdit_31
        self.pd_biooil_EV_LE = self.window.lineEdit_34
        self.pd_fluegas_EV_LE = self.window.lineEdit_37
        
        ######################### energy consumption###############################
        self.ec_energy_type_CB = self.window.comboBox_4
        self.ec_energy_value_LE = self.window.lineEdit_17
        self.ec_energyrecoveryfrombiooil_LE = self.window.lineEdit_18
        self.ec_energyrecoveryfromfluegases_LE = self.window.lineEdit_19
        self.ec_netenergyconsumption_LE = self.window.lineEdit_20
        ##################  plots ####################

        ################# run#########################
        self.assesmentmethod_CB = self.window.comboBox
        self.run_PB = self.window.pushButton
        
        ######### energy auto fill##############       
        self.ec_energy_value_LE.editingFinished.connect(self.fillNetEnergyConsumption)
        self.ec_energyrecoveryfrombiooil_LE.editingFinished.connect(self.fillNetEnergyConsumption)
        self.ec_energyrecoveryfromfluegases_LE.editingFinished.connect(self.fillNetEnergyConsumption)
        
        
        ########### double Validator for line edit#############
        self.entryValidation()
        
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
        
    def entryValidation(self):
        self.lineEditValidator = QtGui.QDoubleValidator(self, 0,999999999,4)
        self.lineEditValidator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        
        self.energyAnalysisSampleNo_LE.setValidator(self.lineEditValidator)
        self.ps_feedsize_LE.setValidator(self.lineEditValidator)
        self.ps_feedamount_LE.setValidator(self.lineEditValidator)
        #self.ps_temp_LE.setValidator(self.lineEditValidator)        
        self.ps_temp_LE.setValidator(self.lineEditValidator)
        self.ps_residensetime_LE.setValidator(self.lineEditValidator)
        self.ps_heatingrate_LE.setValidator(self.lineEditValidator)
        self.comp_bc_carbon_LE.setValidator(self.lineEditValidator)
        self.comp_bc_nitrogen_LE.setValidator(self.lineEditValidator)
        self.comp_bc_sulphur_LE.setValidator(self.lineEditValidator)         
        self.comp_bc_phos_LE.setValidator(self.lineEditValidator) 
        self.comp_bc_heavymetals_LE.setValidator(self.lineEditValidator)        
        self.comp_bo_hydrocarbon_LE.setValidator(self.lineEditValidator) 
        self.comp_bo_pofour_LE.setValidator(self.lineEditValidator) 
        self.comp_bo_nothree_LE.setValidator(self.lineEditValidator)  
        self.comp_bo_sofour_LE.setValidator(self.lineEditValidator)       
        self.comp_fg_ch4_LE.setValidator(self.lineEditValidator)
        self.comp_fg_co2_LE.setValidator(self.lineEditValidator)
        self.comp_fg_co_LE.setValidator(self.lineEditValidator)
        self.comp_fg_nox_LE.setValidator(self.lineEditValidator)
        self.comp_fg_sox_LE.setValidator(self.lineEditValidator)
        self.comp_fg_h2s_LE.setValidator(self.lineEditValidator)
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
        self.ec_energy_value_LE.setValidator(self.lineEditValidator)
        self.ec_energyrecoveryfrombiooil_LE.setValidator(self.lineEditValidator)
        self.ec_energyrecoveryfromfluegases_LE.setValidator(self.lineEditValidator)
        self.ec_netenergyconsumption_LE.setValidator(self.lineEditValidator)
        
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
        
        self.widgetDict[self.tagName[3]].append(self.comp_bc_carbon_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_bc_nitrogen_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_bc_sulphur_LE)         
        self.widgetDict[self.tagName[3]].append(self.comp_bc_phos_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_bc_heavymetals_LE)        
        self.widgetDict[self.tagName[3]].append(self.comp_bo_hydrocarbon_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_bo_pofour_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_bo_nothree_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_bo_sofour_LE)        
        self.widgetDict[self.tagName[3]].append(self.comp_fg_ch4_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_fg_co2_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_fg_co_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_fg_nox_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_fg_sox_LE)
        self.widgetDict[self.tagName[3]].append(self.comp_fg_h2s_LE)
 
        self.widgetDict[self.tagName[4]].append(self.assesmentmethod_CB)
        self.widgetDict[self.tagName[4]].append(self.energyAnalysisSampleNo_LE)
        
    def fillDataToEntry(self): 
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
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
        