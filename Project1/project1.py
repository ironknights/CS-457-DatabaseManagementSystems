import os
import re

globalScopeDirectory = ""
workingDirectory = ""


def main():
    table_arr = ["table"]
    flag = 0

    try:
        # Creating files to store the databases for security

        if not os.path.exists("./files"):

            os.makedirs("./files")

        while True:
            command = ""

        # To check of the flag input is correct
            if flag is 1:

                    # removes the files from the folder

                    toRemove = "./files/" + table_arr[0]

                    if os.path.isfile(toRemove):

                        os.remove(toRemove)

                    table_arr = ["table"]

                    # sets the flag back to 0 for the upcoming condition

                    flag = 0

            if flag is not 1:

                # Checks for the intry of ; and --

                while not ";" in command and not "--" in command:

                    # takes in the input from the terminal

                    command += input("\n enter a command \n").strip('\r')

            command = command.split(";")[0]

            command_string = str(command)
            command_string = command_string.upper()

            if "--" in command:
                pass

            elif "CREATE DATABASE" in command_string:
                create_db(command)

            elif "CREATE TABLE" in command_string:
                create_table(command)

            elif "ALTER TABLE" in command_string:
                alter_table(command)

            elif "DROP DATABASE" in command_string:
                drop_db(command)

            elif "DROP TABLE" in command_string:
                drop_table(command)

            elif "SELECT*" in command_string:
                select_in(command)

            elif "USE" in command_string:
                use_db(command)

            elif ".EXIT" in command:
                print("All done.")
                exit()

    except (EOFError, KeyboardInterrupt) as e:
        print("\n All done.")



def check_db():  # Catch the error when a database hasn't been enabled

    if globalScopeDirectory is "":
        raise ValueError("!Failed to use table because no database was selected")
    else:
        global workingDirectory
        workingDirectory = os.path.join(os.getcwd(), globalScopeDirectory)




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

        check_db()

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

# This function alters the table inside the database directory

def alter_table(input):

    try:

        check_db()  # Check that a database is selected

        table_name = input.split("ALTER TABLE ")[1]

        table_name = table_name.split(" ")[0].lower()

        file_name = os.path.join(workingDirectory, table_name)

        if os.path.isfile(file_name):

            if "ADD" in input:

                with open(file_name, "a") as table:

                    add_string = input.split("ADD ")[1]

                    table.write(" | " + add_string)

                    print("Table " + table_name + " modified.")

        else:
            
            print("!Failed to alter table " + table_name + " because it does not exist")

    except IndexError:

        print("!Failed to alter Table because no table name is specified")

    except ValueError as err:

        print(err.args[0])

# This function prints the table

def select_in(input):
  try:
      check_db()

      database = input.split("FROM ")[1]

      # getting the user table

      subdir = os.path.join(workingDirectory, database)

      if os.path.isfile(subdir):

          with open(subdir, "r+") as new_output:

              output = new_output.read()

              print(output)
  except IndexError:

      print("Failed to print the table")

  except ValueError as err:
      print(err.args[0])

# This function deletes the database

def drop_db(input):
    try:

        directory = input.split("DROP DATABASE ")[1]

        if os.path.exists(directory):

            for remove_val in os.listdir(directory):

                os.remove(directory + "/" + remove_val)

            os.rmdir(directory)

            print("Database " + directory + " deleted.")

        else:

            print("!Failed to delete database " + directory + " because it does not exist")

    except IndexError:
        print("!No database name specified")


# This function deletes the table inside the database directory

def drop_table(input):
    try:
        check_db()

        sub_dir = input.split("DROP TABLE ")[1]

        path_to_table = os.path.join(workingDirectory, sub_dir)

        if os.path.isfile(path_to_table):

            os.remove(path_to_table)

            print("Table " + sub_dir + " deleted.")
        else:
            print("!Failed to delete Table " + path_to_table + " because it does not exist")


    except IndexError:
        print("!Failed to remove Table because no table name is specified")
    except ValueError as err:
        print(err.args[0])

# This function deletes the table inside the database directory


def use_db(input):
    try:
        global globalScopeDirectory

        globalScopeDirectory = input.split("USE ")[1]

        if os.path.exists(globalScopeDirectory):

            print("Using database " + globalScopeDirectory + " .")

        else:
            raise ValueError("!Failed to use database because it does not exist")

    except IndexError:
        print("!No database name specified")
    except ValueError as err:
        print(err.args[0])


if __name__ == '__main__':
    main()