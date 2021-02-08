# Class definition for the route a truck takes, holds the truck, the delivery list (dictionary with location as key and
# list of packages as the associated values) and packages applied which holds the total number of packages that the
# truck is carrying
class Route:
    def __init__(self, truck, deliveryList):
        self.truck = truck
        self.deliveryList = deliveryList
        self.packagesApplied = 0
        self.route_start_time = "0000"
        self.route_end_time = "0000"


# Class definition for the truck, holds the truck number and the capacity of the truck, as well as the speed(mph)
class Truck:
    capacity = 16
    speed = 18

    def __init__(self, truckNo):
        self.truckNo = truckNo


# Class definition for the packages, holds all values to be associated with the package, the special notes are a string
# of semi-formatted values to be added to the trucks, the address is the first and second lines of the address, as the
# city, state, and zipcode are saved in their own separate variables, wight and delivery status are also saved to the
# class with a default value assigned to the package
class Package:
    def __init__(self, packageId, address, city, state, zipCode, deadline, weight, specialNotes):
        self.specialNotes = specialNotes
        self.address = address
        self.packageId = packageId
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.deadline = deadline
        self.weight = weight
        self.deliveryStatus = "At Hub"
        self.route_start = '0000'
        self.delivered = '0000'


# Class definition for the node to hold the package and a pointer to other nodes
class PackageNode:
    def __init__(self, package):
        self.package = package
        self.next = None


# class definition for the driver which holds the route the driver takes and the driver's number
class Driver:
    def __init__(self, driver_no, routes):
        self.routes = routes
        self.driver_no = driver_no
