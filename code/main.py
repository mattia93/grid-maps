from env import navigation_env
import os
import matplotlib.pyplot as plt
import numpy as np
from map_utils import Map
from igraph import Graph



def generate_map(rows: int, cols: int, obstacles_perc: int):
    obs = np.ceil(obstacles_perc * rows * cols/100)
    edges = []
    for i in range(rows):
        for j in range(cols):
            node_id = i * cols + j
            if i != 0:
                edges.append((node_id, node_id - cols))
            if j != 0:
                edges.append((node_id, node_id - 1))
    g = Graph(edges=edges, directed=False)
    g = walk_graph(g, obs)
    return create_map(g, rows, cols)

def walk_graph(g : Graph, obs: int):
    g.vs['visited'] = False
    count = 0
    source = np.random.randint(0, g.vcount())
    available_nodes = [source]
    current_node = np.random.choice(available_nodes, 1)[0]
    while count < g.vcount() - obs:
        g.vs[current_node]['visited'] = True
        available_nodes.remove(current_node)
        count += 1
        print(f'Visiting node {current_node}, {count} nodes visited.')
        available_edegs = g.incident(current_node)
        for e in available_edegs:
            e = g.es[e]
            new_node = e.target if e.source == current_node else e.source
            if not g.vs[new_node]['visited'] and new_node not in available_nodes:
                available_nodes.append(new_node)
        print(f'Available nodes: {available_nodes}')
        current_node = np.random.choice(available_nodes, 1)[0]

    return g

def create_map(g: Graph, rows: int, cols: int):
    map = [0 if g.vs[i]['visited'] else 1 for i in range(g.vcount())]
    return np.array(map).reshape(rows, cols)


if __name__ == '__main__':
    map = Map(3, 3, 30)
    map1 = Map.from_array(map.array)
    print(f'{map1}' == f'{map}')


    