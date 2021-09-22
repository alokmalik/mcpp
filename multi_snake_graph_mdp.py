import numpy as np
import networkx as nx
from gridngraph import GridnGraph

#The entire code is structured as an Markon Chain
class MDP:
    def __init__(self,l,b) -> None:
        self.gridngraph = GridnGraph()
        self.n=0
        self.s=1
        self.e=2
        self.w=3
        self.smallgridsize=10
        self.explored=1
        self.l=l
        self.b=b
        self.nomove=-1
    
    def visit_master(self,crds,agent,bridges,graph):
        #bridges=self.bridges(graph)
        source=crds[agent]
        if len(graph)==1:
            return True
        if crds.count(source)>1:
            return False
        neighbours=[]
        for neighbour in graph[source]:
            neighbours.append(neighbour)
        

        graph.remove_node(source)
        if not nx.algorithms.components.is_connected(graph):
            graph.add_node(source)
            for neighbour in neighbours:
                graph.add_edge(source,neighbour)
            return False
        else:
            graph.add_node(source)
            for neighbour in neighbours:
                graph.add_edge(source,neighbour)

            return True

    def bridges(self,graph):
        edges=list(nx.bridges(graph))
        nodes=[]
        for edge in edges:
            if edge[0] not in nodes:
                nodes.append(edge[0])
            if edge[1] not in nodes:
                nodes.append(edge[1])
        return nodes

    #checks for bridges on smaller map and larger map
    def visitpermission(self,crds,agent,grid,graph):
        [x,y]=crds[agent]
        if crds.count([x,y])!=1:
            return False
        l,b=grid.shape
        if x-self.smallgridsize>0 and x+self.smallgridsize+1<l and y-self.smallgridsize>0 and y+self.smallgridsize+1<b:
            smallgraph=self.gridngraph.makegraph(grid[x-self.smallgridsize:x+self.smallgridsize+1,y-self.smallgridsize:y+self.smallgridsize+1])
            mark= self.visit_master(self.smallgridsize,\
                self.smallgridsize,grid[x-self.smallgridsize:x+self.smallgridsize+1,y-self.smallgridsize:y+self.smallgridsize+1],smallgraph)
            #checks for bridge in larger map if a point is part of bridge in smaller map
            if not mark:
                return self.visit_master(x,y,grid,graph)
            else:
         
                return mark
        #else is triggered near edges of map.
        else:
            return self.visit_master(x,y,grid,graph)

    def availablemoves(self,crds,agent,graph):
        source=crds[agent]
        c=0
        if source in graph:
            c=graph.degree[source]
        else:
            raise NameError('Source Node not in Graph')
        return c
    
    def nextaction(self,crds,agent,actiontuple,moves,graph):
        l,b=self.l,self.b
        source=crds[agent]
        am=self.availablemoves(crds,agent,graph)
        actions=actiontuple.copy()
        pref=[]
        #print(am,actiontuple)
        for i in range(4):
            m=np.argmax(actiontuple)
            pref.append(m)
            actiontuple[m]=float('-inf')
        
        if len(graph)==1:
            print('No Move')
            return self.nomove
        if am==0 and len(graph)!=1:
            raise NameError('Available Actions zero')
        elif am==1:
            for neighbour in graph[source]:
                if neighbour==source-b:
                    return self.n
                elif neighbour==source+b:
                    return self.s
                elif neighbour==source+1:
                    return self.e
                elif neighbour==source-1:
                    return self.w
        else:
            for dc in pref:
                if dc==self.n and source-b in graph and source in graph[source-b] and source-b!=moves[agent][-2]:
                    return self.n
                elif dc==self.s and source+b in graph and source in graph[source+b] and source+b!=moves[agent][-2]:
                    return self.s
                elif dc==self.e and source+1 in graph and source in graph[source+1] and source+1!=moves[agent][-2]:
                    return self.e
                elif dc==self.w and source-1 in graph and source in graph[source-1] and source-1!=moves[agent][-2]:
                    return self.w
                else:
                    continue
        raise NameError('No action Selected,Source: {}, AM: {}, Original Action Preferences: {}, Pref: {}'.format(source,am,pref,actions))

    #input: current position, past moves, grid and graph, and action prefrences
    #output: next positon, next grid and graph, current moves appended
    def mdp(self,crds,moves,agent,bridges,graph,actiontuple):
        #l and b are length and breadth of graph
        l,b=self.l,self.b
        source=crds[agent]
        #function choses next action based on constraint of grid and last moves
        action=self.nextaction(crds,agent,actiontuple,moves,graph)
        #visit permission function checks whether a point\
        #can be marked as visited
        mark=self.visit_master(crds,agent,bridges,graph)
        visited=[]
        explored=[]
        if mark:
            if source in graph:
                graph.remove_node(source)
                visited.append(source)
            else:
                raise NameError('Source node not in Graph')
        else:
            if source in graph:
                graph.nodes[source]['explored']=self.explored
                explored.append(source)
            else:
                raise NameError('Source node not in graph')
        #print(x,y,action)
        #print('Action {}'.format(action))
        #print(source,source-b,graph[source-b])
        if action==self.n and source-b in graph:
            source-=b
        elif action==self.s and source+b in graph:
            source+=b
        elif action==self.e and source+1 in graph:
            source+=1
        elif action==self.w and source-1 in graph:
            source-=1
        elif action==self.nomove and len(graph)==0:
            pass
        elif len(graph)!=0:
            raise NameError('No Action Taken')
        moves[agent].append(source)

        crds[agent]=source
        return crds,moves,graph,visited,explored