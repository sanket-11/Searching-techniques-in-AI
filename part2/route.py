#!/usr/bin/env python

# put your routing program here!

import sys
import Queue as Q
import math

#input arguments
N1 = sys.argv[1]#City 1
N2 = sys.argv[2] #City 2
N3 = sys.argv[3]#Routing Algorithm eg. bfs, dfs, ucs, ids, astar
N4 = sys.argv[4] #Cost Function eg. time, distance, segment
#Read city-gps file and store in dicionary
f2 = open("city-gps.txt", "r")
coordinates=dict()
for word in f2.readlines():
    word=word[:-1] ##to strip \n in the end from the file
    a=list(word.split(' '))
    x=[a[1],a[2]]
    coordinates[a[0]]=x

#class to store road-segments data
class node():

    def __init__(self,city,distance,speed,highway):
        self.city = city
        self.distance = distance
        self.speed = speed
        self.highway = highway

#read road-segments and store in dictionary with values as object of class
##file3=open("road-segments.txt","r")
##f1=file3.readlines()
##finaldict={}
##road_list = [lines.strip().split() for lines in f1]
##for line in road_list:
##    ##missing speeds are put as 50 in raw file
##    firstcity=node(line[1],line[2],line[3],line[4])
##    secondcity=node(line[0],line[2],line[3],line[4])
##    finaldict[line[0]] = (finaldict.get(line[0], []) + [firstcity])
##    finaldict[line[1]] = (finaldict.get(line[1], []) + [secondcity])

f1 = open("road-segments.txt", "r")
finaldict=dict()
cost=[]
for word in f1.readlines():
	a=list(word.split(' '))
	cost.append(a)
	firstcity=node(a[1],a[2],a[3],a[4])  
	secondcity=node(a[0],a[2],a[3],a[4])
	finaldict[a[0]]=finaldict.get(a[0],[])+[firstcity]
	finaldict[a[1]]=finaldict.get(a[1],[])+[secondcity]

def calculatedistance(route): ##function to check distance cost of a given path
	route_cost=0
	for i in range(len(route)-1):
		for d in cost:
			if route[i]==d[0] and route[i+1]==d[1] or route[i+1]==d[0] and route[i]==d[1]:
		  		 #to extract cost between two nodes
		  		route_cost+=int(d[2])
	return route_cost
def calculatetime(route):
	route_cost=0
	for i in range(len(route)-1):
		for d in cost:
			if route[i]==d[0] and route[i+1]==d[1] or route[i+1]==d[0] and route[i]==d[1]:
                                route_cost+=(int(d[2])/float(d[3]))
	return route_cost
#Breadth-first search
def bfs(graph, start, end, costfunction):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            distance=(calculatedistance(path))
            time=(calculatetime(path))
            if costfunction=='segments':
                print "yes",distance,time, ' '.join(path)
            else:
                print "no",distance,time, ' '.join(path)
            
            return path
        adjacentlist=[]
        for i in range(0,len(graph[node])):
            adjacentlist.append(graph[node][i].city)
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in adjacentlist:
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)
    return False

 
#Depth First Search    
def dfs(graph, start, end,costfunction):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop()
        #print("1st:",path)
        # get the last node from the path
        node = path[-1]
               
        # path found
        if node == end:
            distance=(calculatedistance(path))
            time=(calculatetime(path))
            if costfunction=='segments' or costfunction=='distance' or costfunction=='time':
                print "no",distance,time, ' '.join(path)
            #return(path)
            break
            
        adjacentlist=[]
        for i in range(0,len(graph[node])):
            adjacentlist.append(graph[node][i].city)
        #print("adj list",adjacentlist)
        # get all adjacent nodes, construct a new path and push it into the queue
        for adjacent in adjacentlist:#graph.get(node[0], []):
            #print("adjacent",adjacent)
            new_path = list(path)
            #print("1st new_path",new_path)
            new_path.append(adjacent)
            queue.append(new_path)
            #print("queue",queue)
    return False
#Depth First search for IDS
def dfs1(graph, start, end, depth=-1):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop()
        #print("1st:",path)
        # get the last node from the path
        node = path[-1]
        if(depth!=-1):
           if (len(node)>(depth+1)):
               return 0
        
        # path found
        if node == end:
            
            return(path)
            break
            
        adjacentlist=[]
        for i in range(0,len(graph[node])):
            adjacentlist.append(graph[node][i].city)
        #print("adj list",adjacentlist)
        # get all adjacent nodes, construct a new path and push it into the queue
        for adjacent in adjacentlist:#graph.get(node[0], []):
            #print("adjacent",adjacent)
            new_path = list(path)
            #print("1st new_path",new_path)
            new_path.append(adjacent)
            queue.append(new_path)
            #print("queue",queue)
    return False

def ids(graph,start,end,depth):
    a=dfs1(graph,start,end,depth)
    if isinstance(a,list):
        #print(a)
        distance=(calculatedistance(a))
        time=(calculatetime(a))
        print "yes",distance,time, ' '.join(a)
    else:
        ids(graph,start,end,depth+1)
    return False
	


#Uniform Cost Search
def ucs(graph, start, end,cost_function): 
    # maintain a queue of paths
    queue = Q.PriorityQueue()
    # push the first path into the queue
    queue.put((0,[start], 0))
    while not queue.empty():
        # get the first path from the queue
        node = queue.get()
        current = node[1][len(node[1]) - 1]
        cost=node[0]
        cost2=node[2]
        if end in node[1]:
            distance=(calculatedistance(node[1]))
            time=(calculatetime(node[1]))
            print "yes",distance,time, ' '.join(node[1])
##            if cost_function=='distance':
##                
##                print("Path found: " + str(node[1]) + ", Total Distance = " + str(node[0])+", Total Time in hours = " + str(node[0]/node[2]))
##        
##            elif cost_function=='time':
##                print("Path found: " + str(node[1]) + ", Total Distance = " + str(node[0])+ ", Total Time in hours = " + str(node[0]/node[2]))
            break
        if cost_function=='distance' or 'segments':
            for neighbor in graph[current]:
                temp = node[1][:]
                temp.append(neighbor.city)                
                queue.put((cost + int(neighbor.distance), temp, cost2 + int(neighbor.speed)))
        if cost_function=='time':
            for neighbor in graph[current]:
                temp = node[1][:]
                temp.append(neighbor.city)            
                queue.put((cost + int(neighbor.speed), temp, cost2 + int(neighbor.distance)))
    return False




def distance(origin, destination):  ## https://stackoverflow.com/questions/44743075/calculate-the-distance-between-two-coordinates-with-python
    """
    Calculate the Haversine distance.
    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)
    Returns
    -------
    distance_in_km : float
    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d


#Astar using Distance
def a_stardistance(graph, start, dest, coordinates):
    queue = Q.PriorityQueue()
    queue.put([(start, 0)], 0)
    explored = set()

    while not queue.empty():
        # shortest available path
        path = queue.get()        
        node = path[-1][0]
        g_cost = path[-1][1]
        explored.add(node)
        if node == dest:
            dist=(calculatedistance([x for x, y in path]))
            time=(calculatetime([x for x, y in path]))
            print "yes",dist,time, ' '.join([x for x, y in path])
##            print ([x for x, y in path])
##            print (calculatedistance([x for x, y in path]))
##            print (calculatetime([x for x, y in path]))
            #print ("Distance cost",cumulative_cost)
            break

        for neighbor in graph[node]:
            cumulative_cost = g_cost + int(neighbor.distance)
            if neighbor.city in coordinates:
                x1=float(coordinates[neighbor.city][0])
                y1=float(coordinates[neighbor.city][1])
            else:
                x1=0.0
                y1=0.0
            if dest in coordinates:
                x2=float(coordinates[dest][0])
                y2=float(coordinates[dest][1])
            else:
                x2=0.0
                y2=0.0
            f_cost = cumulative_cost + distance((x1,y1),(x2,y2))
            new_path = path + [(neighbor.city, cumulative_cost)]
            # add new_path to queue
            if neighbor.city not in explored:
                queue.put(new_path, f_cost)
            # update cost of path in queue
            elif neighbor.city in queue.queue:
                queue.put(new_path, f_cost)
                print("Path found",path)

    return False



#Astar using Time
def a_startime(graph, start, dest, coordinates):
    queue = Q.PriorityQueue()
    queue.put([(start, 0)], 0)
    explored = set()

    while not queue.empty():
        # shortest available path
        path = queue.get()
        node = path[-1][0]
        g_cost = path[-1][1]
        explored.add(node)

        if node == dest:
            dist=(calculatedistance([x for x, y in path]))
            time=(calculatetime([x for x, y in path]))
            print "yes",dist,time, ' '.join([x for x, y in path])
##            print ([x for x, y in path])
##            print (calculatedistance([x for x, y in path]))
##            print (calculatecost([x for x, y in path]))
            #print ("Speed Cost: ",cumulative_cost)
            break

        for neighbor in graph[node]:
            cumulative_cost = g_cost + int(neighbor.speed)
            if neighbor.city in coordinates:
                x1=float(coordinates[neighbor.city][0])
                y1=float(coordinates[neighbor.city][1])
            else:
                x1=0.0
                y1=0.0
            if dest in coordinates:
                x2=float(coordinates[dest][0])
                y2=float(coordinates[dest][1])
            else:
                x2=0.0
                y2=0.0
            f_cost = cumulative_cost + distance((x1,y1),(x2,y2))
            new_path = path + [(neighbor.city, cumulative_cost)]
            # add new_path to queue
            if neighbor.city not in explored:
                queue.put(new_path, f_cost)
            # update cost of path in queue
            elif neighbor.city in queue.queue:
                queue.put(new_path, f_cost)
                print("Path found",path)

    return False


#Astar using Segment
def a_starsegment(graph, start, dest, coordinates):
    queue = Q.PriorityQueue()
    queue.put([(start, 0)], 0)
    explored = set()

    while not queue.empty():
        # shortest available path
        path = queue.get()
        node = path[-1][0]
        g_cost = path[-1][1]
        explored.add(node)
        if node == dest:
            dist=(calculatedistance([x for x, y in path]))
            time=(calculatetime([x for x, y in path]))
            print "yes",dist,time, ' '.join([x for x, y in path])
##            print ([x for x, y in path])
##            print (calculatedistance([x for x, y in path]))
##            print (calculatecost([x for x, y in path]))
            #print ("Segments cost: ",cumulative_cost)
            break

        for neighbor in graph[node]:
            cumulative_cost = g_cost + 1
            if neighbor.city in coordinates:
                x1=float(coordinates[neighbor.city][0])
                y1=float(coordinates[neighbor.city][1])
            else:
                x1=0.0
                y1=0.0
            if dest in coordinates:
                x2=float(coordinates[dest][0])
                y2=float(coordinates[dest][1])
            else:
                x2=0.0
                y2=0.0
            f_cost = cumulative_cost + distance((x1,y1),(x2,y2))
            new_path = path + [(neighbor.city, cumulative_cost)]

            # add new_path to queue
            if neighbor.city not in explored:
                queue.put(new_path, f_cost)
            # update cost of path in queue
            elif neighbor.city in queue.queue:
                queue.put(new_path, f_cost)
                print("Path found",path)
    return False

if N3=='bfs' and N4=='distance':
    bfs(finaldict,N1,N2,N4)
elif N3=='bfs' and N4=='segments':
    bfs(finaldict,N1,N2,N4)
elif N3=='bfs' and N4=='time':
    bfs(finaldict,N1,N2,N4)

elif N3=='dfs' and N4=='time':
    dfs(finaldict,N1,N2,N4)
elif N3=='dfs' and N4=='segments':
    dfs(finaldict,N1,N2,N4)
elif N3=='dfs' and N4=='distance':
    dfs(finaldict,N1,N2,N4)

elif N3=='ids':
    ids(finaldict,N1,N2,0)#start with depth 0 and increment recursively until goal state is attained
elif N3=='uniform' and N4=='distance':
    ucs(finaldict,N1,N2,N4)
elif N3=='uniform' and N4=='segments':
    ucs(finaldict,N1,N2,N4)
elif N3=='uniform' and N4=='time':
    ucs(finaldict,N1,N2,N4)
elif N3=='astar' and N4=='distance':
    a_stardistance(finaldict,N1,N2,coordinates)
elif N3=='astar' and N4=='time':
    a_startime(finaldict,N1,N2,coordinates)
elif N3=='astar' and N4=='segments':
    a_starsegment(finaldict,N1,N2,coordinates)
    

