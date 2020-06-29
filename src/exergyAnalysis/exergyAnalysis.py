# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 02:28:03 2020

@author: spark
"""

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QObject
from PySide2.QtGui import QStandardItemModel, QStandardItem
from exergyAnalysis.exergyAnalysisDialog import exergyAnalysisDialog
import rc_appMainGui
from collections import defaultdict

class exergyAnalysisWindow(QObject):
    def __init__(self, dataPoints=[], blankDataLen=0, parent=None):
        super(exergyAnalysisWindow,self).__init__(parent)
        ui_file = QFile('exergyAnalysis/exergyAnalysis.ui')
        ui_file.open(QFile.ReadOnly)
        
        loader = QUiLoader()
        self.window = loader.load(ui_file) # self.window is ui
        
        self.tagNameDict=defaultdict(list)
        self.dataPoints = dataPoints   # list of all entered data in form of ditionary
        self.tagName=["Process Parameters","Biomass Composition","Biochar Composition", "Bio-Oil Composition","Flue-gas Composition","Flue gas property Composition"]
        self.noOfAddedData = len(self.dataPoints)#0  # no of added data, 1 for 1 data
        self.sendData=defaultdict(list)
        self.receivedData=defaultdict(list)
        
        self.createwidgets()
        self.createTagNameDict()
        
        self.updateDataPointsFromProcessParameters(blankLength = blankDataLen)
        
        ui_file.close()
        
    def showWindow(self):
        #self.window.show()
        self.window.showMaximized()
        self.updateTreeView()
    def closeWindow(self):
        self.window.close()
        
    def updateDataPointsFromProcessParameters(self, blankLength=0):
        tempdict=defaultdict(list)
        for i in range(self.noOfAddedData-blankLength, self.noOfAddedData, 1):
            pp_arr = self.dataPoints[i].copy()
            tempdict.clear()
            tempdict[self.tagName[0]] = pp_arr
                 
            tempdict[self.tagName[1]] = [""for k in range(len( self.tagNameDict[self.tagName[1]]))]
            
            tempdict[self.tagName[2]] = [""for k in range(len( self.tagNameDict[self.tagName[2]]))]
            tempdict[self.tagName[3]] = [""for k in range(len( self.tagNameDict[self.tagName[3]]))]
            tempdict[self.tagName[4]] = [""for k in range(len( self.tagNameDict[self.tagName[4]]))]
            tempdict[self.tagName[5]] = [""for k in range(len( self.tagNameDict[self.tagName[5]]))] 
            
            self.dataPoints[i]=tempdict.copy()
                 
    def createTagNameDict(self):
        self.tagNameDict[self.tagName[0]].append("Product System")
        self.tagNameDict[self.tagName[0]].append("Feed Type")
        self.tagNameDict[self.tagName[0]].append("Feed Size(mm)")
        self.tagNameDict[self.tagName[0]].append("Feed Amaount(kg)")
        self.tagNameDict[self.tagName[0]].append("Temp(C)")
        self.tagNameDict[self.tagName[0]].append("Residense Time(min) ")
        self.tagNameDict[self.tagName[0]].append("Heating rate(C/min)")
        
        self.tagNameDict[self.tagName[1]].append("Carbon (kg)")
        self.tagNameDict[self.tagName[1]].append("Hydrogen (kg)")
        self.tagNameDict[self.tagName[1]].append("Oxygen (kg)")
        self.tagNameDict[self.tagName[1]].append("Nitogen (kg)")
        self.tagNameDict[self.tagName[1]].append("Sulpher (kg)")
        self.tagNameDict[self.tagName[1]].append("Phosphrous (kg)")
        
        self.tagNameDict[self.tagName[2]].append("Carbon (kg)")
        self.tagNameDict[self.tagName[2]].append("Hydrogen (kg)")
        self.tagNameDict[self.tagName[2]].append("Oxygen (kg)")
        self.tagNameDict[self.tagName[2]].append("Nitogen (kg)")
        self.tagNameDict[self.tagName[2]].append("Sulpher (kg)")
        self.tagNameDict[self.tagName[2]].append("Phosphrous (kg)")
        
        self.tagNameDict[self.tagName[3]].append("Carbon (kg)")
        self.tagNameDict[self.tagName[3]].append("Hydrogen (kg)")
        self.tagNameDict[self.tagName[3]].append("Oxygen (kg)")
        self.tagNameDict[self.tagName[3]].append("Nitogen (kg)")
        self.tagNameDict[self.tagName[3]].append("Sulpher (kg)")
        self.tagNameDict[self.tagName[3]].append("Phosphrous (kg)")
              
        self.tagNameDict[self.tagName[4]].append("Carbon dioxide (kg)")
        self.tagNameDict[self.tagName[4]].append("Methane (kg)")
        self.tagNameDict[self.tagName[4]].append("Carbon mono-oxide (kg)")
        self.tagNameDict[self.tagName[4]].append("Oxides of Sulpher (kg)")
        self.tagNameDict[self.tagName[4]].append("Oxides of Nitrogen (kg)")
        self.tagNameDict[self.tagName[4]].append("Oxides of Phosphrous (kg)")
        self.tagNameDict[self.tagName[4]].append("Pyrolysis (Process) Energy (MJ)")
        
        self.tagNameDict[self.tagName[5]].append("Process temp [T] (K)")
        self.tagNameDict[self.tagName[5]].append("Ambient temp [To] (K)")
        self.tagNameDict[self.tagName[5]].append("Enthalpy at process temp [h] (J)")
        self.tagNameDict[self.tagName[5]].append("Enthalpy at ambient temp [ho] (J)")
        self.tagNameDict[self.tagName[5]].append("Entropy at process temp [S] (J/K)")
        self.tagNameDict[self.tagName[5]].append("Entropy at ambient temp [So] (J/K)")
        
        
    def createDataDictForEntry(self,addEditIndex=0):
        self.sendData.clear()
        self.sendData = self.dataPoints[addEditIndex-1].copy()  # addEditIndex start from 1 where as data index from o

        
    def createwidgets(self):
        self.sampleDataNo_CB = self.window.comboBox
        self.addEditButton_PB = self.window.pushButton
        self.dataTreeView = self.window.treeView
        self.run_PB = self.window.pushButton_2
        
        self.sampleDataNo_CB.addItems([str(i) for i in range(1,self.noOfAddedData+1)]) 
        
        self.addEditButton_PB.clicked.connect(self.addEditData)
    
        self.model = QStandardItemModel()
        self.dataTreeView.setModel(self.model)
        self.dataTreeView.setUniformRowHeights(True)
            
    def updateTreeView(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.tagName)
        
        for i in range(self.noOfAddedData):
            parent1 = QStandardItem('Samle No {}.'.format(i+1))  # sample no 1,2,3,----
            showThisData = self.dataPoints[i]
            maximumIteam = max(len(self.tagNameDict[self.tagName[0]]),len(self.tagNameDict[self.tagName[1]]),len(self.tagNameDict[self.tagName[2]]))

            for j in range(maximumIteam):
                currentRow=[]
                for tn in self.tagName:
                    if(j<len(self.tagNameDict[tn])):  # because 0 to len-1
                        x=str(self.tagNameDict[tn][j])
                        y=str(showThisData[tn][j])
                        child =QStandardItem((x+': {}').format(y))
                    else:
                        child =QStandardItem("")                        
                    currentRow.append(child)
                parent1.appendRow(currentRow)
            self.model.appendRow(parent1)
        
    def addEditData(self):
        addEditIndex = int(self.sampleDataNo_CB.currentText())
        self.createDataDictForEntry(addEditIndex)   
        ######## launch add data dialog and send current data##########
        exergyAnalysisDialogWindow = exergyAnalysisDialog(self.sendData, editData=1)  # only data can be edited by filling blank spots
        
        def getValue():
            exergyAnalysisDialogWindow.fetchData()
            self.receivedData = exergyAnalysisDialogWindow.data.copy()                              
            self.dataPoints[addEditIndex -1] = self.receivedData # -1 because list starts from 0             
            self.updateTreeView()
            
        exergyAnalysisDialogWindow.okButton.clicked.connect(getValue)
        exergyAnalysisDialogWindow.showWindow()
            
        
            
            
        