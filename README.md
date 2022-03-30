# dijekstra_bridge
# First PHASE(main.py)
This code has been developed for .docx problem. There are 3 main file. First one is main.py . This is the simplest way of implementation. For a second one I assumed we have a one river but we have a remarkable number of bridges and ports. 
# Second PHASE(phase_two.py)
IN THIS PHASE WE ASSUME WE HAVE A REMARKABLE NUMBER OF PORT AND BRIDGES
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
2- If inputs are NOT sorted the order is reduced to O(shop * home * bridge log(bridge)) + O(shop * home * port *log(port)).
if we use parrallel programming the order reduced to O(bridge*log(bridge)) + O(port *log(port)) 

# Third PHASE(phase_three.py)
IN THIS PHASE WE ASSUME WE HAVE A REMARKABLE NUMBER OF PORT AND BRIDGES AND WE HAVE MORE THAN 1 RIVER

WARNING1: BECAUSE INPUT IS INCOMPATIBLE TO OUR OUTPUT, I CAHNGED INPUT AS FOLLOW:
AFTER SHOP-INPUTS, WE HAVE EXTRA NUMBER THAT POINT TO THE NUMBER OF RIVERS AND FOLLOW THAT WE HAVE PORT AND BRIDGE INPUTS

WARNINIG2: WE ASSUME THAT DISTANCE BETWEEN EACH RIVER IS 2

ALGORITHM:
For solving problem, first we prune or graph. 
we use phase 2 in each layer to reduce number of edges from approximately V^2 to V-1.
After that Dijkstra is used. therefore the order reduce to O(shop * home * bridge log(bridge)) + O(shop * home * port *log(port)) +O(VlogV) instead of O((V + E)logV)
Also if we use parrallel programming(in prunning for each 3 lane for one thread) the order will reduce more!

# OUTPUT
For phase 1 and phase 2 we print both shortest-path and path itself. For example 2_3:10, meaning travel from home 2 to 3 is 10 second and [2,4,5] is show the path
