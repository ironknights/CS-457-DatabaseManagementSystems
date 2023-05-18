
# Author : Deeptanshu Das
# Date : November 12, 2019


import sys


# This is the main file that imports the files needed to execute the database

from Parser import Parser
from UseStatement import UseStatement
from Query import Query
from Database import Database 

EXIT_COMMAND = "EXIT"

parser = Parser()
dbContext = Database()

def main():
    global dbContext 

    print ("Enter SQL queries ending with ; or .EXIT to end session")
    while True:
        SQLInput = GetSQLInput()
        if SQLInput == "":
            continue
        parsedQueries = parser.parse(SQLInput)
        
        if ExecuteQueries(parsedQueries) == EXIT_COMMAND:
            break

    # Save before exiting 
    if dbContext is not None:
        dbContext.save() 
    
    print ("All done.")


# This function gets the sql input from the user

def GetSQLInput():

    SQLInput = ""
    try:
        SQLInput = input()
        if SQLInput.startswith("--"): SQLInput = ""
        while not (SQLInput.endswith(';') or SQLInput.upper().endswith('.EXIT')):
            line = input()
            if line.startswith("--"): line = ""
            SQLInput += ' ' + line
        return SQLInput
    except EOFError:
        SQLInput += "\n"
        return SQLInput

# This function adds to the functionality of executing queries

def ExecuteQueries(queries):

    global dbContext

    while not queries.empty():
        query = queries.get()        

        if type(query) is UseStatement:
            dbContext.save() 
        if isinstance(query, Query):
            query.setDBContext(dbContext)
        if query == EXIT_COMMAND:
            return EXIT_COMMAND
        elif query is not None:
            retVal = query.execute()

            if not dbContext.transactionInProgress:
                for table in list(dbContext.tables.values()):
                    table.save()
            


            if type(retVal) is Database:
                dbContext = retVal


if __name__ == "__main__":
    main()
