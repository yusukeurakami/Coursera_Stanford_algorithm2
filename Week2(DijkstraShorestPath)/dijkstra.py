from heapq import heappush, heappop
import itertools

class Node(object):
    def __init__(self, id):
        self.id = id
        self.shortest_dist = 0
        self.neighber = []

    def __str__(self):
        return str(self.id)
    

class PriorityQueue():
    def __init__(self):
        self.pq = []                    # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task):
            'Mark an existing task as REMOVED.  Raise KeyError if not found.'
            entry = self.entry_finder.pop(task)
            entry[-1] = self.REMOVED

    def pop_task(self):
            'Remove and return the lowest priority task. Raise KeyError if empty.'
            while self.pq:
                priority, count, task = heappop(self.pq)
                if task is not self.REMOVED:
                    del self.entry_finder[task]
                    return task, priority
            raise KeyError('pop from an empty priority queue')

    def lookupKey(self, task):
        if len(self.entry_finder) == 0:
            return 10000000
        try:
            entry = self.entry_finder[task]
            return entry[0]
        except:
            return 100000000

    def showpq(self):
        print("PQ:")
        for i in range(len(self.entry_finder)): 
            if type(self.pq[i][2]) == str:
                print("removed")
            else:
                print(self.pq[i][2].id, self.pq[i][0])

    def length(self):
            print(len(self.entry_finder))


def dijkstra(goal_index, neighber):
    #Initialize nodes
    nodes_list = initializeNode(neighber)

    source_node = nodes_list[0]
    goal_node = nodes_list[goal_index - 1]
    explored = []
    pq = PriorityQueue()
    node = source_node
    key = 0

    while pq: 

        # print("Current node",node.id)
        # print("Key",key)

        explored.append(node.id)

        if node.id == goal_node.id:
            return key

        # print(node.neighber)

        for n in node.neighber:
            n_id = int(n[0])
            n_cost = int(n[1])
            neighber_node = nodes_list[n_id-1]

            # print("Adding", neighber_node.id, 'cost=', n_cost + key)
            # print("lookup_key:", pq.lookupKey(neighber_node))
            # print("explored:", explored)

            #compare the key value
            if neighber_node.id not in explored:
                if (n_cost + key) < pq.lookupKey(neighber_node):
                    # print("decreasing")
                    pq.add_task(neighber_node, n_cost + key)
            # pq.showpq()
            # pq.length()


        node, key = pq.pop_task()

        # print('')


def initializeNode(neighber):
    nodes_list = []
    for i in range(1, len(neighber)+1):
        node = Node(i)
        node.neighber = neighber[i-1]
        nodes_list.append(node)
    return nodes_list

def readfile():
    file = open('dijkstraData.txt')#('dijkstraData.txt')
    lines = file.readlines()
    neighber = []


    b = [x.strip('\n').strip(' ').strip('\r').split('\t')[:-1] for x in lines]
    # print(b[0])
    for b_ele in b:
        # print("b_ele",b_ele)
        c = [y.split(',') for y in b_ele]
        if c[1] == ['']:
            c = []
        neighber.append(c[1:])
    return neighber

def run():
    goal_list = [7,37,59,82,99,115,133,165,188,197]
    result_list = []
    neighber = readfile()

    for goal in goal_list:
        shortest_path = dijkstra(goal, neighber)
        result_list.append(shortest_path)
    return result_list

if __name__ == "__main__":
    print(run())

