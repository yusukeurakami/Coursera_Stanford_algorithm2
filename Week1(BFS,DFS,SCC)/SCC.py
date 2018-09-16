import sys
import numpy as np
from Queue import Queue
from collections import deque
from sets import Set
import resource
# from resource import setrlimit
from sys import setrecursionlimit
import datetime



class Graph(object):
    def __init__(self, direction_file):
        self.direction = direction_file
        self.edge_n = np.shape(self.direction)[0]
        self.node_n = np.amax(self.direction)
        self.adjecentList = None
        self.FTcounter = 0
        self.leaderCounter = None
        self.nodes1st = []
        self.nodes2nd = []
        self.explored = Set()
        self.size_counter = 0
        self.big5 = np.zeros(5)
        self.secondtime = False

    def flip_direction(self):
        'Flip the order of the edges'
        self.direction[:,0], self.direction[:,1] = self.direction[:,1] , self.direction[:,0].copy()

    def initNodes(self):
        'Initialize the nodes and store them in nodes dictionary.'
        for i in range(1,self.node_n+1):
            self.nodes1st.append(Node(i))

    def initExplored(self):
        'Reset the explored list.'
        self.explored = Set()

    def edgeSearch(self, node):
        'Search the nodes adjacent that has not been explored and return them as a list.'
        unexplored = [n for n in self.adjecentList[node.originalLabel - 1] if not n in self.explored]
        # []
        # for edge in self.adjecentList[node.originalLabel - 1]:
        #     if edge not in self.explored:
        #         unexplored.append(edge)
        return unexplored
    
    def adjecentListMaker(self):
        'Make the adjecentList by the direction'
        adj_list = []
        for i in range(self.node_n):
            adj_list.append([])
        for i in range(self.edge_n):
            adj_list[self.direction[i][0] - 1].append(self.direction[i][1])
        self.adjecentList = adj_list

    def checkexplored(self, node):
        ''' True when the node doesn't have any unexplored edge.'''
        it_is_deadend = True
        edges = self.edgeSearch(node)
        if len(edges) == 0:
            return it_is_deadend
        for edge in edges:
            if int(edge) not in self.explored:
                    it_is_deadend = False
        return it_is_deadend

    def noRoute(self, node, stack):
        ''' True when it doesn't have any edge that is unexplored or instack '''
        no_route = True
        edges = self.edgeSearch(node)
        if len(edges) == 0:
            return no_route
        for edge in edges:
            if int(edge) not in self.explored:
                if edge not in stack.instack:
                    no_route = False
        return no_route
            
class Node(object):
    def __init__(self, label):
        self.originalLabel = label
        self.finishingTime = 0
        self.leader = None
        self.parents = None

    def __str__(self):
        return "Original Label: " + str(self.originalLabel)

def DFS_rec(graph, node):

    if node.originalLabel in graph.explored:
        return

    graph.explored.add(node.originalLabel)
    edges = graph.edgeSearch(node)
    # print(edges)

    for edge in edges:
        DFS_rec(graph, graph.nodes1st[edge-1])

    graph.FTcounter += 1
    node.finishingtime = graph.FTcounter
    # print("node:", node.originalLabel," is FTcounter", graph.FTcounter)
    graph.nodes2nd[graph.FTcounter-1] = node

def DFS_rec2(graph, node):

    if node.originalLabel in graph.explored:
        return

    graph.explored.add(node.originalLabel)
    graph.size_counter += 1

    edges = graph.edgeSearch(node)

    for edge in edges:
        DFS_rec2(graph, graph.nodes1st[edge-1])
    

def DFS_new(graph, node):
        
    while True:
        # print('testnode: ',test_node.originalLabel)
        graph.explored.add(node.originalLabel)
        # print(test_node.originalLabel, "'s leader is ", graph.leaderCounter)

        #Expand the neighbers
        edges = graph.edgeSearch(node)

        #Push in current node into new nodes list
        if len(edges) == 0:
            graph.nodes2nd.append(node.originalLabel)
            if node.parents == None:
                break
            node = node.parents
        
        else:
            graph.nodes1st[edges[0]-1].parents = node
            node = graph.nodes1st[edges[0]-1]


def DFS_new2(graph, node):

    parents = []
        
    while True:
        # print('testnode: ',node.originalLabel)
        if node.originalLabel not in graph.explored:
            graph.size_counter += 1
        graph.explored.add(node.originalLabel)
        # print("graph size", graph.size_counter)
        # print(test_node.originalLabel, "'s leader is ", graph.leaderCounter)

        #Expand the neighbers
        edges = graph.edgeSearch(node)
        # print(edges)

        #Push in current node into new nodes list
        if len(edges) == 0:
            # print("it is zero len")
            if len(parents) == 0:
                break
            node = parents.pop()
        
        else:
            parents.append(node)
            # graph.nodes1st[edges[0]-1].parents = node
            node = graph.nodes1st[edges[0]-1]

def main(data):

    st_time = datetime.datetime.now()
    G = Graph(data)

    #flip the direction
    # G.flip_direction()
    # print("1st flipping done")
    G.adjecentListMaker()
    print('1st Adjacent completed')

    #Make nodes
    G.initNodes()
    print('Initial node ready')
    # for node in G.nodes1st:
    #     print(node)

    #1st DFS loop
    i = len(G.nodes1st)
    while i > 0:
        # print("iteration: ", i)
        node = G.nodes1st[i-1]
        if node.originalLabel not in G.explored:
            DFS_new(G, node)
        i -= 1
    
    print('First DFS completed')
    
    '''
    No need for regenerating the new graph with the new label.
    graph.nodes2nd is already ordered by the finishing time.
    If you feed the nodes2nd from the last to first, it will be same as update the graph and 
    feed the node from the largest finishingtime to the smallest finishing time.

    Use original graph + reverse order of the assignment of FT == Use updated graph + reverse order of finishing time.
    '''
    #flip the direction
    G.flip_direction()
    print("2nd flipping done")
    G.adjecentListMaker()
    print('2nd adjecent list done')
    G.initExplored()
    G.initNodes()
    print("Initialized the 1stnodes' parents")
    G.secondtime = True

    #2nd DFS loop
    i = len(G.nodes2nd)
    while i > 0:
        G.size_counter = 0
        node = G.nodes1st[G.nodes2nd[i-1]-1]
        if node.originalLabel not in G.explored:
            DFS_new2(G, node)

        size = G.size_counter
        # # print("size: ", size)

        if size != 0:
            if size > G.big5[4]:
                if size > G.big5[3]:
                    G.big5[4] = G.big5[3]
                    if size > G.big5[2]:
                        G.big5[3] = G.big5[2]
                        if size > G.big5[1]:
                            G.big5[2] = G.big5[1]
                            if size > G.big5[0]:
                                G.big5[1] = G.big5[0]
                                G.big5[0] = size
                            else:
                                G.big5[1] = size
                        else:
                            G.big5[2] = size
                    else:
                        G.big5[3] = size
                else:
                    G.big5[4] = size

        # print(G.big5)
        i -= 1
    
    print("Second DFS done")

    ed_time = datetime.datetime.now()

    #get the size of 5 biggest SCCs
    delta = ed_time - st_time
    
    print("Running time:", divmod(delta.total_seconds(), 60))
    print(G.big5)


if __name__ == "__main__":
    setrecursionlimit(2 ** 20)
    # resource.setrlimit(resource.RLIMIT_STACK, (10**6, 10**6))

    #read the txt file
    inputfile = sys.argv[1]
    data = np.loadtxt(inputfile, usecols=range(0,2), delimiter=" ", dtype=int)

    # with open(inputfile) as file:
    #     lines = file.readlines()
    #     b = [x.split(' ')[:-1] for x in lines]
    #     # b = [x.strip() for x in lines]
    # c = np.array(b)
    main(data)
