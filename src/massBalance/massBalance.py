# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 02:28:03 2020

@author: spark
"""

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QObject
from PySide2.QtGui import QStandardItemModel, QStandardItem
from massBalance.massBalanceDialog import massBalanceDialog

import rc_appMainGui
from collections import defaultdict

class massBalanceWindow(QObject):
    def __init__(self, dataPoints=[], parent=None):
        super(massBalanceWindow,self).__init__(parent)
        ui_file = QFile('massBalance/massBalance.ui')
        ui_file.open(QFile.ReadOnly)
        
        loader = QUiLoader()
        self.window = loader.load(ui_file) # self.window is ui
        
        self.tagNameDict=defaultdict(list)
        self.dataPoints = dataPoints   # list of all entered data in form of ditionary
        self.tagName=["Process Parameters","Input","Output","MBC"]
        self.noOfAddedData = len(self.dataPoints)#0  # no of added data, 1 for 1 data
        self.sendData=defaultdict(list)
        self.receivedData=defaultdict(list)
        
        self.createwidgets()
        self.createTagNameDict()
        
        ui_file.close()
        
    def showWindow(self):
        #self.window.show()
        self.window.showMaximized() 
        self.updateTreeView()
    def closeWindow(self):
        self.window.close()
        
    def createTagNameDict(self):
        self.tagNameDict[self.tagName[0]].append("Product System")
        self.tagNameDict[self.tagName[0]].append("Feed Type")
        self.tagNameDict[self.tagName[0]].append("Feed Size(mm)")
        self.tagNameDict[self.tagName[0]].append("Feed Amaount(kg)")
        self.tagNameDict[self.tagName[0]].append("Temp(C)")
        self.tagNameDict[self.tagName[0]].append("Residense Time(min) ")
        self.tagNameDict[self.tagName[0]].append("Heating rate(C/min)")
        
        self.tagNameDict[self.tagName[1]].append("Biomass (kg)")
        self.tagNameDict[self.tagName[1]].append("Inert gases (kg)")
        self.tagNameDict[self.tagName[1]].append("Total (kg)")
        
        self.tagNameDict[self.tagName[2]].append("Biochar (kg)")
        self.tagNameDict[self.tagName[2]].append("Bio-Oil (kg)")
        self.tagNameDict[self.tagName[2]].append("Gases amount (kg)")
        self.tagNameDict[self.tagName[2]].append("Total (kg)")
        
        self.tagNameDict[self.tagName[3]].append("Mass Balance Closure (MBC)")
        
    def createDataDictForEntry(self,addEditIndex=0):
        self.sendData.clear()
        if(addEditIndex>self.noOfAddedData):
            for tn in self.tagName:  # add new data
                for i in range(len(self.tagNameDict[tn])):
                    self.sendData[tn].append("0.0")
        else:  # editing data
            self.sendData = self.dataPoints[addEditIndex-1].copy()  # addEditIndex start from 1 where as data index from o

        
    def createwidgets(self):
        self.sampleDataNo_CB = self.window.comboBox
        self.addEditButton_PB = self.window.pushButton
        self.dataTreeView = self.window.treeView
        self.run_PB = self.window.pushButton_2
        
        self.sampleDataNo_CB.addItems([str(i) for i in range(1,self.noOfAddedData+2)]) 
        
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
        if(addEditIndex>self.noOfAddedData): # add new
            massBalanceDialogWindow = massBalanceDialog(self.sendData)
        else: # edit 
            massBalanceDialogWindow = massBalanceDialog(self.sendData, editData=1) 
        
        def getValue():
            massBalanceDialogWindow.fetchData()
            self.receivedData = massBalanceDialogWindow.data.copy()
                                  
            if(addEditIndex>self.noOfAddedData): # new data was added
                # update drop don
                self.noOfAddedData = self.noOfAddedData+1
                self.sampleDataNo_CB.clear()
                self.sampleDataNo_CB.addItems([str(i) for i in range(self.noOfAddedData+1,0,-1)])
                #update data list
                self.dataPoints.append(self.receivedData)
            else: # data was modified
                self.dataPoints[addEditIndex -1] = self.receivedData # -1 because list starts from 0
                
            self.updateTreeView()
            
        massBalanceDialogWindow.okButton.clicked.connect(getValue)
        massBalanceDialogWindow.showWindow()
            
        
            
            
        