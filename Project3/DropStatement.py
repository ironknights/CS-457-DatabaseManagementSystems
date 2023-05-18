

# Author : Deeptanshu Das
# Date : November 12, 2019

import shutil
import os

from Query import Query
from Database import Database

# This class adds to the DROP functionality of the project


class DropStatement(Query):

    def __init__(self, dropType, name):
        super(DropStatement, self).__init__()
        self.name = name
        self.dropType = dropType
        self.database = None
     
    def execute(self):

        if self.dropType == "DATABASE":

            dirs = next(os.walk("."))[1] 
            if self.name in dirs:
                shutil.rmtree(self.name)
                print ("Database", self.name, "deleted.")
            else:
                print ("!Failed to delete", self.name, "because it does not exist.")

            return Database() 

        elif self.dropType == "TABLE" and self.database is not None:

            if self.database.tableInDB(self.name):
                self.database.removeTable(self.name)
                print ("Table", self.name, "deleted.")
            else:
                print ("!Failed to delete", self.name, "because it does not exist.")
        else:
            print ("!Invalid SQL Statement!")
            
