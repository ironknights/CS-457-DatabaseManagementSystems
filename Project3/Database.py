
# Author : Deeptanshu Das
# Date : November 12, 2019

from Table import Table
import os
import glob

# This class creates the DATABASE


class Database(object):

    def __init__(self, dbName=None):

        self.dbName = dbName
        self.tables = {}

        self.transactionInProgress = False
        self.successfulTransactions = 0

        if self.dbName is not None:
            tablesList = glob.glob(f"./{self.dbName}/*.tbl")
            for entry in tablesList:
                entry = entry.split("/")[-1]
                if entry.endswith(".tbl"):
                    entry = entry[0:-4]
                temp = Table(self.dbName, entry)

                self.tables[temp.safeName] = temp 

    def save(self):


        for table in self.tables.values():
            table.save()
        

        if self.dbName is not None:
            dbDir = "./" + self.dbName + "/"

            tableFiles = [tbl.fileName for tbl in self.tables.values()]
            diskFiles = os.listdir(dbDir)
            for filename in diskFiles:
                if filename not in tableFiles:
                    os.remove(dbDir + filename)

    def addTable(self, newTable):

        if self.dbName is not None:
            self.tables[newTable.safeName] = newTable

    def removeTable(self, tableName):

        tableName = tableName.lower()
        if self.tableInDB(tableName):
            self.tables.pop(tableName)

    def tableInDB(self, tableName):

        return (tableName.lower() in self.tables.keys())
    
    def getTableByName(self, tableName):

        tableName = tableName.lower()
        if self.tableInDB(tableName):
            tname = self.tables[tableName].tableName 
            self.tables[tableName] = Table(self.dbName, tname)
            return self.tables[tableName]
        else:
            return None
        
    def isWritable(self, tableName):

        # Check for a lock file 
        files = glob.glob(f"./{self.dbName}/{tableName}.*")
        if len(files) > 1:
            # Check the pid matches 
            pid = str(os.getpid())
            for filename in files:
                extension = filename.split('.')[2]
                if extension == pid:
                    return True 
            return False 
        return True 
        
