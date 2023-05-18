"""
Author: Deeptanshu Das
Class: CS 457

"""

import os
import re

globalScopeDirectory = ""
workingDirectory = ""


def main():
    try:
        while True:
            command = ""
            while not ";" in command and not "--" in command:
                command += input("\n enter a command \n")

            command = command.split(";")[0]
            command_string = str(command)
            command_string = command_string.upper()

            if "--" in command:
                pass

            elif "ALTER TABLE" in command_string:
                alter_table(command)

            elif "CREATE DATABASE" in command_string:
                create_db(command)

            elif "CREATE TABLE" in command_string:
                create_table(command)

            elif "DELETE FROM" in command_string:
                delete_from(command)

            elif "DROP DATABASE" in command_string:
                drop_db(command)

            elif "DROP TABLE" in command_string:
                drop_table(command)

            elif "INSERT INTO" in command_string:
                insert(command)

            elif "SELECT" in command_string:
                select_from(command, command_string)

            elif "UPDATE" in command_string:
                update_table(command)

            elif "USE" in command_string:
                use_db(command)

            elif ".EXIT" in command:
                print ("All done.")
                exit()

    except (EOFError, KeyboardInterrupt) as e:
        print ("\n All done.")


def use_enabled():  # Catch the error when a database hasn't been enabled

    if globalScopeDirectory is "":

        raise ValueError("!Failed to use table because no database was selected")

    else:
        global workingDirectory

        workingDirectory = os.path.join(os.getcwd(), globalScopeDirectory)


def get_column(data):

    column_index = data[0].split(" | ")

    for x in range(len(column_index)):

        column_index[x] = column_index[x].split(" ")[0]

    return column_index


def separate(line):

    line_tester = line.split(" | ")

    for x in range(len(line_tester)):  # Check that each column has an item

        line_tester[x] = line_tester[x].split(" ")[0]

    return line_tester


# This function creates the database

def create_db(input):
    try:

        # Takes the input and stores the name of the database
        directory = input.split("CREATE DATABASE ")[1]

        # To check if the database exists in the directory

        if not os.path.exists(directory):

            os.makedirs(directory)

            print("Database " + directory + " created.")

        else:

            print("!Failed to create database " + directory + " because it already exists")

    except IndexError:

        print("!Failed to create database because no database name specified")


# This function creates the table inside the database directory

def create_table(input):

    try:

        use_enabled()

        # This takes the entry and stores the 2nd part of the string and stroes it in the variable as
        # the sub-directory within the directory of the database

        sub_dir = re.split("CREATE TABLE ", input, flags=re.IGNORECASE)[1]

        sub_dir = sub_dir.split("(")[0].lower()

        file_name = os.path.join(workingDirectory, sub_dir)

        # To check if the database exists in the directory

        if not os.path.isfile(file_name):

            with open(file_name, "w") as table:

                print("Table " + sub_dir + " created.")

                # Check for ( in the beginning of the entry
                if "(" in input:

                    # stores the entry into the list

                    out = []

                    data = input.split("(", 1)[1]

                    data = data[:-1]

                    counter = data.count(",")

                    # Goes until the loop for the counter

                    for x in range(counter + 1):

                        out.append(data.split(", ")[

                                       x])

                    table.write(" | ".join(out))
        else:

            print("!Failed to create table " + sub_dir + " because it already exists")

    except IndexError:

        print("!Failed to create table because no table name is specified")

    except ValueError as err:
        print(err.args[0])

# Function to implement where functionality

def where(search_arg, action, data, up_val=""):

    counter = 0

    column_index = get_column(data)

    attr_name = column_index

    input_data = list(data)

    out = []

    flag = 0

    # Checks for operators =,>,

    if "=" in search_arg:  # Evaluate operator

        if "!=" in search_arg:

            r_col = search_arg.split(" !=")[0]

            flag = 1

        else:

            r_col = search_arg.split(" =")[0]

        search_arg = search_arg.split("= ")[1]

        if "\"" in search_arg or "\'" in search_arg:

            search_arg = search_arg[1:-1]

        for line in data:
            line_test = separate(line)
            if search_arg in line_test:
                column_index = attr_name.index(r_col)
                line_index = line_test.index(search_arg)
                if line_index == column_index:  # Check for correct column
                    if action == "delete":
                        del input_data[input_data.index(line)]  # Remove matching field
                        out = input_data
                        counter += 1
                    if action == "select":
                        out.append(input_data[input_data.index(line)])
                    if action == "update":
                        attribute, field = up_val.split(" = ")
                        if attribute in attr_name:
                            sep_line = separate(line)
                            sep_line[attr_name.index(attribute)] = field.strip().strip("'")
                            input_data[input_data.index(line)] = ' | '.join(sep_line)
                            out = input_data
                            counter += 1

    elif ">" in search_arg:
        r_col = search_arg.split(" >")[0]
        search_arg = search_arg.split("> ")[1]
        for line in data:
            line_test = line.split(" | ")
            for x in range(len(line_test)):
                line_test[x] = line_test[x].split(" ")[0]
                try:
                    line_test[x] = float(line_test[x])
                    if line_test[x] > float(search_arg):
                        temp_col = column_index.index(r_col)
                        if x == temp_col:
                            if action == "delete":
                                del input_data[input_data.index(line)]
                                out = input_data
                                counter += 1
                            if action == "select":
                                out.append(input_data[input_data.index(line)])
                            if action == "update":
                                print ("hi")
                except ValueError:
                    continue
    if flag:
        out = list(set(data) - set(out))
    return counter, out




def alter_table(input):
    try:
        use_enabled()  # Check that a database is selected

        table_name = input.split("ALTER TABLE ")[1]

        table_name = table_name.split(" ")[0].lower()

        file_name = os.path.join(workingDirectory, table_name)

        if os.path.isfile(file_name):

            if "ADD" in input:  # Only checks for during first project

                with open(file_name, "a") as table:  # Use A to append data to end of the file

                    add_string = input.split("ADD ")[1]

                    table.write(" | " + add_string)

                    print ("Table " + table_name + " modified.")
        else:

            print ("!Failed to alter table " + table_name + " because it does not exist")

    except IndexError:

        print ("!Failed to alter Table because no table name is specified")

    except ValueError as err:

        print (err.args[0])


# Delete function to remove specific entries

def delete_from(input):
    try:
        use_enabled()  # Check that a database is selected

        table_name = re.split("DELETE FROM ", input, flags=re.IGNORECASE)[1]

        table_name = table_name.split(" ")[0].lower()

        file_name = os.path.join(workingDirectory, table_name)

        if os.path.isfile(file_name):               # check if file is in the current file path

            with open(file_name, "r+") as table:

                data = table.readlines()

                delete_item = re.split("WHERE ", input, flags=re.IGNORECASE)[1]         # gets the input and splits it

                counter, out = where(delete_item, "delete", data)

                table.seek(0)

                table.truncate()

                for line in out:
                    table.write(line)
                if counter > 1:
                    print (counter, " records deleted.")
                elif counter == 1:
                    print (counter, " record deleted.")
                else:
                    print ("No records deleted.")
        else:
            print ("!Failed to delete table " + table_name + " because it does not exist")
    except IndexError:
        print ("!Failed to delete table because no table name is specified")
    except ValueError as err:
        print (err.args[0])


# This function deletes the database

def drop_db(input):
    try:

        directory = input.split("DROP DATABASE ")[1]

        if os.path.exists(directory):

            for remove_val in os.listdir(directory):

                os.remove(directory + "/" + remove_val)

            os.rmdir(directory)

            print ("Database " + directory + " deleted.")

        else:

            print ("!Failed to delete database " + directory + " because it does not exist")

    except IndexError:

        print ("!No database name specified")

# This function deletes the table inside the database directory

def drop_table(input):
    try:

        use_enabled()

        sub_dir = input.split("DROP TABLE ")[1].lower()

        path_to_table = os.path.join(workingDirectory, sub_dir)

        if os.path.isfile(path_to_table):

            os.remove(path_to_table)

            print ("Table " + sub_dir + " deleted.")

        else:

            print ("!Failed to delete Table " + sub_dir + " because it does not exist")

    except IndexError:

        print ("!Failed to remove Table because no table name is specified")

    except ValueError as err:
        print (err.args[0])


# Insert function to insert values
def insert(input):
    try:
        use_enabled()

        table_nm = input.split(" ")[2].lower()

        file_nm = os.path.join(workingDirectory, table_nm)

        if os.path.isfile(file_nm):

            if "values" in input:

                with open(file_nm, "a") as table:

                    out = []

                    data = input.split("(", 1)[1]

                    data = data[:-1]

                    counter = data.count(",")

                    for x in range(counter + 1):

                        out.append(data.split(",")[

                                       x].lstrip())
                        if "\"" == out[x][0] or "\'" == out[x][0]:

                            out[x] = out[x][1:-1]

                    table.write("\n")

                    table.write(" | ".join(out))

                    print ("1 new record inserted.")
            else:
                print ("!Failed to insert into " + table_nm + " because there were no specified arguments")
        else:
            print ("!Failed to alter table " + table_nm + " because it does not exist")
    except IndexError:
        print ("!Failed to insert into table because no table name is specified")
    except ValueError as err:
        print (err.args[0])


# Select function to select values

def select_from(input, inputUp):
    try:
        use_enabled()

        table_nm = re.split("FROM ", input, flags=re.IGNORECASE)[1].lower()

        if "WHERE" in inputUp:

            table_nm = re.split("WHERE", table_nm, flags=re.IGNORECASE)[0]

            if " " in table_nm:

                table_nm = table_nm.split(" ")[0]

        file_nm = os.path.join(workingDirectory, table_nm)

        output = ""

        if os.path.isfile(file_nm):

            with open(file_nm, "r+") as table:

                if "WHERE" in inputUp:

                    search_item = re.split("WHERE ", input, flags=re.IGNORECASE)[1]

                    data = table.readlines()

                    counter, output = where(search_item, "select", data)

                    for line in output:

                        print(line)

                if "SELECT *" in inputUp:

                    if not output == "":

                        for line in output:

                            print(line)
                    else:
                        output = table.read()
                        print(output)
                else:
                    arguments = re.split("SELECT", input, flags=re.IGNORECASE)[1]

                    attributes = re.split("FROM", arguments, flags=re.IGNORECASE)[0]

                    attributes = attributes.split(",")
                    if not output == "":

                        lines = output

                    else:
                        lines = table.readlines()

                        data = lines

                    for line in lines:

                        out = []

                        for attribute in attributes:

                            attribute = attribute.strip()

                            column_index = get_column(data)

                            if attribute in column_index:

                                separated_line = separate(line)
                                out.append(separated_line[column_index.index(attribute)].strip())
                        print (" | ".join(out))
        else:
            print ("!Failed to query table " + table_nm + " because it does not exist")
    except IndexError:
        print ("!Failed to select because no table name is specified")
    except ValueError as err:
        print (err.args[0])


# To update the table
def update_table(input):
    try:
        use_enabled()

        table_nm = re.split("UPDATE ", input, flags=re.IGNORECASE)[1]

        table_nm = re.split("SET", table_nm, flags=re.IGNORECASE)[0].lower().strip()

        file_nm = os.path.join(workingDirectory, table_nm)

        if os.path.isfile(file_nm):

            with open(file_nm, "r+") as table:

                data = table.readlines()

                update_item = re.split("WHERE ", input, flags=re.IGNORECASE)[1]

                val = re.split("SET ", input, flags=re.IGNORECASE)[1]

                val = re.split("WHERE ", val, flags=re.IGNORECASE)[0]

                counter, out = where(update_item, "update", data, val)

                table.seek(0)

                table.truncate()

                for line in out:

                    if not "\n" in line:

                        line += "\n"

                    table.write(line)

                if counter > 0:

                    print (counter, " records modified.")
                else:
                    print ("No records modified.")
        else:
            print ("!Failed to update table " + table_nm + " because it does not exist")
    except IndexError:
        print ("!Failed to update table because no table name is specified")
    except ValueError as err:
        print (err.args[0])


def use_db(input):
    try:
        global globalScopeDirectory
        globalScopeDirectory = input.split("USE ")[1]  # Store the string after USE (with global scope)
        if os.path.exists(globalScopeDirectory):
            print ("Using database " + globalScopeDirectory + " .")
        else:
            raise ValueError("!Failed to use database because it does not exist")
    except IndexError:
        print ("!No database name specified")
    except ValueError as err:
        print (err.args[0])


if __name__ == '__main__':
    main()
