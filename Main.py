# Author: Lucas Hynes, Student ID: 001235265

import FileOpener
import random
import HashFunctions as hasher
import ClassDef

# length of hash table
tableSize = 23
# number of trucks (per location)
num_trucks = 3
# number of drivers to drive trucks
num_drivers = 2
# the number of options for movement of the trucks
num_neighbors = 5
# number of packages to be applied
num_packages = 40
# number of options for the routes to find the best route available
iteration_num = 25
# holds the hashed list of the packages
packages_hashed = FileOpener.package_file_open()


# gets the neighbors by returning the three candidate indexes
def get_neighbors(locIndex, route, packages_grouped, distance_location, current_locations):
    # gets all indexes for which the trucks can travel to
    available_moves = find_available_spaces(distance_location[0], packages_grouped, distance_location[1],
                                            route.truck.truckNo)

    # sets a min distance to a high value to make sure that there is a lesser value found
    min_distance = 100

    # will hold the results of options to the different indexes
    results = []

    # will hold the index value of the result to be saved to the results list
    index_hold = -1

    # checks to make sure that the route has enough space to add another package
    if route.packagesApplied < route.truck.capacity:

        # looping to find the next closet neighbors to the given location
        for option in range(num_neighbors):

            # goes through the different options available
            for index in available_moves:

                # checks to see if the index has already been assigned or is the same as the current location
                if (index not in results) & (distance_location[1][index] != current_locations):

                    # checks to see which value is less to format a query for the distances matrix
                    if locIndex < index:
                        distance_to_index = distance_location[0][index][locIndex]
                    else:
                        distance_to_index = distance_location[0][locIndex][index]

                    # finds the associated package index from the packages grouped list
                    packages_index = package_loc_match(packages_grouped, distance_location[1][index])

                    # checks to make sure the index value is valid
                    if packages_index > -1:

                        # checking if there is a list of packages at the location
                        if packages_grouped[packages_index][1]:

                            # checks to see if the packages at this index could fit on the truck
                            if len(packages_grouped[
                                       packages_index][1]) + route.packagesApplied < route.truck.capacity:

                                # checks to see if the distance is a more effective choice than a previous value
                                if distance_to_index < min_distance:
                                    # sets the holding values to the new found effective index
                                    index_hold = index
                                    min_distance = distance_to_index

            # checks to see if there was an index value found
            if index_hold > -1:

                # if the index found has not already been added to the result
                if index_hold not in results:
                    # adds the found value to the result
                    results.append(index_hold)

            # resets the values to be able to go through the list finding the next best option
            index_hold = -1
            min_distance = 100

    # returns the values found
    return results


# groups together the hashed packages by their locations
def locationPackageMatch(hashedPackages):
    # holds list values formatted by [location1, [package1, package2...]][location2, [etc.]]...
    list_group_packages = [["", []]]

    # holds boolean value of whether or not the location is in the list
    found = False

    # loops through the different packages in a range given by the hash length function
    for packageNo in range(hasher.hash_table_length(hashedPackages, tableSize)):

        # finds the temp node of the package id associated with the node
        tempNode = hasher.hashSearch(hashedPackages, packageNo + 1)

        # checks to see if the node has the data and is not empty
        if tempNode is not None:

            # if the list group is empty
            if list_group_packages[0][0] == "":

                # sets the value of the first list to the address and the node
                list_group_packages[0][0] = tempNode.package.address
                list_group_packages[0][1] = [tempNode]

            # if there is values within the list
            else:

                # loops through the location, node matches
                for group_package in list_group_packages:

                    # checks to see if the address is matching
                    if tempNode.package.address == group_package[0]:
                        # appends the node to the list after the match is found
                        group_package[1].append(tempNode)

                        # sets the found value to true so it is not added to the end
                        found = True

                # if the value has not been matched, it adds the location and the node to the end of the list
                if not found:
                    list_group_packages.append([tempNode.package.address, [tempNode]])

            # resets the value to be able to check the packages in a loop
            found = False

    # returns the list match of the locations and the nodes associated
    return list_group_packages


# checks for the array of neighbors returned
def get_next_move(neighbors):
    # making sure the value is not -1
    if -1 in neighbors:
        neighbors.remove(-1)

    # checks to make sure list is not empty
    if neighbors:

        # returns a random option of the different neighbors found
        return neighbors[get_rand(0, len(neighbors) - 1)]
    else:
        # otherwise return a blank value
        return [0]


# returns random value within the given bounds
def get_rand(minimum, maximum):
    return random.randint(minimum, maximum)


# results in an array that holds the routes for each of the trucks called for
def length_count(locationPackageMatchList):
    # variable to hold the count of packages left in the list
    count = 0

    # loops through the list of locations and packages
    for i in locationPackageMatchList:

        # checks if i is a list
        if isinstance(i, list):

            # check for empty list
            if i:

                # variable to hold the list of packages
                temp_list = i[1]

                # check if there is a list of nodes
                if temp_list:

                    # loops through the resulting list of nodes
                    for _ in temp_list:
                        # adds to the count
                        count += 1

    # returns the final count of nodes within the list
    return count


# returns true if the location group is already assigned to a different route
def check_if_loc_in(location_group, list_of_routes):
    for route in list_of_routes:
        if location_group[0] in route.deliveryList:
            return 1, list_of_routes.index(route)

    return 0, 0


# checks to see if the input list has a package that has a delivery time associated
def check_for_deadline(package_list):
    for package_node in package_list:
        if package_node.package.deadline != "EOD":
            return True

    return False


# checks the list to see if the package with the matching package Id is associated with the list
def check_for_package(package_list, id_input):
    for package_node in package_list:
        if package_node.package.packageId == id_input:
            return True

    return False


# function returns a list of routes for all associated trucks and the information to deliver packages
def attempt_to_load():
    # holds both location and distance lists
    distance_and_location = FileOpener.distance_file_open()

    # separates the values into the two distinct lists
    distances = distance_and_location[0]
    list_of_locations = distance_and_location[1]

    # groups packages by location
    packages_hashed2 = locationPackageMatch(packages_hashed)
    # holds the list of trucks classes
    list_of_trucks = [ClassDef.Truck(i + 1) for i in range(num_trucks)]

    # holds the dictionaries of all the different delivery lists
    list_of_deliveries = [{} for _ in range(num_trucks)]

    # creates the list of routes, combining the list of trucks and delivery lists
    list_of_routes = [ClassDef.Route(list_of_trucks[i], list_of_deliveries[i]) for i in range(num_trucks)]

    # returns the modified values of the packages remaining, the updated list of routes, and also the current indexes
    # of the trucks after handling the special instructions for the packages
    packages_grouped, list_of_routes, current_route_loc_index, distances = load_from_special_instructions(
        packages_hashed2, list_of_routes, list_of_locations, distances)

    # resets the format of the two matrix
    packages_grouped = clean_list(packages_grouped)
    distances = clean_distance(packages_grouped, distances, list_of_locations)

    neighbors = None

    # loops while the length of the grouped packages is greater than 0 to make sure all packages get applied
    while length_count(packages_grouped) > 0:
        # loops through the trucks by truck number
        for truck_number in range(num_trucks):

            if current_route_loc_index[truck_number]:
                # gets the neighbors for the truck selected
                neighbors = get_neighbors(current_route_loc_index[
                                              truck_number], list_of_routes[truck_number], packages_grouped,
                                          distance_and_location, current_route_loc_index)

            # if the results are valid
            if neighbors:
                # gets the next move index value for the truck
                index_next_move = get_next_move(neighbors)
                # sees if the index of the move is a valid move
                if index_next_move != 0:
                    # finds the packages matching the location of the next move
                    index_of_packages = package_loc_match(packages_grouped, list_of_locations[index_next_move])

                    # if the value of the index is valid
                    if index_of_packages is not None:
                        if index_of_packages > -1:

                            # checks to see if the
                            check_deadline = check_for_deadline(packages_grouped[index_of_packages][1])

                            # if the location is already apart of the trucks delivery list
                            check, truck_num = check_if_loc_in(packages_grouped[index_of_packages], list_of_routes)

                            # checks that if there is a deadline that it is not going on the last truck
                            if (check_deadline is True) & (truck_number != 2):

                                # checks to see if the package associated location was already applied to the route
                                if (check == 1) & (not check_for_package(packages_grouped[index_of_packages][1], 31)):

                                    # adds the list to the delivery list
                                    list_of_routes[truck_num].deliveryList[packages_grouped[index_of_packages][0]] += (
                                        packages_grouped[index_of_packages][1])

                                    # loops through the different distances within the column of the store being moved
                                    for distanceToStore in distances:
                                        # sets the distances to -1 so that no truck can travel to the store anymore
                                        distanceToStore[index_next_move] = -1

                                    # sets the index of the truck to be the move of the next index
                                    current_route_loc_index[truck_number] = index_next_move

                                    # adds the length of the packages applied to the routes packages applied amount
                                    list_of_routes[truck_number].packagesApplied += len(
                                        packages_grouped[index_of_packages][1])

                                    # sets the packages grouped value to empty because there is no need to visit
                                    packages_grouped[index_of_packages].clear()

                                else:
                                    # if the move found is not within the the index of the trucks
                                    if index_next_move not in current_route_loc_index:

                                        # checks if the location is already apart of the delivery list
                                        if list_of_locations[index_next_move][1] not in list_of_routes[
                                                truck_number].deliveryList:

                                            # adds the packages to the dictionary
                                            list_of_routes[truck_number].deliveryList[str(
                                                list_of_locations[index_next_move][1])] = \
                                                packages_grouped[index_of_packages][1]

                                        # if the location is already in the dictionary, add the package
                                        else:

                                            # concatenates the list of packages not assigned to the packages already
                                            # applied
                                            list_of_routes[truck_number].delivery_list[
                                                str(list_of_locations[index_next_move][1])] += (
                                                packages_grouped[index_of_packages][1])

                                        # loops through the different distances within the column of the store being
                                        # moved
                                        for distanceToStore in distances:
                                            # sets the distances to -1 so that no truck can travel to the store anymore
                                            distanceToStore[index_next_move] = -1

                                        # sets the index of the truck to be the move of the next index
                                        current_route_loc_index[truck_number] = index_next_move

                                        # adds the length of the packages applied to the routes packages applied amount
                                        list_of_routes[truck_number].packagesApplied += len(
                                            packages_grouped[index_of_packages][1])

                                        # sets the packages grouped value to empty because there is no need to visit
                                        packages_grouped[index_of_packages].clear()

                            else:

                                # checks to see if the associated location was already in the delivery list
                                if (check == 1) & (not check_for_package(packages_grouped[
                                            index_of_packages][1], 31)) & (check_deadline is False):

                                    # adds the list of packages to the delivery list
                                    list_of_routes[truck_num].deliveryList[packages_grouped[index_of_packages][0]] += (
                                        packages_grouped[index_of_packages][1])

                                    # loops through the different distances with the column of the store being moved to
                                    for distanceToStore in distances:
                                        # sets the distances to -1 so that no truck can travel to the store anymore
                                        distanceToStore[index_next_move] = -1

                                    # sets the index of the truck to be the move of the next index
                                    current_route_loc_index[truck_number] = index_next_move

                                    # adds the length of the packages applied to the routes packages applied amount
                                    list_of_routes[truck_number].packagesApplied += len(
                                        packages_grouped[index_of_packages][1])

                                    # sets the packages grouped value to empty because there is no need to visit
                                    packages_grouped[index_of_packages].clear()

                                else:
                                    # if the move found is not within the the index of the trucks
                                    if index_next_move not in current_route_loc_index:

                                        # checks if the location is already apart of the delivery list
                                        if list_of_locations[index_next_move][1] not in list_of_routes[
                                                truck_number].deliveryList:

                                            # adds the packages to the dictionary
                                            list_of_routes[truck_number].deliveryList[str(
                                                list_of_locations[index_next_move][1])] = \
                                                packages_grouped[index_of_packages][1]

                                        # if the location is already in the dictionary, add the package
                                        else:

                                            # concatenates the list of packages not assigned to the packages already
                                            # applied
                                            list_of_routes[truck_number].delivery_list[
                                                str(list_of_locations[index_next_move][1])] += (
                                                packages_grouped[index_of_packages][1])

                                        # loops through the different distances within the column of the store being
                                        # moved
                                        for distanceToStore in distances:
                                            # sets the distances to -1 so that no truck can travel to the store anymore
                                            distanceToStore[index_next_move] = -1

                                        # sets the index of the truck to be the move of the next index
                                        current_route_loc_index[truck_number] = index_next_move

                                        # adds the length of the packages applied to the routes packages applied amount
                                        list_of_routes[truck_number].packagesApplied += len(
                                            packages_grouped[index_of_packages][1])

                                        # sets the packages grouped value to empty because there is no need to visit
                                        packages_grouped[index_of_packages].clear()

                # if there is no where for the truck to go
                else:

                    # gets the index of any packages within the trucks current location
                    temp_package_index = package_loc_match(packages_grouped, list_of_locations[
                        current_route_loc_index[truck_number]])

                    # checking to make sure of valid index values within the list
                    if (temp_package_index is not None) & (packages_grouped[temp_package_index] is not None) & (
                            not check_for_deadline(packages_grouped[temp_package_index][1])):

                        # checking if the list is present, and that the truck can carry the packages
                        if (packages_grouped[temp_package_index][1]) & (
                                len(packages_grouped[temp_package_index[1]]) + list_of_routes[
                                truck_number].packagesApplied < list_of_routes[truck_number].truck.capacity):

                            # checking if the location is already within the dictionary of the delivery list
                            if list_of_locations[current_route_loc_index[truck_number]] in list_of_routes[
                                    truck_number].deliveryList:

                                # adds the list of packages present to the delivery list
                                list_of_routes[truck_number].deliveryList[list_of_locations[
                                    current_route_loc_index[truck_number]]] += (
                                    packages_grouped[temp_package_index][1])

                            # if the location is not in the dictionary
                            else:

                                # sets the list of packages to the value of the key value pair for the dictionary
                                list_of_routes[truck_number].deliveryList[list_of_locations[current_route_loc_index[
                                    truck_number]]] = packages_grouped[temp_package_index][1]

            # if the neighbors value is blank
            else:

                # checks to see if there is space within the truck to add a package
                if list_of_routes[truck_number].packagesApplied < list_of_routes[truck_number].truck.capacity:

                    temp = None

                    # finds the index within the packages matched group
                    if current_route_loc_index[truck_number]:
                        temp = package_loc_match(packages_grouped, list_of_locations[current_route_loc_index[
                            truck_number]])

                    # if the index is valid
                    if temp:

                        # if the list with index is valid
                        if packages_grouped[temp]:

                            # if packages are present within the location
                            if packages_grouped[temp][1]:

                                # checks to see if the truck can fit the packages
                                if len(packages_grouped[truck_number][1]) + list_of_routes[
                                        truck_number].packagesApplied < list_of_routes[truck_number].truck.capacity:

                                    # checks to see if the dictionary has the key present within
                                    if list_of_locations[current_route_loc_index[truck_number]][1] in list_of_routes[
                                            truck_number].deliveryList:

                                        # adds the list to the end of the present list
                                        list_of_routes[truck_number].deliveryList[list_of_locations[
                                            current_route_loc_index[truck_number]][1]].concat(packages_grouped[temp][1])

                                    # otherwise add the key value pair to the dictionary
                                    else:

                                        # adds the value to the dictionary
                                        list_of_routes[truck_number].deliveryList[list_of_locations[
                                            current_route_loc_index[truck_number]][1]] = packages_grouped[temp][1]

                                    # updates the number of packages applied to the route
                                    list_of_routes[truck_number].packagesApplied += len(packages_grouped[temp][1])

                                    # cleans the list and distances to be properly formatted
                                    packages_grouped = clean_list(packages_grouped)
                                    distances = clean_distance(packages_grouped, distances, list_of_locations)

            # cleans the list and distances to be properly formatted
            packages_grouped = clean_list(packages_grouped)
            distances = clean_distance(packages_grouped, distances, list_of_locations)

    # returns the list of routes where every route represents what the truck is doing
    return list_of_routes


# finds the index of packages that have a matching location to the input of the function
def package_loc_match(packages_grouped, location):
    # loops through the packages
    for j in packages_grouped:

        # if the value is valid
        if j:

            # if the location matches
            if (j[0] in location[0]) | (j[0] in location[1]):
                # returns the index of the list
                return packages_grouped.index(j)


# finds the index of the location that matches the address given
def loc_package_match(list_of_locations, address):
    # loops through the locations
    for location_info in list_of_locations:

        # sets the location to the value of the list
        location = location_info[1]

        # checks if the values are matching or if the given address is within the address
        if address in location:
            # returns the index of the matching value
            return list_of_locations.index(location_info)


# loads based on special instructions associated with the package
def load_from_special_instructions(packages_grouped, list_of_routes, list_of_locations, distances):
    # sets default values for the location
    previous_locations = [0 for _ in range(num_trucks)]

    delivered_with = False

    check_for_index = [j for j in range(len(packages_grouped))]
    
    random.shuffle(check_for_index)
    # loops through the groups base don the location
    for index in check_for_index:
        location_group = packages_grouped[index]
        index_temp = packages_grouped.index(location_group)
        # sets the list of packages to the value within the list of the location group

        if location_group:
            if location_group[1]:
                packages_list = location_group[1]
                # loops through the package nodes within the list
                for packagesNode in packages_list:

                    # checks if the special notes are not null and that the package has not already been previously
                    # assigned
                    if (packagesNode.package.specialNotes != "") & (not check_if_in(packagesNode, list_of_routes)):

                        # sets variable to hold the string of the special note
                        specialNotes = packagesNode.package.specialNotes

                        # loops through the routes
                        for tempRoute in list_of_routes:

                            # checks for valid route
                            if tempRoute:

                                # sets the index for the route being edited
                                route_index = list_of_routes.index(tempRoute)

                                # checking for string value to find packages with a special note value to
                                # tell which truck the package needs to be on
                                if (" on truck " + str(tempRoute.truck.truckNo)) in specialNotes:

                                    # checks for a negative (not used within the project)
                                    if "not" in specialNotes:

                                        # loops through the routes
                                        for i in range(list_of_routes):

                                            # checks to make sure route in question does not match otherwise
                                            # loops to find other route that can work
                                            if i != tempRoute.truck.truckNo:

                                                # checks if the key is in the dictionary
                                                if location_group[0] in list_of_routes[i].deliveryList:

                                                    # if the value is already within the dictionary append
                                                    # the packaged node
                                                    list_of_routes[i].deliveryList[str(location_group[0])].append(
                                                        packagesNode)
                                                    list_of_routes[i].packagesApplied += 1

                                                # key val not in dictionary
                                                else:

                                                    # sets the key value pair for the dictionary
                                                    list_of_routes[i].deliveryList[str(location_group[0])] = [
                                                        packagesNode]
                                                    list_of_routes[i].packagesApplied += 1

                                                # removes the applied node from the list so it is not added again
                                                packages_list.remove(packagesNode)

                                                # checking to see if any other packages are associated with the location
                                                if not packages_list:
                                                    # removes the location if there are no packages
                                                    packages_grouped.remove(location_group)

                                                # set previous location to the location of the package applied
                                                previous_locations[tempRoute.truck.truckNo - 1] = loc_package_match(
                                                    list_of_locations, packagesNode.package.address)

                                                # escapes the loop to move on to the next special instruction
                                                break

                                    # if the truck that is listed is the target
                                    else:

                                        # checking if the location is valid
                                        if location_group is not None:

                                            # checking for the key val in the dictionary
                                            if str(location_group[0]) in tempRoute.deliveryList:
                                                tempRoute.deliveryList[str(location_group[0])] += location_group[1]
                                                tempRoute.packagesApplied += len(location_group[1])

                                            # the key val id not within the dictionary
                                            else:

                                                # adds the package node in a list
                                                tempRoute.deliveryList[str(location_group[0])] = location_group[1]
                                                tempRoute.packagesApplied += len(location_group[1])

                                            # set the entire location to empty as there is no reason
                                            # to visit that location
                                            location_group = []

                                            # sets the previous location to the current location
                                            previous_locations[route_index] = loc_package_match(
                                                list_of_locations, packagesNode.package.address)

                                    # saves the adjusted route back into the list of routes
                                    list_of_routes[route_index] = tempRoute

                                # checking for package arrival delays, adds to the last truck
                                elif "will not arrive to depot until" in specialNotes:
                                    # gets the value for when the package is arriving
                                    time_of_arrival = specialNotes[-8:]
                                    # sets the status to the reason for the lateness
                                    packagesNode.package.status = specialNotes[:17]

                                    truck_select = get_rand(0, 0)

                                    # checks to see if the time of arrival is after the point when the
                                    # first trucks leave
                                    if int(time_of_arrival[1]) > 8:
                                        # checks to see if the location is already apart of the trucks delivery list
                                        if location_group:
                                            if str(location_group[0]) in list_of_routes[truck_select].deliveryList:
                                                # if true: adds the package node to the end
                                                if packagesNode not in list_of_routes[truck_select].deliveryList[
                                                        location_group[0]]:
                                                    list_of_routes[truck_select].deliveryList[
                                                        location_group[0]] += location_group[1]
                                                    list_of_routes[truck_select].packagesApplied += len(
                                                        location_group[1])
                                            # if the location is not in the delivery list, add the package
                                            else:
                                                list_of_routes[truck_select].deliveryList[
                                                    location_group[0]] = location_group[1]
                                                list_of_routes[truck_select].packagesApplied += len(
                                                    location_group[1])

                                        location_group = []

                                        # sets the previous location to the location that had just added the package
                                        previous_locations[route_index] = loc_package_match(
                                            list_of_locations, packagesNode.package.address)

                                # checks to see if the package needs to be shipped with other packages
                                elif ("be delivered with" in specialNotes) & (not delivered_with):
                                    # checks to make sure that the packages are not added multiple times
                                    delivered_with = True

                                    # selects a random truck to have the packages grouped together
                                    tempRoute = list_of_routes[0]

                                    # making sure that the location group is not empty
                                    if location_group is not None:

                                        # checks to see if the key val is in the delivery list
                                        if str(location_group[0]) in tempRoute.deliveryList:

                                            # adds the node to the list of dictionary
                                            tempRoute.deliveryList[location_group[0]] += location_group[1]
                                            tempRoute.packagesApplied += len(location_group[1])

                                        # if the key val is not in the dictionary
                                        else:

                                            # adds the key value pair to the dictionary
                                            tempRoute.deliveryList[location_group[0]] = location_group[1]
                                            tempRoute.packagesApplied += len(location_group[1])

                                        # loops through the packages group again to find the other packages
                                        for byLocation in packages_grouped:

                                            # saves the index value
                                            index_loc_temp = packages_grouped.index(byLocation)

                                            # if the location value is not empty
                                            if byLocation:

                                                # if there are packages associated with the location
                                                if byLocation[1] is not None:

                                                    # loops through the associated packages
                                                    for tempNode in byLocation[1]:

                                                        # checks to see if the package id is in the string and
                                                        # that the length is correct of the id
                                                        if (str(tempNode.package.packageId) in specialNotes) & (
                                                                len(str(tempNode.package.packageId)) == 2):

                                                            # checks if the address is an existing key within the
                                                            # dictionary
                                                            if tempNode.package.address in tempRoute.deliveryList:

                                                                # makes sure the package is not already in the list
                                                                if packagesNode not in tempRoute.deliveryList[
                                                                        byLocation[0]]:
                                                                    # adds the value to the end of the packages list
                                                                    tempRoute.deliveryList[byLocation[0]] += byLocation[
                                                                        1]
                                                                    tempRoute.packagesApplied += len(byLocation[1])

                                                            # address is not a key in the dictionary
                                                            else:

                                                                # adds the key value pair to the dictionary
                                                                tempRoute.deliveryList[
                                                                    tempNode.package.address] = byLocation[1]
                                                                tempRoute.packagesApplied += len(byLocation[1])

                                                            byLocation = []

                                                            # sets the previous location to the location that has
                                                            # just added the packages
                                                            previous_locations[list_of_routes.index(
                                                                tempRoute)] = loc_package_match(
                                                                list_of_locations, tempNode.package.address)

                                                            # saves the changes to the list of the packages
                                                            packages_grouped[index_loc_temp] = []

                                            location_group = []

                                            # loops through the different distances within the column of the store
                                            # being moved
                                            for distanceToStore in distances:
                                                # sets the distances to -1 so that no truck can travel to the store
                                                # anymore
                                                distanceToStore[loc_package_match(
                                                    list_of_locations, packagesNode.package.address)] = -1

                                # if the special note labels the package to the correct address and to the last truck
                                elif "Wrong address" in specialNotes:

                                    # load to the last truck that leaves later in the day when the value is updated
                                    if (location_group is not None) & (not check_if_in(packagesNode, list_of_routes)):

                                        # if the key val is within the dictionary
                                        if str(location_group[0]) in list_of_routes[1].deliveryList:

                                            # adds the package to the end of the delivery list
                                            list_of_routes[1].deliveryList[location_group[0]] += location_group[1]
                                            list_of_routes[1].packagesApplied += len(location_group[1])

                                        # no key val in the dictionary
                                        else:

                                            # adds the package node within a list
                                            list_of_routes[1].deliveryList[location_group[0]] = location_group[1]
                                            list_of_routes[1].packagesApplied += len(location_group[1])

                                        # sets the location to the address
                                        previous_locations[1] = loc_package_match(list_of_locations, "410 S State St.")

                                        location_group = []

                        # if the location group is null, set the packages grouped at the index to an empty list
                        if not location_group:
                            packages_grouped[index_temp] = []

    # returns the changed lists of values
    return packages_grouped, list_of_routes, previous_locations, distances


# returns true if the node is within the routes, false if not
def check_if_in(package_node, list_of_routes):
    # goes through the routes
    for route in list_of_routes:

        # sets the temp variable value to the delivery list
        delivery_list_temp = route.deliveryList

        # goes through the key values
        for keys in delivery_list_temp:

            # checks if the node is within the list of the dictionary's key value pair
            if package_node in delivery_list_temp[keys]:
                # if the node is within the list, returns true
                return True

    # if no match was found returns false
    return False


# returns the available spaces from the distances
def find_available_spaces(distances, list_of_packages, list_of_locations, truck_no):
    # finds the list of distances of the last row, because the last row has all the available distances that have
    # values to  see which places can be moved to based on the format
    distance_list = distances[-1]

    # holds the resulting index option
    results = []

    # goes through the values within the distance list
    for distance_val in range(len(distance_list)):

        # checks to see if the distance is able to be traveled to
        if distance_list[distance_val] != -1:
            # adds the index value to the resulting list
            results.append(distance_val)

    # holds the results of the trucks who do not deal with delivery deadlines, and one that does
    final_results = []
    secondary_final_results = []

    # goes through the results
    for index in results:
        index_of_packages = package_loc_match(list_of_packages, list_of_locations[index])

        # checks to see if the results have an associated deadline to handle
        if check_for_deadline(list_of_packages[index_of_packages][1]):
            # adds the found values
            final_results.append(index)

    # if the truck is not the last truck,
    if truck_no != 3:

        # if there are indexes with deadlines
        if final_results:

            # return the indexes associated with the results
            return final_results

        else:
            # with no deadline packages to handle, continue to add the other packages
            return results
    else:
        # goes through the results
        for index in results:
            if final_results:
                # checks to see if the results are not in the final results making it okay for the last truck to be
                # able to add
                if index not in final_results:
                    secondary_final_results.append(index)

        # if there are results
        if final_results:
            # return the unqualified results
            return secondary_final_results

        # with no deadline associated results, just return all other results
        else:
            return results


# goes through the list of the packages to make sure there are no null values
def clean_list(packages_grouped):
    # goes through the packages grouped by location
    for pair in packages_grouped:

        # if there is a location value
        if pair:

            # if there are no packages associated
            if not pair[1]:
                # removes the location group
                packages_grouped.remove(pair)

    # returns the updated packages grouped
    return packages_grouped


# goes through the distances and packages to make sure the distance matrix accurately returns the available moves
def clean_distance(packages_grouped, distances, list_of_locations):
    # goes through the list of locations
    for location in list_of_locations:

        # sets value to see if there is match
        match = False

        # goes through the packages
        for package_group in packages_grouped:

            # if the package group is valid
            if package_group:

                # if the address value is a valid key
                if package_group[0] in location[1]:
                    # shows that there is a valid entry
                    match = True

        # checking if its not a match
        if not match:

            # finds the index of the location to edit the distance matrix as they have parallel values
            distance_index = list_of_locations.index(location)

            # goes through all the rows and at the specified column sets the values to -1 to not be able to travel to
            # that location
            for distance in distances:
                distance[distance_index] = -1

    # returns the updated distances matrix
    return distances


# iterates through the routes to find the best route in terms of total distance covered by the trucks
def route_compare():
    # gets a fresh distance and location value to be able to analyze the routes
    distance_location_pair = FileOpener.distance_file_open()

    # splits the array returned from the file opening and sets it to the two distinct matrices
    distances = distance_location_pair[0]
    list_of_locations = distance_location_pair[1]

    # sets the variables to hold the best route and the distance traveled of the route
    best_distance = -1
    best_route = None

    # loops based on global variable assignment for how many times to create a potential route
    for iterator in range(iteration_num):

        # sets a variable to hold the results of the attempt to load call which returns the number of routes that
        # are set based on the number of trucks
        routes = attempt_to_load()

        # sets the total distance to a counter variable
        routes_total_distance = 0

        # goes through each route and finds the total distance for the route
        for route in routes:
            routes_total_distance += distance_per_route(distances, list_of_locations, route)

        # checks to see if the values for the the distance are more than the previously saved distance
        if (routes_total_distance < best_distance) | (best_distance == -1):
            # sets the values to the best route and the distance of the best route
            best_distance = routes_total_distance
            best_route = routes

    # returns the best route available
    return best_route, best_distance


# returns the distance for a route
def distance_per_route(distances, list_of_locations, route):
    # is a list of keys from the dictionary
    list_of_delivery_keys = list(route.deliveryList)

    # finds the distance from the hub to the first delivery location (and will be added to)
    distance_total = distances[loc_package_match(list_of_locations, list_of_delivery_keys[0])][0]

    # goes through the delivery list by index
    for location_index in range(len(route.deliveryList)):

        # checks to see if the index value is valid (keeps till one before to be able to check the distances
        if location_index < len(route.deliveryList) - 1:

            # finds the first and second index of the list of deliveries by location
            temp_index_1 = loc_package_match(list_of_locations, list_of_delivery_keys[location_index])
            temp_index_2 = loc_package_match(list_of_locations, list_of_delivery_keys[location_index + 1])

            # checks to see if the values are not null
            if (temp_index_1 is not None) & (temp_index_2 is not None):

                # checking for formatting of the distance matrix
                if temp_index_1 > temp_index_2:
                    distance_total += distances[temp_index_1][temp_index_2]
                else:
                    distance_total += distances[temp_index_2][temp_index_1]

    # finally adds the distance from the last stop to the hub to complete the route
    distance_total += distances[loc_package_match(list_of_locations, list_of_delivery_keys[-1])][0]

    # returns the total distance
    return distance_total


# assigns the found routes to the available drivers
def route_by_driver(routes):
    # counter variable
    truck_no = 0

    # sets a class definition for the drivers
    drivers = [ClassDef.Driver(i, []) for i in range(num_drivers)]

    # loops through while the counter is up to the number of trucks
    while truck_no < num_trucks:

        # loops through the drivers to find which routes to apply
        for driver in drivers:

            # checks again within loop to provide an escape from the loop
            if truck_no < num_trucks:

                # if the value is not null
                if driver.routes is None:

                    # sets the first drivers route to the number currently being selected within the loop
                    driver.routes = [routes[truck_no]]

                # if the value is not null
                else:

                    # append the route to the drivers routes array
                    driver.routes.append(routes[truck_no])

                # increments the truck number
                truck_no += 1

            # if the truck no value is too large, escape from the loop
            else:
                break

    # returns the list of drivers with the assigned routes
    return drivers


# finds the time it would take for a route associated truck to travel from the start location to the end location
def time_to_location(start_loc, end_loc, route, distances):
    # sets the variable value for the distance found within the table
    dist_found = 0

    # validates the entries from the user
    if (start_loc is not None) & (end_loc is not None):

        # checking for formatting the matrix to confirm the correct distance value is found
        if start_loc > end_loc:
            dist_found = distances[start_loc][end_loc]
        else:
            dist_found = distances[end_loc][start_loc]

    # returns the found length divided by the trucks speed to find how many hours it would take to travel
    return dist_found / route.truck.speed


# takes a start time and adds a given amount of time (in hours) to the starting time value
def time_add(start_time, length):
    # separates the values from the string passed in into hours and minutes
    start_hours = int(start_time[:2])
    start_min = int(start_time[-2:])

    # finds how many minutes to add
    min_to_add = int(length * 60)

    # makes sure that the minutes value is not greater than 60 so that the time values are correct
    if start_min + min_to_add >= 60:

        # edits values to make sure that the hours are updated as well as the minutes
        hours = start_hours + int((start_min + min_to_add) / 60)
        minute = (start_min + min_to_add) % 60

    # if adding the minutes do not make it to 60
    else:
        # sets the hours and minutes
        hours = start_hours
        minute = start_min + min_to_add

    # makes the format of the hours correct if the value is a single digit
    if len(str(hours)) < 2:
        hours = "0" + str(hours)

    # makes the format of the minutes correct if the value is a single digit
    if len(str(minute)) < 2:
        minute = "0" + str(minute)

    # returns the found final values of the minutes and the hours values
    return str(str(hours) + str(minute))


# assigns time values to the packages and routes based on the routes assigned to the drivers
def time_assign(drivers):
    # gets the distance and location values
    distance_location = FileOpener.distance_file_open()
    distances = distance_location[0]
    list_of_locations = distance_location[1]

    # goes through the drivers
    for driver in drivers:

        # sets the default values to when the day starts
        timeTracker = "0800"

        # goes through the routes assigned to the driver
        for route in driver.routes:

            # goes through each location within the delivery list of the route
            for location_group in range(len(route.deliveryList)):

                # if the group is the first entry and the driver has their first route
                if (location_group == 0) & (driver.routes.index(route) == 0):

                    if drivers.index(driver) != 1:
                        # sets the time to start to 0800 when the work day begins
                        route.route_start_time = '0800'
                    else:
                        route.route_start_time = "0800"

                    # goes through the packages within the delivery list
                    for packageNode in list(route.deliveryList.values())[location_group]:
                        # sets the start time for the delivery to the route start value
                        packageNode.package.route_start = route.route_start_time

                        # finds the time to take a driver to get from the hub to the first location
                        packageNode.package.delivered = time_add(packageNode.package.route_start, time_to_location(
                            0, loc_package_match(list_of_locations, packageNode.package.address), route, distances))

                        # sets the variable time tracker to the value found to be built upon later within the loop
                        timeTracker = packageNode.package.delivered

                # if it is the first stop and NOT the driver's first route
                elif location_group == 0:

                    # sets the start time for the later route to the end time of the previous route
                    route.route_start_time = driver.routes[driver.routes.index(route) - 1].route_end_time

                    # goes through the packages within the location
                    for packageNode in list(route.deliveryList.values())[location_group]:
                        # sets the start time for the package to the start time of the route
                        packageNode.package.route_start = route.route_start_time

                        # finds the distance from the first location from the hub
                        packageNode.package.delivered = time_add(packageNode.package.route_start, time_to_location(
                            0, loc_package_match(list_of_locations, packageNode.package.address), route, distances))

                        # updates the time tracker value to keep track later during the route
                        timeTracker = packageNode.package.delivered

                # if it is not the first stop then run this section
                else:

                    # finds the value of the delivery time of the package base off of the current location
                    # and the previous location
                    deliveryTime = time_add(timeTracker, time_to_location(loc_package_match(
                        list_of_locations, list(route.deliveryList)[location_group - 1]), loc_package_match(
                        list_of_locations, list(route.deliveryList)[location_group]), route, distances))

                    # goes through the packages within the location
                    for packageNode in list(route.deliveryList.values())[location_group]:
                        # sets the start time to the route start time as all packages leave the hub at the same time
                        packageNode.package.route_start = route.route_start_time

                        # sets the value of the package delivery to the found time
                        packageNode.package.delivered = deliveryTime

                    # updates the value of the time tracker to be able to use in the loop the next time
                    timeTracker = deliveryTime

            # after making it through the loop of the route, finds the distance from the last stop to the hub and sets
            # that found value to the end time of the route to know when the next route should start
            route.route_end_time = time_add(timeTracker, time_to_location(
                loc_package_match(list_of_locations, list(route.deliveryList)[-1]), 0, route, distances))


# finds the packages' status by the time value passed into the function
def print_by_time(time):
    # goes through the list of packages based on the number of packages
    for i in range(num_packages + 1):

        # searches for and assigns the value to a node based on the id key value
        temp = hasher.hashSearch(packages_hashed, i)

        # if the value returned is a valid node
        if temp:

            # checks to see if the time the user requests is before the start time of the route
            if time_compare(time, temp.package.route_start):

                # sets the status of the package to at hub as the truck has not left yet
                temp.package.deliveryStatus = "At Hub"

            # if the user's time input is after the start time of the route
            else:

                # if the time entered is before the delivery time of the package set status to enroute
                if time_compare(time, temp.package.delivered):
                    temp.package.deliveryStatus = "Enroute to Location"

                # if the time entered is after or equal to the time of delivery, set the status to be
                # delivered with the time
                else:
                    temp.package.deliveryStatus = "Package delivered at " + temp.package.delivered

            # displays to the user the delivery status and the package id
            print("Package ID: ", temp.package.packageId, " \t Delivery Status: ", temp.package.deliveryStatus,
                  "\t Deadline: ", temp.package.deadline)


# checks which time is before, if the first time is before, return true
def time_compare(time1, time2):
    # parses the time values passed into the function into hour and minute values
    hour1 = int(time1[:2])
    min1 = int(time1[-2:])
    hour2 = int(time2[:2])
    min2 = int(time2[-2:])

    # if the hour value of the time is already greater there is no further need for checking, return true
    if hour1 < hour2:
        return True

    # if the hour value is the same for both time values
    elif hour1 == hour2:

        # then checks the time value to see if the minutes value is smaller
        if min1 < min2:
            return True

        # the minute value is larger
        else:
            return False

    # the second hour value is larger
    else:
        return False


# checks to make sure that all package's deadlines are met
def check_deadlines(routes):
    for route in routes:
        if route is not None:
            for location_group in list(route.deliveryList.values()):
                for package_node in location_group:
                    # goes through all packages and checks if the deadline requirements are being met
                    if package_node.package.deadline != "EOD":
                        if time_compare(package_node.package.deadline[:-2], package_node.package.delivered):
                            return False

    # if all delivery times are able to be met with delivery standards
    return True


# defines the user interface for the program user to be able to interact with the data and calculations
def interface():

    # defines the routes at the first run (preliminary)
    routes, distance = route_compare()

    # assigns drivers, and times to the routes
    drivers = route_by_driver(routes)
    time_assign(drivers)

    # sets a value to see if the deadlines have been met
    check = check_deadlines(routes)

    # loops until the requirements for the overall routes have been met
    while (distance > 140) | (not check):
        routes, distance = route_compare()
        drivers = route_by_driver(routes)
        time_assign(drivers)
        check = check_deadlines(routes)

    # sets value to check if the user would like to escape the program
    exit_check = False

    # loops until user presses non specific key
    while not exit_check:

        # displays the options to the user
        print("Main Menu")
        print("1. Create New Route")
        print("2. Check Package Status")
        print("3. Lookup Package Status at a time")
        print("4. Print total mileage of the trucks")
        print("Press any other key to exit")

        # used for spacing
        print("")

        # gathers user input
        user_input = input("Please select an option 1-4")

        # checking what the user input
        if user_input == "1":

            # generates a new route configuration
            routes, distance = route_compare()
            drivers = route_by_driver(routes)
            time_assign(drivers)

            # tells user of the success
            print("Route Created")

        elif user_input == "2":
            # allows user to input package id to search for information on the package requested
            package_id = int(input("Please enter a Package ID to check"))

            # looks up the information for the package
            temp = hasher.hashSearch(packages_hashed, package_id)

            print()

            # displays to the user the various information of the selected package
            print('The package selected has an id of ', temp.package.packageId)
            print("The address of the package is ", temp.package.address)
            print("The package left the Hub at ", temp.package.route_start)
            print("The package arrived at the destination at", temp.package.delivered)

            # if the value returned is a valid node
            if temp:
                # sets the delivery status to the most recent time check
                temp.package.deliveryStatus = "Package delivered at " + temp.package.delivered

            # displays the status
            print("The status of the package is ", temp.package.deliveryStatus)

            # checks if the package has a deadline, and if so displays to the user
            if temp.package.deadline != "":
                print("The delivery deadline is ", temp.package.deadline)

            # if the package has an associated special note, then print the special note
            if temp.package.specialNotes != "":
                print("The special notes are ", temp.package.specialNotes)

        # time check
        elif user_input == "3":

            # user input for which time they would like to view the status
            time = input("Please insert a time (in the military time format (0800) for 8:00am)")

            print()

            # checks the formatting of the time entered
            if len(time) == 4:
                print_by_time(time)
            else:
                # invalid time message
                print("Please enter a valid time!")

                # user input for which time they would like to view the status
                time = input("Please insert a time (in the military time format (0800) for 8:00am)")

                # loops until the time value is valid
                while len(time) != 4:
                    if len(time) == 4:
                        print_by_time(time)
                    else:
                        print("Please enter a valid time!")

        # displays the total distance traveled by all trucks
        elif user_input == "4":
            print('The total mileage traveled by the trucks is ', distance)

        # if the user has submitted a different key, then exit loop and program
        else:
            exit_check = True

        # used for spacing of the main menu in-between selections
        print()
        print("_______________________")
        print()
