import numpy as np
import networkx as nx

class BFSengine:
    def __init__(self,l,b) -> None:
        self.l=l
        self.b=b
        self.neighbours=[]
    def bfs(self,source,graph,depth):
        paths={}
        #print(source)
        paths[source]=[source]
        queue=[]
        queue.append(source)
        distances={}
        distances[source]=0
        nodes=[]
        while queue:
            node=queue.pop(0)
            for neighbour in graph[node]:
                if neighbour not in distances.keys() and distances[node]<depth and graph.degree(neighbour)<4:
                    distances[neighbour]=distances[node]+1
                    paths[neighbour]=paths[node]+[neighbour]
                    queue.append(neighbour)
                    if node not in nodes:
                        nodes.append(node)
        return paths

    def bridges(self,graph):
        edges=list(nx.bridges(graph))
        nodes=[]
        for edge in edges:
            if edge[0] not in nodes:
                nodes.append(edge[0])
            if edge[1] not in nodes:
                nodes.append(edge[1])
        return nodes


    def action_list(self,crds,agent,graph,depth):
        l,b=self.l,self.b
        source=crds[agent]
        paths=self.bfs(source,graph,depth)
        bridges=self.bridges(graph)
        north=source-b
        south=source+b
        east=source+1
        west=source-1
        n,s,e,w=0,0,0,0
        pathrating={}
        #give each possible path rating
        for node in paths.keys():
            pathrating[node]=0
            for p in paths[node]:
                if graph.degree(p)==1:
                    pathrating[node]=+depth*2
                if p in bridges:
                    pathrating[node]-=1
                if not graph.nodes[p]['explored']:
                    pathrating[node]+=1
                if p in crds and p!=source:
                    pathrating[node]-=1
        #for each direction choose path with highest rating
        for node in pathrating.keys():
            if north in paths[node] and n<pathrating[node]:
                n=pathrating[node]
            if south in paths[node] and s<pathrating[node]:
                s=pathrating[node]
            if east in paths[node] and e<pathrating[node]:
                e=pathrating[node]
            if west in paths[node] and w<pathrating[node]:
                w=pathrating[node]
        #deprioritize paths if other agents are in the way
        for crd in crds:
            for node in paths.keys():
                #print(paths[node],north,south,east,west)
                if north in paths[node] and crd in paths[node] and crd!=crds[agent]:
                    #print('hi1')
                    n-=depth*2
                    if south in graph and source in graph[south] and not graph.nodes[south]['explored'] and south not in crds:
                        s+=1
                    if east in graph and source in graph[east] and not graph.nodes[east]['explored'] and east not in crds:
                        e+=1
                    if west in graph and source in graph[west] and not graph.nodes[west]['explored'] and west not in crds:
                        w+=1
                elif south in paths[node] and crd in paths[node] and crd!=crds[agent]:
                    #print('hi2')
                    s-=depth*2
                    if north in graph and source in graph[north] and not graph.nodes[north]['explored'] and north not in crds:
                        n+=1
                    if east in graph and source in graph[east] and not graph.nodes[east]['explored'] and east not in crds:
                        e+=1
                    if west in graph and source in graph[west] and not graph.nodes[west]['explored'] and west not in crds:
                        w+=1
                elif east in paths[node] and crd in paths[node] and crd!=crds[agent]:
                    #print('hi3')
                    e-=depth*2
                    if north in graph and source in graph[north] and not graph.nodes[north]['explored'] and north not in crds:
                        n+=1
                    if south in graph and source in graph[south] and not graph.nodes[south]['explored'] and south not in crds:
                        s+=1
                    if west in graph and source in graph[west] and not graph.nodes[west]['explored'] and west not in crds:
                        w+=1
                elif west in paths[node] and crd in paths[node] and crd!=crds[agent]:
                    #print('hi4')
                    w-=depth*2
                    if north in graph and source in graph[north] and not graph.nodes[north]['explored'] and north not in crds:
                        n+=1
                    if south in graph and source in graph[south] and not graph.nodes[south]['explored'] and south not in crds:
                        s+=1
                    if east in graph and source in graph[east] and not graph.nodes[east]['explored'] and east not in crds:
                        e+=1
        return [n,s,e,w],bridges