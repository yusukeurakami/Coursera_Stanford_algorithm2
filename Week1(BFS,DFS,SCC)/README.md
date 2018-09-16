# Strongly Connected Components Algorithm

## Approach

### Iterative form
I changed the algirithm into an iterative form because Python has the recursive limit, and giving the huge size of the graph (800,000 edges), likely to hit the limit. Plus, I didn't want to occupy the memory space.

### Backtrack function
Since applying the iterative form, I have to backtrack the node when the DFS hit the bottom of the graph in order to record of visiting node in pre-order.

## Result
Running time: 6 hours
```
[4.34821e+05 9.68000e+02 4.59000e+02 3.13000e+02 2.11000e+02]
```
For the first code I wrote, the output is correct but the running time is 6 hours.

## Improvement

### 9/14/2018 
Running time 1m 06s on my same Macbook Pro by improving the code.

#### No stack
I realized that in DFS, I don't have to stick to a stack data structure. When the alrorithm do a neighbers search and get the unexplored candidate nodes (Frontier nodes) connected to certain node, instead of storing the Frontier node into the stack, I can just choose the random explored node and discard the rests (In my implementation I chose the first one on the list).

```
        #Expand the neighbers
        edges = graph.edgeSearch(node)                  # Neighbers search

        #Push in current node into new nodes list
        if len(edges) == 0:                             # if no neighbers
            graph.nodes2nd.append(node.originalLabel)
            if node.parents == None:                    # if came back to the source node, break
                break
            node = node.parents                         # set its parents as a next node (backtrack)
        
        else:
            graph.nodes1st[edges[0]-1].parents = node
            node = graph.nodes1st[edges[0]-1]           # else, set the 1st node as a next node
```

This can be possible because the purpose of the DFS is to just dig deeper and deeper. It don't have to keep the frontiers on a memory all time, instead, it will redo the neighbers search again when it came back to that node by backtracking function.

#### Backtrack

In this case, backtracking is not even a particular function. Algorithm will just give the parents node as next node to explore when the DFS hit the bottom of the graph. During the backtracking, iterative loop will push the already explored node (parents node) into explored list for second time, but there is no problem with that. Explored list only matter when executing the neighbers search.
