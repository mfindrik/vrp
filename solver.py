#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from operator import itemgetter
import tsp
Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y', 'angle', 'dist'])


def assignNewRoute(vehicle_tour,order):
    l = len(vehicle_tour)
    newRoute = []
    for i in range(1,l+1):
        indexToTake = order[i]
        customer = vehicle_tour.__getitem__(indexToTake-1)
        newRoute.append(customer)
    return newRoute


def getKey(customer):
    return customer.angle


def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x) ** 2 + (customer1.y - customer2.y) ** 2)


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
    print(parts)
    # the depot is always the first customer in the input
    line = lines[1]
    parts = line.split()
    x = float(parts[1])
    y = float(parts[2])
    customers.append(Customer(0, int(parts[0]), x, y, 0, 0))

    for i in range(2, customer_count + 1):
        line = lines[i]
        parts = line.split()
        x = float(parts[1])
        y = float(parts[2])
        dist = math.sqrt((customers[0].x - x) ** 2 + (customers[0].y - y) ** 2)
        angle = math.atan2(customers[0].y - y, customers[0].x - x)
        if (angle < 0): angle = angle + 2 * math.pi
        customers.append(Customer(i - 1, int(parts[0]), x, y, angle, dist))

    # the depot is always the first customer in the input
    depot = customers[0]

    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands
    vehicle_tours = []
    tour_coord_opt = []

    remaining_customers = set(customers)
    remaining_customers.remove(depot)

    for v in range(0, vehicle_count):
        # print "Start Vehicle: ",v
        vehicle_tours.append([])
        tour_coord_opt.append([])
        capacity_remaining = vehicle_capacity
        while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
            used = set()
            order = sorted(remaining_customers, key=lambda customer: customer.angle)
            for customer in order:
                if capacity_remaining >= customer.demand:
                    capacity_remaining -= customer.demand
                    vehicle_tours[v].append(customer)
                    tour_coord_opt[v].append((customer.x,customer.y))
                    # print '   add', ci, capacity_remaining
                    used.add(customer)
            remaining_customers -= used

    # checks that the number of customers served is correct
    assert sum([len(v) for v in vehicle_tours]) == len(customers) - 1

    # Solve TSP for each cluster
    optimization = True
    if ( optimization ):
        for v in range(0, vehicle_count):
            print(len(vehicle_tours[v]),v,v/vehicle_count)
            if ( vehicle_tours[v].__len__() > 1  ):
                if ( customer_count == 421 and len(vehicle_tours[v]) > 15 ): continue
                tour_coord_opt[v].insert(0,(depot.x,depot.y))
                t = tsp.tsp(tour_coord_opt[v])
                optimized_tour = assignNewRoute(vehicle_tours[v],t[1])
                vehicle_tours[v] = optimized_tour






    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot, vehicle_tour[0])
            for i in range(0, len(vehicle_tour) - 1):
                obj += length(vehicle_tour[i], vehicle_tour[i + 1])
            obj += length(vehicle_tour[-1], depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join(
            [str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

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

        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

