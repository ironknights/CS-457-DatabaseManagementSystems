
# Author : Deeptanshu Das
# Date : November 12, 2019

from Query import Query

# This class adds the Alter statement functionality

class AlterStatement(Query):

    def __init__(self, queryInput):
        super(AlterStatement, self).__init__()
        self.queryInput = queryInput
        self.database = None

    def execute(self):

        states = {
            "ADD": self.__executeAdd,
            "DROP": self.__executeDrop,
            "MODIFY": self.__executeModify
        }


        tableName = self.queryInput[0]

        if len(self.queryInput) > 1:
            state = self.queryInput[1].upper()
            if state in states.keys():
                states[state](tableName, self.queryInput[2:])
                print ("Table", tableName, "modified.")
            else:
                print ("!Invalid SQL Statement!")
        else:
            print ("!Invalid SQL Statement!")

    def __executeAdd(self, tableName, addInput):

        if len(addInput) > 1:
            attrName = addInput[0].strip()
            dataType = addInput[1].strip()
            table = self.database.getTableByName(tableName)
            if table is not None:

                if not self.database.isWritable(table.tableName):
                    print(f"Error: Table {table.tableName} is locked!")
                    return

                table.addColumn(attrName, dataType)

                self.database.successfulTransactions += 1

    def __executeDrop(self, tableName, dropInput):
        pass

    def __executeModify(self, tableName, modifyInput):
        pass
