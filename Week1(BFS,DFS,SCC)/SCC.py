import sys
import numpy as np
from Queue import Queue
from collections import deque
from sets import Set
import resource
# from resource import setrlimit
from sys import setrecursionlimit



class Graph(object):
    def __init__(self, direction_file):
        self.direction = direction_file
        self.edge_n = np.shape(self.direction)[0]
        self.node_n = np.amax(self.direction)
        self.adjecentList = None
        self.flipcounter = False
        self.FTcounter = 0
        self.leaderCounter = None
        self.nodes1st = [None] * self.node_n
        self.nodes2nd = [None] * self.node_n
        self.explored = Set()
        self.size_counter = 0
        self.big5 = np.zeros(5)

    def flip_direction(self):
        'Flip the order of the edges'
        self.direction[:,0], self.direction[:,1] = self.direction[:,1] , self.direction[:,0].copy()
        if self.flipcounter == False:
            self.flipcounter = True
        if self.flipcounter == True:
            self.flipcounter = False

    def initNodes(self):
        'Initialize the nodes and store them in nodes dictionary.'
        for i in range(1,self.node_n+1):
            self.nodes1st[i-1] = Node(i)

    def initExplored(self):
        'Reset the explored list.'
        self.explored = Set()

    def edgeSearch(self, node):
        'Search the nodes adjacent of input and return them as a list.'
        # edges = []
        # for i in range(self.edge_n):
        #     if self.direction[i,0] == node.originalLabel:
        #         edges.append(self.direction[i,1])
        # return edges
        return self.adjecentList[node.originalLabel - 1 ]
    
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


    def backtrack(self, node, stack):
        '''
        This function will be called when the input node has no more edges to explore.
        It will trace the parents node of the input node and check if that node is also a deadend.
        If the parents node is also a deadend, it will assign the finishing time.
        It will call itself recursively until it finds the parents node with an unexplored node.
        '''
        # print("backtrack!")
        if node.parents == None:
            # print('no parents')
            pass
        else:
            s = node.parents
            # print('Parent Label:', s.originalLabel)
            # print('Is ', s.originalLabel, ' dead end? :', self.checkexplored(s) )
            while self.checkexplored(s):
                # print('backtracking')
                self.FTcounter += 1 #For debugging
                s.finishingTime = self.FTcounter #For debugging
                self.nodes2nd[self.FTcounter-1] = s
                # print(self.FTcounter)
                # print(s.originalLabel, " is Labeled as ", s.finishingTime)
                s = s.parents
                if s == None:
                    break

    def backtrack2(self, node, stack):
        '''
        This function will be called when the input node has no more edges to explore.
        It will trace the parents node of the input node and check if that node is also a deadend.
        '''
        if node.parents == None:
            pass
        else:
            s = node.parents
            while self.checkexplored(s):
                s = s.parents
                if s == None:
                    break
            
class Node(object):
    def __init__(self, label):
        self.originalLabel = label
        self.finishingTime = 0
        self.leader = None
        self.parents = None

    def __str__(self):
        return "Original Label: " + str(self.originalLabel)

class Stack(object):
    def __init__(self):
        self.queue = deque()
        self.instack = Set()
    
    def add(self, node):
        self.queue.append(node)
        self.instack.add(node.originalLabel)

    def pop(self):
        poped = self.queue.pop()
        self.instack.remove(poped.originalLabel)
        return poped

    def searchStack(self, node):
        if str(node) in self.instack:
            True
        else:
            False

    def length(self):
        return len(self.instack)

    def stackshow(self):
        show = []
        for i in self.queue:
            show.append(i.originalLabel)
        print("Current stack",show)


def DFS(graph, node):
    #Make the Stack 
    stack = Stack()
    stack.add(node)

    while stack.queue:
        test_node = stack.pop()

        # print('testnode: ',test_node.originalLabel)
        graph.explored.add(test_node.originalLabel)
        test_node.leader = graph.leaderCounter
        graph.size_counter += 1
        # print(test_node.originalLabel, "'s leader is ", graph.leaderCounter)

        #Expand the neighbers
        edges = graph.edgeSearch(test_node)

        #Push in current node into new nodes list
        if graph.noRoute(test_node, stack):
            graph.FTcounter += 1 #For debugging
            test_node.finishingTime = graph.FTcounter #For debugging
            graph.nodes2nd[graph.FTcounter-1] = test_node #This list's order actually work as a FT
            # print(test_node.originalLabel, " is Labeled as ", test_node.finishingTime)
            # print("what is parents:", test_node.parents.originalLabel)
            graph.backtrack(test_node, stack) # backtrack until node has a unexplored edges

        else:
            for edge in edges:
                if int(edge) not in graph.explored:
                    if edge in stack.instack:
                        # stack.stackshow()
                        stack.queue.remove(graph.nodes1st[edge-1])
                    # print(graph.nodes1st[edge-1].originalLabel, ' parent is ', test_node.originalLabel)
                    graph.nodes1st[edge-1].parents = test_node
                    stack.add(graph.nodes1st[edge-1])

def DFS2(graph, node):
    #Make the Stack 
    stack = Stack()
    stack.add(node)

    while stack.queue:
        test_node = stack.pop()

        # print('testnode: ',test_node.originalLabel)
        graph.explored.add(test_node.originalLabel)
        test_node.leader = graph.leaderCounter
        graph.size_counter += 1
        print(graph.size_counter)
        # print(test_node.originalLabel, "'s leader is ", graph.leaderCounter)

        #Expand the neighbers
        edges = graph.edgeSearch(test_node)

        #Push in current node into new nodes list
        if graph.noRoute(test_node, stack):
            graph.backtrack2(test_node, stack) # backtrack until node has a unexplored edges

        else:
            for edge in edges:
                if int(edge) not in graph.explored:
                    if edge in stack.instack:
                        # stack.stackshow()
                        stack.queue.remove(graph.nodes1st[edge-1])
                    # print(graph.nodes1st[edge-1].originalLabel, ' parent is ', test_node.originalLabel)
                    graph.nodes1st[edge-1].parents = test_node
                    stack.add(graph.nodes1st[edge-1])

def main(data):
    G = Graph(data)

    #flip the direction
    G.flip_direction()
    print("1st flipping done")
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
            G.leaderCounter = i
            DFS(G, node)
        i -= 1
    
    print('First DFS completed')

    # print('')
    # print("After 1st DFS loop")
    # for node in G.nodes2nd:
    #     print(node)

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

    #2nd DFS loop
    i = len(G.nodes2nd)
    while i > 0:
        print("iteration: ", i)
        G.size_counter = 0
        node = G.nodes2nd[i-1]
        if node.originalLabel not in G.explored:
            G.leaderCounter = i
            DFS2(G, node)

        size = G.size_counter
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
        i -= 1
    
    print("Second DFS done")

    #get the size of 5 biggest SCCs
    print(G.big5)
    ''' 2.Need function to count the size of each leader nodes group and order them in size '''
    '''Get the five biggest during the 2nd DFS loop'''

if __name__ == "__main__":
    setrecursionlimit(2 ** 20)
    resource.setrlimit(resource.RLIMIT_STACK, (10**6, 10**6))

    #read the txt file
    inputfile = sys.argv[1]
    data = np.loadtxt(inputfile, usecols=range(0,2), delimiter=" ", dtype=int)

    # with open(inputfile) as file:
    #     lines = file.readlines()
    #     b = [x.split(' ')[:-1] for x in lines]
    #     # b = [x.strip() for x in lines]
    # c = np.array(b)
    main(data)
