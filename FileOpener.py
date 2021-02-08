import csv

import ClassDef

import HashFunctions as hasher


# Used to open the package file and returned a hashed list of the packages
def package_file_open():

    # opens the .csv file to be edited
    with open('wgupsPackageFile.csv') as csvFile:

        # defines the variable to hold the values of the .csv file
        readCsv = csv.reader(csvFile, delimiter=',')

        # will be the hash table returned at the end of the function
        hashedTable = [None for _ in range(hasher.table_size)]

        # loops through all available rows in the csv
        for row in readCsv:

            # checks to make sure it is not the column names values
            if row[0] != "Package ID":

                # sets the variables to the data pulled from the file, and casting values to be appropriate
                # variable types
                packageId = int(row[0])
                address = row[1].strip('"')
                city = row[2]
                state = row[3]
                zipCode = row[4]
                deadline = row[5]
                weight = int(row[6])
                specialNotes = row[7]

                # creates a class defined package that holds all the found values
                package = ClassDef.Package(packageId, address, city, state, zipCode, deadline, weight, specialNotes)

                # creates a node with the package defined attached
                listPackage = ClassDef.PackageNode(package)

                # function call to insert value into the hash table, returns the updated table
                hashedTable = hasher.hashInsert(hashedTable, listPackage)

    # returns the completed hash table
    return hashedTable


# calls to open the distances file and splits the values into locations and distances
def distance_file_open():

    # opens the .csv file
    with open('wgupsDistanceFile.csv') as csvFile:

        # holds the csv file in a readable format
        readCsv = csv.reader(csvFile, delimiter=',')

        # holds the list of the locations, the shorter version, and the index value
        listOfLocations = []

        # holds the distances matrix from one store to the next
        distances = []

        # holds the count of thw index values for the distance
        counter = 0

        # loops through the rows of the csv to assign the values
        for row in readCsv:

            # adds the values of the rows associated with the desired values
            listOfLocations.append([row[0], row[1], counter])

            # adds an empty list to add the distance values
            distances.append([])

            # goes through the column values of the row
            for column in row:

                # checks to make sure it is not the list of locations values
                if (column != row[0]) & (column != row[1]):

                    # checks to make sure it is a valid entry
                    if column is not '':

                        # adds the value of the column to the distances matrix, casting them as a float value
                        distances[counter].append(float(column.strip("'")))

                    # if entry is not valid fill matrix with -1 values to show no travel possible
                    else:
                        distances[counter].append(-1)

            # adds to the counter to keep track of the index value
            counter += 1

    # returns a list of the distance matrix and the list of locations matrix
    return [distances, listOfLocations]
