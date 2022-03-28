import numpy as np
import heapq
import concurrent.futures as futures
import math

""" THIS IS PHASE ONE, WE SOLVE PROBLEM IN THE SIMPLEST WAY. WE ASSUME THAT WE DO NOT HAVE A REMARKABLE NUNBER OF PORT AND BRIDGE. SO OUR APPROACH IS BRUTE FORCE ALGORITHM
in this phase we assume that
we have just one river and arbitrary
number of ports and bridges
also we assume that each pedestrian or rider can go top bottom
left and right not cross(because question indirectly impose this assume)
"""
class create_graph:
    def __init__(self,house_array, shop_array , port_bridge , port,mover =[-1,0,1]):
        self.house_array = house_array
        self.shop_array = shop_array
        self.adj_list = {}
        self.port = port
        self.path = {}
        self.home_to_shop = {}
        self.port_bridge = port_bridge
        self.mover = mover
        self.bridge_port_length = 3 if self.port else 4
        self.to_beach = 2 if self.port else 1

    def calculate_distance(self):
        mul = (2, 1, 2) if self.port else (1, 1, 1)
        self.__graph_pair_pair(self.house_array, self.port_bridge, self.shop_array, mul)
        return self.home_to_shop, self.path
    def __graph_pair_pair(self,first,second,third,mul):
        for i in range(len(first)):
            for j in range(len(second)):
                for k in range(len(third)):
                    home_shop_key = "{0}_{1}".format(first[i],third[k])
                    length = ((math.fabs(second[j] - first[i])  + self.to_beach) * mul[0]) + (self.bridge_port_length * mul[1]) + ((math.fabs(third[k] - second[j])  + self.to_beach) * mul[2])
                    if (home_shop_key in self.home_to_shop.keys()) == False:
                        self.home_to_shop[home_shop_key] = [third[k],length]
                        self.path[home_shop_key]=[first[i],second[j],third[k]]
                    elif self.home_to_shop[home_shop_key][0] > length:
                        self.home_to_shop[home_shop_key] = [third[k] , length]
                        self.path[home_shop_key] = [first[i], second[j], third[k]]
    def bridge_to_shop(self):
        pass
    def port_to_shop(self):
        pass
    def home_to_river(self):
        pass
"""
get data from file
"""
x_input = {"house_number":-1,"house_array":[],"shop_number":-1,"shop_array":[],"bridge_number":-1,"bridge_array":[],"port_number":-1,"port_array":[]}
keys = list(x_input.keys())
index = 0
text = open("input.txt")
for l in text.readlines():
    l = l.replace("\n","")
    key = keys[index]
    if index %2 ==0:
        x_input[key] = int(l)
    else:
        x_input[key] = l.split(" ")
        x_input[key] = list(map(int, x_input[key]))
    index+=1
bridge_graph = create_graph(x_input["house_array"],x_input["shop_array"],x_input["bridge_array"],port =False)
home_to_shop_bridge , path_bridge = bridge_graph.calculate_distance()
port_graph = create_graph(x_input["house_array"],x_input["shop_array"],x_input["port_array"],port =True)
home_to_shop_port , path_port = port_graph.calculate_distance()
for k in home_to_shop_port.keys():
    distance = min(home_to_shop_bridge[k][1],home_to_shop_bridge[k][1])
    print("{0} : {1}".format(k,distance))
    path = path_bridge[k] if distance == home_to_shop_bridge[k][1] else path_port[k]
    print(path)
"""
get data from input
"""
# house_number = int(input())
# house_array = input().split(" ")
# house_array = list(map(int, house_array))
# shop_number = int(input())
# shop_array = input().split(" ")
# shop_array = list(map(int, shop_array))
# bridge_number = int(input())
# bridge_array = input().split(" ")
# bridge_array = list(map(int, bridge_array))
# port_number = int(input())
# port_array = input().split(" ")
# port_array = list(map(int, port_array))

