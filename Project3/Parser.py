
# Author : Deeptanshu Das
# Date : November 12, 2019

import os
import shutil
from Database import Database
from CreateStatement import CreateStatement
from UseStatement import UseStatement
from DropStatement import DropStatement
from SelectStatement import SelectStatement
from AlterStatement import AlterStatement
from InsertStatement import InsertStatement
from DeleteStatement import DeleteStatement
from UpdateStatement import UpdateStatement
from CommitStatement import CommitStatement

from queue import Queue

# The purpose of this class is to parse the input from the user

class Parser(object):

    def __init__(self):
        self.queries = Queue()

    def parse(self, SQLinput):


        states = {
            "CREATE": self.__parseCreate,
            "USE": self.__parseUse,
            "ALTER": self.__parseAlter,
            "DROP": self.__parseDrop,
            "SELECT": self.__parseSelect,
            "INSERT": self.__parseInsert,
            "DELETE": self.__parseDelete,
            "UPDATE": self.__parseUpdate,
            "BEGIN": self.__parseBegin,
            "COMMIT": self.__parseCommit
        }

        SQLinput = SQLinput.strip()
        statements = SQLinput.split(';')
        for input in statements:
            input = input.strip()
            if input.upper() == ".EXIT":
                    self.queries.put("EXIT")
                    continue
            elif input.startswith("--"):
                continue
            elif input == "":
                continue

            tokens = input.split()
            if tokens[0].upper() in states.keys():
                self.queries.put(states[tokens[0].upper()](tokens[1:]))
            else:
                self.__invalidStatement()
        return self.queries
    
    def __parseCreate(self, input):
        if input[0].upper() == "DATABASE":
            return CreateStatement("DATABASE", dbName=input[1])
        elif input[0].upper() == "TABLE":
            return CreateStatement("TABLE", attributes=input[1:])
        else:
            pass #ERROR

    def __parseUse(self, input):

        dbName = input[0]
        return UseStatement(dbName) 

    def __parseSelect(self, input):
        return SelectStatement(input) 

    def __parseDrop(self, input):
        if input[0].upper() == "DATABASE":
            return DropStatement("DATABASE", input[1])        
        elif input[0].upper() == "TABLE":
            return DropStatement("TABLE", input[1])
        self.__invalidStatement()
        return None 

    def __parseAlter(self, input):
        if input[0].upper() == "TABLE":
            return AlterStatement(input[1:])
        else:
            return None 

    def __parseInsert(self, input):
        if input[0].upper() != "INTO":
            self.__invalidStatement()
            return None
        return InsertStatement(input[1:])

    def __parseDelete(self, input):
        if input[0].upper() != "FROM":
            self.__invalidStatement()
            return None 
        return DeleteStatement(input[1:])

    def __parseUpdate(self, input):

        if len(input) < 3:
            self.__invalidStatement()
            return None 
        return UpdateStatement(input)

    def __invalidStatement(self):

        print ("!Invalid SQL statement!")

    def __parseBegin(self, input):
        if not len(input) == 1:
            self.__invalidStatement()
            return None
        if not input[0].lower() == "transaction":
            self.__invalidStatement()
            return None

    
    def __parseCommit(self, input):
        if not len(input) == 0:
            self.__invalidStatement()
            return None
        return CommitStatement()

        
