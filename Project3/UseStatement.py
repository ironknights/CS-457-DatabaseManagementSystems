
# Author : Deeptanshu Das
# Date : November 12, 2019

import os

from Query import Query
from Database import Database

# This class performs the USE functionality for the database

class UseStatement(Query):
    def __init__(self, dbName):
        super(UseStatement, self).__init__()
        self.dbName = dbName
    
    def execute(self):
        if self.dbName in next(os.walk("."))[1]:
            print ("Using database", self.dbName + ".")
            return Database(self.dbName)
        else:
            print ("!Cannot use database", self.dbName, "because it does not exist.")
            return None
