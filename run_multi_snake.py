import numpy as np
from multi_snake_mdp import MDP
from multi_snake_engine import BFSengine
from gridngraph import GridnGraph
import time
import networkx as nx
from random import sample

#Define the map
l,b=50,50
grid=np.zeros((l,b))
grid[int(l/2),:]=1
grid[int(l/2),int(b/2)]=0
grid[int(l/2),int(b/2)+1]=0
plt.imshow(grid)

g=GridnGraph()
n=5
#moves1=[[x1,y1],[x1,y1]]
#moves2=[[x2,y2],[x2,y2]]
l,b=grid.shape
graph=g.makegraph(grid)
nodes=sample(list(graph.nodes()), n)
crds=[]
for node in nodes:
    crds.append([int(node/b),node%b])
moves=[]
print(crds)
#initialize moves array to capture moves of n agents
for i in range(n):
    moves.append([crds[i],crds[i]])
game=MDP()
engine=BFSengine(l,b)
snapshots=[]
stepsbfs={}
stepsbfs[i]=0
while len(graph):
    for agent in range(n):
        actiontuple=engine.action_list(crds,agent,grid,graph,10)
        crds,moves,grid,graph=game.mdp(crds,moves,agent,grid,graph,actiontuple)

print('Number of steps taken {}'.format(len(moves)))
