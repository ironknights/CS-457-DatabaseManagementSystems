
# Author : Deeptanshu Das
# Date : November 12, 2019

import os
import Joins

# This class makes the table of the database

class Table(object):
    def __init__(self, dbName, tableName, newlyCreated=False):
        # Initialize member variables.
        self.dbName = dbName
        self.tableName = tableName
        # if not self.tableName.endswith('.tbl'):
        #    self.tableName += '.tbl'
        self.fileName = tableName + ".tbl"
        self.safeName = tableName.lower()

        # If the table is not brand new:
        if not newlyCreated:
            # Check to ensure the table does exist.  If it does, read in
            # the table schema and data.
            dbDir = './' + self.dbName + '/'
            if self.fileName not in os.listdir(dbDir):
                print("!Table", self.tableName, "not found")
            else:
                self.schema = None
                self.rows = []
                # Read in and store all data from the table
                fid = open(dbDir + self.fileName)
                lines = fid.readlines()

                # Set the table schema
                self.schema = self.__parseSchema(lines[0])

                # Store each row as an entry in the dictionary
                for row in lines[1:]:
                    parsedRow = self.__parseRow(row)
                    self.rows.append(parsedRow)
                fid.close()
        # If the table is new, create empty table.
        else:
            self.schema = {}
            self.rows = []

    def getFriendlyName(self):

        return self.safeName

    def save(self):

        if self.dbName is not None:
            dbDir = './' + self.dbName + '/'
            fid = open(dbDir + self.fileName, mode='w')

            # Write the schema as the first row
            fid.write(self.getSchemaString())

            # Write each row to the file
            for row in self.rows:
                fid.write(" | ".join(row.values()))
                fid.write('\n')
            fid.close()

    def getDataByAttrName(self, attrList, where=None, joinType=None):

        returnSet = []
        if ["*" in tmp for tmp in attrList][0]:
            attrList = list(self.schema.keys())
        if where is None or len(where) == 0:
            for row in self.rows:
                temp = {}
                for key in list(self.schema.keys()):
                    if key in attrList:
                        temp[key] = row[key]
                returnSet.append(temp)
        else:
            for row in self.rows:
                if self.conditionCheck(where[0], where[1], where[2], row):
                    temp = self.__buildRow(row, attrList)
                    returnSet.append(temp)
                elif joinType == Joins.LEFT_OUTER_JOIN:
                    # Set all values from left table to NULL 
                    prefix = self.__getPrefix(list(self.schema.keys())[0])
                    temp = self.__buildRow(row, attrList, joinType, prefix)
                    returnSet.append(temp)



        return returnSet

    def addColumn(self, attrName, dataType):

        # Check if column already exists
        if self.attrExists(attrName):
            print("!Failed to add column", attrName,
                  "because it already exists")
            return False

        self.schema[attrName] = dataType
        for row in self.rows:
            row[attrName] = "NULL"
        return True

    def dropColumn(self, attrName):

        if not self.__attrInSchema(attrName):
            return False

        self.schema.pop(attrName)
        for row in self.rows:
            row.pop(attrName)
        return True

    def modifyColumn(self, attrName, dataType):

        if not self.__attrInSchema(attrName):
            return False

        castable = True
        for row in self.rows:
            if not self.__isCastableTo(row[attrName], dataType):
                castable = False
                break
        if castable:
            self.schema[attrName] = dataType
            return True
        else:
            return False

    def setSchema(self, schema):

        self.schema = schema

    def getSchemaString(self):

        schemaStr = ""
        index = 0
        iterSchema = list(self.schema.items())
        for attributeName, dataType in iterSchema:
            schemaStr += attributeName + " (" + dataType + ") "
            schemaStr += " | " if (index < len(self.schema) - 1) else "\n"
            index += 1
        return schemaStr

    def insert(self, values, columns=None):



        if columns is None:
            # Check that we have a value for every attribute
            if len(values) != len(self.schema):
                print("!Failed to insert on table", self.tableName,
                      "because there must be a value for every attribute")
                return False

            row = {}
            index = 0
            for attrName, dataType in list(self.schema.items()):
                # Check that the data type of this element is correct
                if not self.__isCastableTo(values[index], dataType):
                    print("!Failed to insert on table", self.tableName,
                          "because data type does not match schema!")
                    return False
                # Add to the row
                row[attrName] = values[index]
                index += 1
            self.rows.append(row)
            print("1 new record inserted.")
            return True

        else:
            if len(values) != len(columns):
                print("!Failed to insert on table", self.tableName,
                      "because there must be a value for every attribute")
                return False
            
            row = {}
            index = 0 
            for attrName, dataType in list(self.schema.items()):
                # Check to see if the column has data 
                if attrName in columns:
                    # Check the data type 
                    if not self.__isCastableTo(values[index], dataType):
                        print("!Failed to insert on table", self.tableName,
                              "because data type does not match schema!")
                        return False
                    # Add to the row 
                    row[attrName] = values[index]
                    index += 1
                else:
                    # Set value to NULL 
                    row[attrName] = "NULL"
            self.rows.append(row)
            print("1 new record inserted.")
            return True 

    def delete(self, where=None):

        if where is None or len(where) == 0:
            self.rows = []
            return True


        column = where[0]

        if not self.attrExists(column):
            print("!Failed to delete from table", self.tableName,
                  "because column", column, "does not exist")
            return False


        delRows = self.getDataByAttrName('*', where)
        for row in delRows:
            self.rows.remove(row)
        print(len(delRows), "records" if len(
            delRows) > 1 else "record", "deleted.")
        return True

    def update(self, updates, where=None):

        for column, value in list(updates.items()):
            if not self.attrExists(column):
                print("!Failed to update table", self.tableName,
                      "because", column, "is not an attribute in the table.")
                return False

        if where is None or len(where) == 0:
            for row in self.rows:
                for column, value in list(updates.items()):
                    row[column] = value
            return True


        column = where[0]
        operator = where[1]
        value = where[2]

        # Verify that the where column exists.
        if not self.attrExists(column):
            print("!Failed to update table", self.tableName, "because",
                  column, "is not an attribute in the table.")
            return False

        # For every row of the table, check against the where conditional and update if successful.
        for row in self.rows:
            if self.conditionCheck(column, operator, value, row):
                for upCol, upVal in list(updates.items()):
                    row[upCol] = upVal

        return True

    def __parseSchema(self, schemaInput):
        '''
        Purpose:    Parses schema in format saved to files.
     	Parameters: schemaInput: The input to parse into a schema
    	Returns: A dictionary containing the schema for the table
        
        '''
        schema = {}

        columns = schemaInput.split('|')
        for column in columns:
            column = column.strip()
            data = column.split()
            attributeName = data[0]
            dataType = data[1][1:-1]
            schema[attributeName] = dataType

        return schema

    def __parseRow(self, rowInput):

        columns = rowInput.split('|')
        attributes = list(self.schema.keys())

        row = {}
        for i in range(len(columns)):
            row[attributes[i]] = columns[i].strip()

        return row

    def __attrInSchema(self, attrName):

        return (attrName in self.schema.keys())

    def __isCastableTo(self, val, newType):

        newType = self.getType(newType)
        if newType is str:
            return True
        try:
            self.castColumn(val, newType)
            return True
        except ValueError:
            return False

    def attrExists(self, attrName):

        return self.__attrInSchema(attrName)

    def conditionCheck(self, column, operator, value, row):

        column = column.strip().replace("'", '')
        operator = operator.strip()
        value = value.strip().replace("'", '')

        castType = None 
        try:
            castType = self.getType(self.schema[column])
            if '.' in value:
                castType2 = self.getType(self.schema[value])
                value = self.castColumn(row[value], castType2)
            else:
                value = self.castColumn(value, castType)
        except:
            return False 

        testValue = self.castColumn(row[column], castType)
        return self.__conditionCompare(testValue, operator, value)

    def __conditionCompare(self, lVal, operator, rVal):

        if operator == "=":
            return lVal == rVal
        if operator == "!=" or operator == "<>":
            return lVal != rVal
        if operator == "<":
            return lVal < rVal
        if operator == ">":
            return lVal > rVal
        if operator == "<=":
            return lVal <= rVal
        if operator == ">=":
            return lVal >= rVal
        return False

    def castColumn(self, column, castType):

        return castType(column)

    def getType(self, string):

        string = string.split("(")
        string = string[0]
        string = string.lower()
        if string == "char":
            return str
        if string == "varchar":
            return str
        if string == "int":
            return int
        if string == "float":
            return float
    
    def printTableByAttr( self, attrList, where=None, joinType=None):

        header = ""
        body = ""
        rows = self.getDataByAttrName(attrList, where, joinType)
        index = 1
        if ["*" in tmp for tmp in attrList][0]:
            attrList = self.schema.keys()
        for attr in attrList:
            cleanAttr = attr.split(".")
            if( len(cleanAttr) > 1):
                cleanAttr = cleanAttr[1]
            else:
                cleanAttr = cleanAttr[0]
            header += cleanAttr + " " + self.schema[attr]
            header += "|" if(index<len(attrList)) else ""
            index += 1
        print(header)

        for row in rows:
            index = 1
            for value in row.values():
                body += value
                body += "|" if(index<len(row)) else ""
                index += 1
            body += "\n"
        body = body[0:-1]
        print(body)

    def printTable( self ):

        self.printTableByAttr( ["*"] )

    def __getPrefix(self, attribute):

        result = attribute.split('.')
        if(len(result) == 1):
            return None 
        return result[0]

    def __buildRow(self, row, attrList, joinType=Joins.NO_JOIN, prefix=None):

        temp = {}
        for key in list(self.schema.keys()):
            if key in attrList:
                if joinType == Joins.LEFT_OUTER_JOIN and self.__getPrefix(key) != prefix:
                    temp[key] = ""
                else:
                    temp[key] = row[key]
        return temp 

    def __addTableNameToRow(self, tname, row):

        newRow = {}
        for k, v in list(row.items()):
            newRow[tname + "." + k] = v
        return newRow

    @classmethod 
    def OuterJoin(cls, ltable, rtable, joinType, conditions):

        found = False 
        T = Table(None, "MERGE", True)
        L, R = None, None
        if joinType == Joins.LEFT_OUTER_JOIN:
            L = ltable 
            R = rtable 
        elif joinType == Joins.RIGHT_OUTER_JOIN:
            R = ltable 
            L = rtable 
        else:
            return None

        lName = L.getFriendlyName()
        rName = R.getFriendlyName()

        lCol = conditions[0].strip() # lCol = conditions[0].replace(lName, '')[1:]
        operator = conditions[1].strip()
        rCol = conditions[2].strip() # rCol = conditions[2].replace(rName, '')[1:]

        for lRow in L.rows:
            found = False 
            lRow = cls.__addTableNameToRow(L, lName, lRow)
            lVal = lRow[lCol]
            index = 1
            for rRow in R.rows:
                rRow = cls.__addTableNameToRow(R, rName, rRow)
                rVal = rRow[rCol]
                if(cls.__conditionCompare(L, lVal, operator, rVal)):
                    # Add the row normally 
                    row = {**lRow, **rRow}
                    T.rows.append(row)
                    found = True 
                elif index == len(R.rows) and found == False:
                    for k in list(rRow.keys()):
                        rRow[k] = ""
                    row = {**lRow, **rRow}
                    T.rows.append(row)
                index += 1
        return T 

