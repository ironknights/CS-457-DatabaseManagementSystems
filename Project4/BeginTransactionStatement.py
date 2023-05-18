# Author : Deeptanshu Das
# Date : December 10, 2019
import os
from Query import Query

class BeginTransactionStatement(Query):
    '''Models a BEGIN TRANSACTION SQL statement'''
    def __init__(self):
        pass 

    def execute(self):
        ''' 
        Purpose : Execute a BEGIN TRANSACTION statement
        Parameters : 
            None
        Returns: None
        '''
        # Print Transaction starts.
        # Set transaction flag 
        # Lock all tables by creating lock files 
        if self.database is not None:
            print("Transaction starts.")
            self.database.transactionInProgress = True 
            self.database.successfulTransactions = 0

            

            for tableName, table in list(self.database.tables.items()):
                if self.database.isWritable(table.tableName):
                    self.__createLockFile(table.tableName)

    def __createLockFile(self, fName):
        ''' 
        Purpose : Create a lock file for a given table
        Parameters : 
            tableName: The name of the table
        Returns: true if the file was created successfully
        ''' 
        pid = os.getpid() 
        f = open(f"{self.database.dbName}/{fName}.{pid}", "w")
        f.close()

