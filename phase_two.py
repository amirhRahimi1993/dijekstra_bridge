import numpy as np
import heapq
import concurrent.futures as futures
import math
""" IN THIS PHASE WE ASSUME WE HAVE A REMARKABLE NUMBER OF PORT AND BRIDGES
Although we can use dijekstra for this algorithm, I prefer using better algorithm. if user want to use bridge, 
and his/her home was on A and shop was on B. if we find any bridge between them it is nearest path and if we can find we should find nearest bridge
near A or B. For port we should calculate 4 port. 
1- nearest port to the A and between A and B
2- nearest port to the B and between A and B
3- nearest port to the B but not between A and B
4-nearest port to the A but not between A and B
For this purpose first we sort bridges and ports(we assume inputs are not sorted) then by binary search we find these 4 value for port and 4 value for bridge
This code is  implemented parallel(dijkstra cant run parallel) so
1- If inputs are sorted the order is reduced to O(shop * home * log(bridge)) + O(shop * home * log(port)) because 
this implemntation is parallel the order reduced to O(log(bridge)) + O(log(port))
2- If inputs are NOT sorted the order is reduced to O(shop * home * bridge log(bridge)) + O(shop * home * port *log(port)) because 
this implemntation is parallel the order reduced to O(bridge*log(bridge)) + O(port *log(port))
"""
class create_graph:
    def __init__(self,house_array, shop_array , port_bridge , port,mover =[-1,0,1]):
        self.house_array = sorted(house_array)
        self.shop_array = sorted(shop_array)
        self.adj_list = {}
        self.memory = {}
        self.port = port
        self.path = {}
        self.home_to_shop = {}
        self.port_bridge = sorted(port_bridge)
        self.mover = mover
        self.bridge_port_length = 3 if self.port else 4
        self.to_beach = 2 if self.port else 1
    def __binary_search(self,target,start_index,end_index):
        mid = int((start_index + end_index)/2)
        if start_index> end_index:
            return [end_index,start_index]
        if self.port_bridge[mid] == target:
            return [mid,mid]
        if target > self.port_bridge[mid]:
            start_index = mid + 1
        else:
            end_index = mid - 1
        return self.__binary_search(target, start_index, end_index)

    def __find_good_route(self,A,B):
        start_house, end_house = self.__binary_search(A, 0, len(self.port_bridge)-1)
        indexes = [start_house,end_house]
        start_shop, end_shop = self.__binary_search(B, 0, len(self.port_bridge)-1)
        indexes +=[start_shop, end_shop]
        indexes = sorted(indexes)
        return indexes , A, B
    def calculate_distance(self):
        mul = (2, 1, 1) if self.port else (1, 1, 1)

        for i in range(len(self.house_array)):
            for j in range(len(self.shop_array)):
                indexes , house_value, shop_value =self.__find_good_route(self.house_array[i],self.shop_array[j])
                self.__graph_pair_pair(house_value, indexes, shop_value, mul)
        return self.home_to_shop, self.path
    def __graph_pair_pair(self,first,indexes,third,mul):
        for i in range(len(indexes)):
            if indexes[i] == -1 or indexes[i] >=len(self.port_bridge):
                continue
            second = self.port_bridge[indexes[i]]
            home_shop_key = "{0}_{1}".format(first,third)
            length = ((math.fabs(second - first)  + self.to_beach) * mul[0]) + (self.bridge_port_length * mul[1]) + ((math.fabs(third - second)  + self.to_beach) * mul[2])
            if self.port:
                length += 2
            if (home_shop_key in self.home_to_shop.keys()) == False:
                self.home_to_shop[home_shop_key] = [third,length]
                self.path[home_shop_key]=[first,second,third]
            elif self.home_to_shop[home_shop_key][0] > length:
                self.home_to_shop[home_shop_key] = [third , length]
                self.path[home_shop_key] = [first, second, third]
    def bridge_to_shop(self,bridge,shop):
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

