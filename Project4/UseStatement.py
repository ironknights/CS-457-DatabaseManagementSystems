# Author : Deeptanshu Das
# Date : December 10, 2019

import os

from Query import Query
from Database import Database


#	Class : UseStatement
#	Purpose : Models a USE query on a SQL database

class UseStatement(Query):

    def __init__(self, dbName):
        super(UseStatement, self).__init__()
        self.dbName = dbName
    
    def execute(self):
        '''
        Purpose:    Implementation of a USE Statement.
     	Parameters: None
    	Returns:    Database context of the current database.
        '''
        if self.dbName in next(os.walk("."))[1]:
            print ("Using database", self.dbName + ".")
            return Database(self.dbName)
        else:
            print ("!Cannot use database", self.dbName, "because it does not exist.")
            return None
