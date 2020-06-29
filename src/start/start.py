# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 09:12:15 2020

@author: spark
"""
from os import path, makedirs
import sqlite3
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QObject
from PySide2.QtWidgets import QMessageBox, QFileDialog
import json
from collections import defaultdict

from massBalance.massBalance import massBalanceWindow
from exergyAnalysis.exergyAnalysis import exergyAnalysisWindow
from energyAnalysis.energyAnalysis import energyAnalysisWindow
from impactAssesment.impactAssesment import impactAssesmentWindow


class startAppWindow(QObject):
    def __init__(self, parent=None):
        super(startAppWindow,self).__init__(parent)
        ui_file = QFile('start/start.ui')
        ui_file.open(QFile.ReadOnly)
        
        loader = QUiLoader()
        self.window = loader.load(ui_file) # self.window is ui
        
        ############datas for analysis actions########
        self.massBalanceDataPoints=[]
        self.exergyAnalysisDataPoints=[]
        self.energyAnalysisDataPoints=[]
        self.energyAnalysisSampleNo=0
        self.impactAnalysisDataPoints=[]
        self.processParametersData=[]
        ######################
        self.projectName =""
        self.resultLocation=""
        
        ####################
        
        self.createwidgets()
        
        #self.__fileName = path.join('start/mainDatabase.db')
        self.__folderName = path.abspath(path.join("..\..\ProgramData\LCA of Biochar")) # for installation file in program Data
        self.__fileName =   path.join(self.__folderName, "mainDatabase.db") # for installation file in program Data
        self.createMainDB()
        self.__con = sqlite3.connect(self.__fileName)
        self.__cur = self.__con.cursor()
        self.loadProjectsName()
        
        ui_file.close()
        
    def showWindow(self):
        #self.window.show()
        self.window.showMaximized() 
    def showMessageBox(self, text):
        infoMsgBox = QMessageBox()
        infoMsgBox.setText(text)
        infoMsgBox.exec_()
        
    def createwidgets(self):
        self.createProject_LE = self.window.lineEdit
        self.loadProject_CB = self.window.comboBox
        self.resultLocation_LE = self.window.lineEdit_2
        self.saveProject_LE = self.window.lineEdit_3
        
        self.createProject_PB = self.window.pushButton
        self.loadProject_PB = self.window.pushButton_2
        self.resultLocation_PB = self.window.toolButton
        self.saveProject_PB = self.window.pushButton_3
        
        self.createProject_PB.clicked.connect(self.createProject)
        self.loadProject_PB.clicked.connect(self.loadProject)
        self.resultLocation_PB.clicked.connect(self.getResultLocation)
        self.saveProject_PB.clicked.connect(self.saveProject)
    
        self.massBalanceMenu  = self.window.actionMass_Balance
        self.exergyAnalysisMenu  = self.window.actionExergy_Analysis
        self.energyAnalysisMenu  = self.window.actionEnergy_Analysis
        self.impactAssesmentMenu  = self.window.actionImpact_Assesment
        
        self.massBalanceMenu.triggered.connect(self.massBalanceProcess) 
        self.exergyAnalysisMenu.triggered.connect(self.exergyAnalysisProcess) 
        self.energyAnalysisMenu.triggered.connect(self.energyAnalysisProcess) 
        self.impactAssesmentMenu.triggered.connect(self.impactAssesmentProcess)
        
    def createProject(self):
        if(self.createProject_LE.text() == ""):
            self.showMessageBox("Error: Please provide project name")
            return        
        self.projectName = self.createProject_LE.text()
        self.saveProject_LE.setText(self.projectName)
        self.massBalanceDataPoints=[]
        self.exergyAnalysisDataPoints=[]
        self.energyAnalysisDataPoints=[]
        self.energyAnalysisSampleNo=0
        self.impactAnalysisDataPoints=[]
        self.processParametersData=[]
        createSql ="insert into PROJECTS(\
                    project_Name,massBalanceDataPoints,\
                    exergyAnalysisDataPoints,energyAnalysisDataPoints,impactAnalysisDataPoints)\
                    values(?,?,?,?,?)"
        try:
            self.__cur.execute(createSql,(self.projectName,
                                          json.dumps(self.massBalanceDataPoints),
                                          json.dumps(self.exergyAnalysisDataPoints),
                                          json.dumps(self.energyAnalysisDataPoints),
                                          json.dumps(self.impactAnalysisDataPoints),))
            self.__con.commit()
            self.loadProjectsName()
        except sqlite3.Error as e:
            self.showMessageBox("Unable to create "+self.projectName+", error is "+ e.args[0])
        
    def getResultLocation(self):         
        self.resultLocation = str(QFileDialog().getExistingDirectory(caption ="Select directory to save results",
                                       options = QFileDialog.ShowDirsOnly| QFileDialog.DontResolveSymlinks))
        
        self.resultLocation_LE.clear()
        self.resultLocation_LE.setText(self.resultLocation)
    
    
    def loadProjectsName(self):
        ############## get list of configurations #################
        loadSql = "select project_Name from PROJECTS"
        savedProjectsList=[]
        try:
            self.__cur.execute(loadSql)
            rows = self.__cur.fetchall()
            for i in range(len(rows)):
                savedProjectsList.append(rows[i][0])
            #print(savedConfigurationList)
        except sqlite3.Error as e:
            print("loaing error for projects list  " + e.args[0])
        
        self.loadProject_CB.clear()
        self.loadProject_CB.addItems(savedProjectsList)
        
    def loadProject(self):
        self.projectName = self.loadProject_CB.currentText()
        self.saveProject_LE.setText(self.projectName)
        if(self.projectName==""):
            self.showMessageBox("No project name, Please select a project to load or create blank project")
            return
        loadSql = "select * from PROJECTS where project_Name=?"
        try:
            self.__cur.execute(loadSql,(self.projectName,))
            rows = self.__cur.fetchall()
            self.massBalanceDataPoints = json.loads(rows[0][2])
            self.extractProcessParametersData()  # useful only if massBalance is done but not other 
            self.exergyAnalysisDataPoints= json.loads(rows[0][3])
            self.energyAnalysisDataPoints= json.loads(rows[0][4])
            self.impactAnalysisDataPoints= json.loads(rows[0][5])
            self.showMessageBox(self.projectName+" Loaded Successfully")
        except sqlite3.Error as e:
            self.showMessageBox("Unable to load "+self.projectName+", error is "+ e.args[0])
        
        
    def saveProject(self):
        if(self.projectName == ""):
            self.showMessageBox("Error: No current project exists, please create or load a project")
            return        
        saveSql ="update PROJECTS \
                    set massBalanceDataPoints=?,\
                        exergyAnalysisDataPoints=?,\
                        energyAnalysisDataPoints=?,\
                        impactAnalysisDataPoints=?\
                    where project_Name=? "
        try:           
            self.__cur.execute(saveSql,(json.dumps(self.massBalanceDataPoints),
                                          json.dumps(self.exergyAnalysisDataPoints),
                                          json.dumps(self.energyAnalysisDataPoints),
                                          json.dumps(self.impactAnalysisDataPoints),
                                          self.projectName,))
            self.__con.commit()
            self.showMessageBox("Saved "+self.projectName+" successfully")
        except sqlite3.Error as e:
            self.showMessageBox("Unable to save "+self.projectName+", error is "+ e.args[0])
    def createMainDB(self):
        if(path.exists(self.__fileName)):
            return
        else: 
            try:
                if not path.isdir(self.__folderName ):
                    makedirs(self.__folderName)
            except:
                self.showMessageBox("Unable to craete Program Data folder")
                return               
            try:   
                con = sqlite3.connect(self.__fileName)
                cur = con.cursor()
                cur.execute('''CREATE TABLE PROJECTS
                         ([generated_id] INTEGER,
                         [project_Name] TEXT PRIMARY KEY,
                         [massBalanceDataPoints] BLOB,
                         [exergyAnalysisDataPoints] BLOB,
                         [energyAnalysisDataPoints] BLOB,
                         [impactAnalysisDataPoints] BLOB)''')                    
                con.commit()
            except sqlite3.Error as e:
                self.showMessageBox("Unable to create Databasefile,error is "+ e.args[0])
                
################ check project and path###############
    def waitForData(self):
        if(self.projectName =="" or self.resultLocation==""):
            self.showMessageBox("Either Project name Or Result location doesnot exists. Please create or load a project for project name or browse folder for result location")
            return True
        else:
            return False
            
##################### MASS BALANCE########### 
    def extractProcessParametersData(self):
        self.processParametersData.clear()
        for i in range(len(self.massBalanceDataPoints)):
            self.processParametersData.append(self.massBalanceDataPoints[i]["Process Parameters"])
            
    def massBalanceProcess(self):
        if(self.waitForData()):
            return
        mywindow = massBalanceWindow(dataPoints=self.massBalanceDataPoints)
        
        def getMassBalanceRunData():
            self.massBalanceDataPoints = mywindow.dataPoints # get updated mass balance
            self.extractProcessParametersData()        # build process paarmeters array
            mywindow.closeWindow()
            
        mywindow.run_PB.clicked.connect(getMassBalanceRunData)
        mywindow.showWindow()
        
        
##################### Exergy Analysis ###########            
            
    def exergyAnalysisProcess(self):
        if(self.waitForData()):
            return
        if(len(self.massBalanceDataPoints)==0):
            self.showMessageBox("Mass Balance Analysis not done, Please perform Mass Balance Analysis before Exergy Analysis")
            return
        
        blankDataLen = len(self.massBalanceDataPoints) - len(self.exergyAnalysisDataPoints)
        self.exergyAnalysisDataPoints.extend(self.processParametersData[len(self.exergyAnalysisDataPoints):len(self.massBalanceDataPoints)])
                          
        mywindow = exergyAnalysisWindow(dataPoints=self.exergyAnalysisDataPoints,blankDataLen=blankDataLen)
        
        def getExergyAnalysisRunData():
            self.exergyAnalysisDataPoints = mywindow.dataPoints  # get updated exergy data
            mywindow.closeWindow()
            
        mywindow.run_PB.clicked.connect(getExergyAnalysisRunData)
        mywindow.showWindow()
        
##################### Energy Analysis ###########            
            
    def energyAnalysisProcess(self):
        if(self.waitForData()):
            return
        if(len(self.massBalanceDataPoints)==0):
            self.showMessageBox("Mass Balance Analysis not done, Please perform Mass Balance Analysis before Energy Analysis")
            return
        
        blankDataLen = len(self.massBalanceDataPoints) - len(self.energyAnalysisDataPoints)
        self.energyAnalysisDataPoints.extend(self.processParametersData[len(self.energyAnalysisDataPoints):len(self.massBalanceDataPoints)])
                  
        mywindow = energyAnalysisWindow(dataPoints=self.energyAnalysisDataPoints,blankDataLen=blankDataLen)
        
        def getEnergyAnalysisRunData():
            self.energyAnalysisDataPoints = mywindow.dataPoints # get updated energy data
            mywindow.closeWindow()
            
        mywindow.run_PB.clicked.connect(getEnergyAnalysisRunData)
        mywindow.showWindow()
    
    
##################### impact assesment Analysis ########### 
    def createfullData(self):
        tempdict=defaultdict(list)
        tagName=["Process Parameters","Energy","Pyrolysis Products", "Emissions", "EA sampleNo and Assesment method"]
        data = self.energyAnalysisDataPoints[self.energyAnalysisSampleNo] 
        
        tempdict[tagName[0]] = data[tagName[0]]
        tempdict[tagName[1]] = data[tagName[1]]
        tempdict[tagName[2]] = data[tagName[2]]
        
        
        if(len(self.impactAnalysisDataPoints)==0):
            tempdict[tagName[3]] =  [""for k in range(15)] # len of array is 15
            tempdict[tagName[4]] = ["ImpacT2002+"]
            tempdict[tagName[4]].extend(str(self.energyAnalysisSampleNo))
        else:
            tempdict[tagName[3]] = self.impactAnalysisDataPoints[0][tagName[3]]
            tempdict[tagName[4]] = self.impactAnalysisDataPoints[0][tagName[4]]
            tempdict[tagName[4]][1] = str(self.energyAnalysisSampleNo)
            
        return(tempdict)           
            
    def impactAssesmentProcess(self):
        if(self.waitForData()):
            return
        if(len(self.energyAnalysisDataPoints)==0):
            self.showMessageBox("Energy Analysis not done, Please perform Energy Analysis before Impact Analysis")
            return
        self.energyAnalysisSampleNo =0 # this will be output from energy analysis fun processing   # test 
        
        if(self.energyAnalysisSampleNo >= len(self.energyAnalysisDataPoints)):
            self.showMessageBox("Optimal Energy Analysis sample number out of range, sample no is " + str(self.energyAnalysisSampleNo)+ " length of Energy analysis points is "+ str(len(self.energyAnalysisDataPoints)))
            return
        
        mywindow = impactAssesmentWindow(data=self.createfullData())
        
        def getImpactAssesmentRunData():
            mywindow.fetchData()
            self.impactAnalysisDataPoints.clear()
            self.impactAnalysisDataPoints.append(mywindow.data) # get updated energy data
            mywindow.closeWindow()
            
        mywindow.run_PB.clicked.connect(getImpactAssesmentRunData)
        mywindow.showWindow()
    
        
