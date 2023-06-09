
# Author : Deeptanshu Das
# Date : November 12, 2019


from Query import Query 

# This class adds the INSERT functionality to the project

class InsertStatement(Query):

    def __init__(self, queryInput):

        self.__parseInsert(queryInput)
        self.database = None 

    def execute(self):

        if self.database is None:
            print ("!Failed to execute INSERT on table", self.tableName, "because no database is selected!")
            return 


        table = self.database.getTableByName(self.tableName)

        if table is None:
            print ("!Failed to execute INSERT on table", self.tableName, "because it does not exist!")
            return

        # Check for a lock
        if not self.database.isWritable(table.tableName):
            print(f"Error: Table {table.tableName} is locked!")
            return

        table.insert(self.values)
        
        self.database.successfulTransactions += 1

    def __parseInsert(self, queryInput):
        tableName = queryInput[0] 

        queryInput = queryInput[1:]

        queryInput[0] = queryInput[0][6:].replace('(', '')
        if(queryInput[0] == ''):
            queryInput = queryInput[1:] 
            
        values = []
        for i in range(len(queryInput)):
            temp = queryInput[i].replace(')', '').replace('(', '').strip().split(',')
            for val in temp:
                if val != '':
                    values.append(val.replace("'", ''))

        self.tableName = tableName # Sanitized table name 
        self.values = values # List of sanitized values to insert 
