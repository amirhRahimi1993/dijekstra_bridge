import numpy as np
import heapq
import concurrent
import math
""" IN THIS PHASE WE ASSUME WE HAVE A REMARKABLE NUMBER OF PORT AND BRIDGES AND WE HAVE MORE THAN 1 RIVER
CAUTION1: BECAUSE INPUT IS INCOMPATIBLE TO OUR OUTPUT, I CAHNGED INPUT AS FOLLOW:
AFTER SHOP-INPUTS, WE HAVE EXTRA NUMBER THAT POINT TO THE NUMBER OF RIVERS AND FOLLOW THAT WE HAVE PORT AND BRIDGE INPUTS
CAUTION2: WE ASSUME THAT DISTANCE BETWEEN EACH RIVER IS 2
ALGORITHM:
For solving problem, first we prune or graph. 
we use phase 2 in each layer to reduce number of edges from approximately V^2 to V-1.
After that Dijkstra is used. therefore the order reduce to O(VlogV) instead of O((V + E)logV)
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
        if len(self.port_bridge) != 0:
            self.bridge_port_length = 3 if self.port else 4
            self.to_beach = 2 if self.port else 1
        else:
            self.bridge_port_length = 0
            self.to_beach = 1
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
        if len(self.port_bridge) != 0:
            mul = (2, 1, 1) if self.port else (1, 1, 1)
        else:
            mul = (2, 1) if self.port else (1, 1)
        for i in range(len(self.house_array)):
            for j in range(len(self.shop_array)):
                if len(self.port_bridge)!=0:
                    indexes , house_value, shop_value =self.__find_good_route(self.house_array[i],self.shop_array[j])
                    self.__graph_pair_pair(house_value, indexes, shop_value, mul)
                else:
                    self.__simple_pair(self.house_array[i],self.shop_array[j])
        return self.home_to_shop, self.path
    def __simple_pair(self,first,third):
            home_shop_key = "{0}_{1}".format(first,third)
            length = (third - first)
            if (home_shop_key in self.home_to_shop.keys()) == False:
                self.home_to_shop[home_shop_key] = [third,length]
                self.path[home_shop_key]=[first,third]
            elif self.home_to_shop[home_shop_key][0] > length:
                self.home_to_shop[home_shop_key] = [third , length]
                self.path[home_shop_key] = [first, third]
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
class initiate_process:
    def __init__(self,address="input_for_phase3.txt",bridge_base ="bridge_array",port_base="port_array"):
        self.bridge_base =bridge_base
        self.port_base=port_base
        self.x_input = {"house_number":-1,"house_array":[],"shop_number":-1,"shop_array":[]}
        self.keys = list(self.x_input.keys())
        index = 0
        text = open(address)
        self.river_number = 0
        for l in text.readlines():
            l = l.replace("\n","")
            if index <4:
                key = self.keys[index]
                if index %2 ==0 :
                    self.x_input[key] = int(l)
                else:
                    self.x_input[key] = l.split(" ")
                    self.x_input[key] = list(map(int, self.x_input[key]))
            elif index == 4:
                self.river_number = int(l)
                index+=1
                continue
            elif index >4 and index%2 == 0:
                if (index-4)%4 != 0:
                    indexkey = int((index-4)/4)
                    key = bridge_base+"_{0}".format(indexkey)
                else:
                    indexkey = int((index - 4) / 4) - 1
                    key = port_base + "_{0}".format(indexkey)
                self.x_input[key] = l.split(" ")
                self.x_input[key] = list(map(int, self.x_input[key]))
            index+=1
        self.key_array_bridge =["house_array"]
        self.key_array_port = ["house_array"]
        for k in self.x_input.keys():
            if "port_array" in k:
                self.key_array_port.append(k)
            elif "bridge_array" in k:
                self.key_array_bridge.append(k)
        self.key_array_bridge.append("shop_array")
        self.key_array_port.append("shop_array")

    def adj_list(self,first_key,third_key,home_graph_value,adj_list_dict):
        for k in home_graph_value.keys():
            vertex1 = k.split("_")[0]
            vertex2 = k.split("_")[1]
            key = first_key + "-{0}".format(vertex1)
            distant = third_key + "-{0}".format(vertex2)
            if (key in adj_list_dict.keys()) == False:
                adj_list_dict[key] = [[home_graph_value[k][-1] , distant]]
            else:
                adj_list_dict[key].append([home_graph_value[k][-1], distant])
        return adj_list_dict
    def pruner(self,key_array,port):
        adj_list_dict = {}
        for i in range(0,len(key_array)-2,2):
            first_key = key_array[i]
            try:
                second_key = key_array[i+1]
            except:
                break
            try:
                third_key = key_array[i + 2]
                graph = create_graph(self.x_input[first_key],self.x_input[third_key],self.x_input[second_key],port =port)
                home_graph_value , path_graph = graph.calculate_distance()
                if port==False:
                    adj_list_dict =self.adj_list(first_key,third_key,home_graph_value,adj_list_dict)
                else:
                    adj_list_dict = self.adj_list(first_key, third_key, home_graph_value, adj_list_dict)
            except:
                graph = create_graph(self.x_input[first_key], self.x_input[second_key], [], port=port)
                home_graph_value, path_graph = graph.calculate_distance()
                if port==False:
                    adj_list_dict = self.adj_list(first_key, second_key, home_graph_value, adj_list_dict)
                else:
                    adj_list_dict = self.adj_list(first_key, second_key, home_graph_value, adj_list_dict)
        return adj_list_dict
    def start_process(self,port):
        return self.pruner(self.key_array_bridge,port)
class dijekstra:
    def __init__(self,adj_list):
        self.adj_list = adj_list
    def __itreator(self,key):
        self.distances = {}
        self.distances[key] = 0
        self.key = key
        heap = []
        heapq.heappush(heap,[0,self.key])
        Finisher = {}
        while len(heap)!=0:
            initial_key = heap.pop()
            Finisher[initial_key[1]] = True
            self.distances[initial_key[1]] = initial_key[0]
            if initial_key[1] in self.adj_list.keys():
                for i in range(len(self.adj_list[initial_key[1]])):
                    distance_key, distance_value = self.adj_list[initial_key[1]][i][1] , self.adj_list[initial_key[1]][i][0]
                    if distance_key in Finisher.keys():
                        continue
                    if (distance_key in self.distances.keys()) == False:
                        self.distances[distance_key] = distance_value+ initial_key[0]
                    else:
                        if self.distances[distance_key] > distance_value + initial_key[1]:
                            self.distances[distance_key] = distance_value + initial_key[0]
                        else:
                            continue
                    heapq.heappush(heap, [self.distances[distance_key],distance_key])
        return self.distances
    def calculate_distance(self):
        all_distance = {}
        keys = list(self.adj_list.keys())
        for k in keys:
            if "house_array" in k:
                all_distance[k] = self.__itreator(k)
        return all_distance
def main():
    initiate_values = initiate_process("input_for_phase3.txt")
    adj_list_dict_bridge = initiate_values.start_process(False)
    adj_list_dict_port = initiate_values.start_process(True)
    bridge_dijekstra =dijekstra(adj_list_dict_bridge)
    bridge_distance = bridge_dijekstra.calculate_distance()
    port_dijekstra = dijekstra(adj_list_dict_port)
    port_distance = port_dijekstra.calculate_distance()
    for k in bridge_distance.keys():
        for shop_key in bridge_distance[k].keys():
            if "shop_array" in shop_key:
                if port_distance[k][shop_key] < bridge_distance[k][shop_key]:
                    way = "port"
                else:
                    way = "bridge"
                HOME = k.split("-")[-1]
                SHOP = shop_key.split("-")[-1]
                print("Using {0} for traveling from home {1} to shop {2} is best way and time of travelling is {3}".format(way,HOME,SHOP,min(port_distance[k][shop_key], bridge_distance[k][shop_key])))
main()


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

