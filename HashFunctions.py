# sets a variable to hold the table size value
table_size = 23


# defines hash function
def Hash(key):
    return (key * 2654435761 % 2 ** 32) % table_size


# goes through the hashed list and finds the package with the associated key
def listSearch(hashedList, packageIdKey):

    # checks to make sure that the key and list are valid entries
    if (packageIdKey != 0) & (hashedList is not None):

        # checks to see if the first value in the list matches the search
        if hashedList.package.packageId == packageIdKey:

            # returns the desired node
            return hashedList

        # if there is no match found, it loops through the pointer list
        while hashedList.next is not None:

            # checks to see if the value is the correct value
            if hashedList.package.packageId == packageIdKey:

                # returns correct node
                return hashedList

            # if the match is not present
            else:

                # goes to the next item in the linked list
                temp = hashedList.next.next
                hashedList = hashedList.next
                hashedList.next = temp

        # checks to see if the current value is the match being sought
        if hashedList.next is None:
            if hashedList.package.packageId == packageIdKey:
                return hashedList

            # if no match is found, return None
            else:
                return None

        # if no match is found, return None
        else:
            return None

    # if no match is found, return None
    else:
        return None


# adds a node to the hashed list
def listAppend(hashedList, node):

    # finds the end of the list by going through to find the next value that is null
    while hashedList.next is not None:
        temp = hashedList.next.next
        hashedList = hashedList.next
        hashedList.next = temp

    # once it finds the end of the list, set the next value to the desired node
    hashedList.next = node


# removes a desired node from the list
def listRemove(hashedList, node):

    # checks to see if the package id is a match
    if hashedList.package.packageId == node.package.packageId:

        # removes the value from the list by having the pointer before point to the point after the target
        temp = hashedList.next.next
        hashedList = hashedList.next
        hashedList.next = temp

        # returns the new list
        return hashedList

    # loops through the hashed list to find the matching desired package id
    while (hashedList.next is not None) & (hashedList.next.package.packageId != node.package.packageId):
        temp = hashedList.next.next
        hashedList = hashedList.next
        hashedList.next = temp

    # returns with end of list (val not found) or when the target node is left
    if hashedList.next is not None:

        hashedList.next = hashedList.next.next
        return True
    # if there was no .next package node then the node to be searching for has not been found as the value is the
    # .next value
    else:
        return False


# inserts the node into the hash table
def hashInsert(hashTable, packageNode):

    # finds the associates hashed list by hashing the package's id
    hashList = hashTable[Hash(packageNode.package.packageId)]

    # checks to make sure that the node is valid
    if packageNode is not None:

        # checks to see if the list is empty
        if hashList is None:

            # if empty set the value to the node and set the .next value to None
            hashList = packageNode
            hashList.next = None

            # update the hash table based on the new hashed list
            hashTable[Hash(packageNode.package.packageId)] = hashList

            # return the new table
            return hashTable

        # if the list is not empty
        else:

            # checks to make sure that the package is not already in the list
            if hashSearch(hashTable, packageNode.package.packageId) is None:

                # checks package id for valid value
                if packageNode.package.packageId != 0:

                    # adds the node to the list
                    listAppend(hashList, packageNode)

                # catching invalid package ids
                else:
                    print("tried to insert package with id val of 0")
                    return hashTable

            # if the list already has values in it
            else:

                # loops through the hashed list and finds the next empty slot
                while hashList.next is not None:
                    temp = hashList.next.next
                    hashList = hashList.next
                    hashList.next = temp

                # adds the node to the found empty spot
                hashList.next = packageNode

    # catches error for null nodes
    else:
        print("Package Node is None")

    # returns the updated hash table
    return hashTable


# removes a node from the hashed table
def hashRemove(hashTable, item):

    # finds the list that would contain the node based on hashing the id
    hashedList = hashTable[Hash(item.packageId)]

    # searches for the node associated to the passed in package
    itemNode = listSearch(hashedList, item.packageId)

    # checks for valid entry
    if itemNode is not None:

        # removes the found node from the list
        hashedList = listRemove(hashedList, itemNode)

    # updates the table to have the list reflect the list
    hashTable[Hash(item.packageId)] = hashedList

    # returns the updated hashed table
    return hashTable


# searches through the hashed table to find the node that has the desired key
def hashSearch(hashTable, key):

    # finds the list associated with the hashed key value
    hashedList = hashTable[Hash(key)]

    # checks for null list
    if hashedList is not None:

        # checks for invalid package id
        if hashedList.package.packageId != 0:

            # finds the node associated
            itemNode = listSearch(hashedList, key)

            # checks for null result
            if itemNode is not None:

                # checks for proper retrieval of the item node
                if itemNode.package.packageId != 0:

                    # returns the resulting node
                    return itemNode

                # if the return was an invalid package id
                else:
                    return None

            # if the return was none
            else:
                return None

    # if the associated hashed list is empty
    else:
        return None


# returns the number of associated nodes of the hashed table
def hash_table_length(hashTable, tableLength):

    # counter variable, holds num of nodes
    count = 0

    # loops through the length of the hashed table
    for i in range(tableLength):

        # finds the first node within the table
        startNode = hashTable[i]

        # checks for valid node retrieval
        if startNode is not None:

            # because a node was found, add 1 to the value
            count += 1

            # goes through the length of the list
            while startNode.next is not None:

                # formula to find the next node
                temp = startNode.next.next
                startNode = startNode.next
                startNode.next = temp

                # adds to the count as a node has been found
                count += 1

    # returns the final count of the node
    return count
