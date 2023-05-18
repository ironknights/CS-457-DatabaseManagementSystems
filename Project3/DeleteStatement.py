
# Author : Deeptanshu Das
# Date : November 12, 2019

from Query import Query 

# The following class creates a DELETE functionality
class DeleteStatement(Query):

    def __init__(self, queryInput):
        self.database = None
        self.tableName, self.conditions = self.__parseDelete(queryInput)

    def execute(self):

        if self.database is None:
            print("!Failed to delete from table", self.tableName, "because no database is selected!")
            return None 
        
        table = self.database.getTableByName(self.tableName) 

        if table is None:
            print("!Failed to delete from table", self.tableName, "because table does not exist!")
            return None

        # Check for a lock
        if not self.database.isWritable(table.tableName):
            print(f"Error: Table {table.tableName} is locked!")
            return

        table.delete(self.conditions)

        self.database.successfulTransactions += 1

    def __parseDelete(self, queryInput):

        tableName = queryInput[0] 

        conditions = queryInput[2:]

        return tableName, conditions
