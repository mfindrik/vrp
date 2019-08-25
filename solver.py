#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from operator import itemgetter

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y','angle','dist'])

def getKey(customer):
    return customer.angle


def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

# Solution 1: 387
# Solution 2: 1019
# Solution 3: 713
# Solution 4: 1193
# Solution 5: 3719
# Solution 6: 2392
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    customers = []

    # the depot is always the first customer in the input
    line = lines[1]
    parts = line.split()
    x = float(parts[1])
    y = float(parts[2])
    customers.append(Customer(0,int(parts[0]),x,y,0,0))


    for i in range(2, customer_count+1):
        line = lines[i]
        parts = line.split()
        x = float(parts[1])
        y = float(parts[2])
        dist = math.sqrt((customers[0].x - x)**2 + (customers[0].y - y)**2)
        angle = math.atan2(customers[0].y - y,customers[0].x - x)
        if ( angle < 0 ): angle = angle + 2*math.pi
        customers.append(Customer(i-1, int(parts[0]),x,y,angle,dist))


    #the depot is always the first customer in the input
    depot = customers[0] 

    # Categorize customers depending on their angle
    sorted_by_angle = sorted(customers,key=getKey)

    remaining_customers = sorted_by_angle.copy()
    remaining_customers.remove(depot)
    vehicle_clusters = []

    print(remaining_customers)

    # Assign customers to clusters
    for v in range(0,vehicle_count):
        vehicle_clusters.append([])
        remaining_capacity = vehicle_capacity
        used = []
        for customer in remaining_customers:
            if ( customer.demand <= remaining_capacity):
                vehicle_clusters[v].append(customer.index)
                remaining_capacity = remaining_capacity - customer.demand
                used.append(customer)
            else:
                break
        remaining_customers.remove(used)

    print(vehicle_clusters)



    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands
    vehicle_tours = []
    
    remaining_customers = set(customers)
    remaining_customers.remove(depot)
    
    for v in range(0, vehicle_count):
        # print "Start Vehicle: ",v
        vehicle_tours.append([])
        capacity_remaining = vehicle_capacity
        while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
            used = set()
            order = sorted(remaining_customers, key=lambda customer: -customer.demand)
            for customer in order:
                if capacity_remaining >= customer.demand:
                    capacity_remaining -= customer.demand
                    vehicle_tours[v].append(customer)
                    # print '   add', ci, capacity_remaining
                    used.add(customer)
            remaining_customers -= used

    # checks that the number of customers served is correct
    assert sum([len(v) for v in vehicle_tours]) == len(customers) - 1

    # Sweep algorithm: sweap with angle 0
    # Cluster until capacity is reached
    # solve TSP in each cluster
    # for customer in customers:

    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot,vehicle_tour[0])
            for i in range(0, len(vehicle_tour)-1):
                obj += length(vehicle_tour[i],vehicle_tour[i+1])
            obj += length(vehicle_tour[-1],depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

    return outputData


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

