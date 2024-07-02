from igraph import Graph
import numpy as np
from typing import List, Tuple, Self

class Map:
    '''
    A class to represent a map.

    Attributes:
        width (int): The width of the map.
        height (int): The height of the map.
        obstacles_perc (int): The percentage of obstacles in the map.
        g (Graph): The graph representing the map.
        array (np.array): A 2D array representing the map. 0 means the cell is
                            crossable, 1 means it is an obstacle.
        jump_perc (int): Probability of taking a random node while building
                        the map. Higher values will make the obstacles more
                        grouped. Default is 25.
        shuffle_edges (bool): Whether to shuffle the edges of the graph while
                            building the map. Default is True.
    '''
    g : Graph = None
    array : np.array = None


    def __init__(self, width: int, height: int, obstacles_perc: int, array: np.ndarray = None, jump_perc: int = 25, shuffle_edges: bool = True) -> None:
        self.width = width
        self.height = height
        self.obstacles_perc = obstacles_perc
        self.jump_perc = jump_perc
        self.shuffle_edges = shuffle_edges
        self.generate_graph()
        self.init_obstacles(array)
        if array is None:
            arr = [0 if self.g.vs[i]["crossable"] else 1 for i in range(self.g.vcount())]
            self.array = np.array(arr).reshape(self.width, self.height)
        else:
            self.array = array
        self.check_values()


    @classmethod
    def from_array(cls, array: np.array) -> Self:
        '''
        Create a Map object from a 2D array.

        Args:
            array (np.array): A 2D array representing the map. 0 means the cell is
                            crossable, 1 means it is an obstacle.

        Returns:
            Map: A Map object.
        '''
        width = array.shape[1]
        height = array.shape[0]
        obstacles_perc = int(np.floor(100 * np.sum(array) / (width * height)))
        return cls(width, height, obstacles_perc, array)
    

    def check_values(self):
        '''
        Check if the values of the attributes are valid.

        Raises:
            ValueError: If any of the values are invalid.
        '''

        if self.width <= 0:
            raise ValueError("Width must be greater than 0.")
        if self.height <= 0:
            raise ValueError("Height must be greater than 0.")
        if self.obstacles_perc < 0 or self.obstacles_perc > 100:
            raise ValueError("Obstacles percentage must be between 0 and 100.")
        if self.jump_perc < 0 or self.jump_perc > 100:
            raise ValueError("Jump percentage must be between 0 and 100.")
        if self.array is not None and (self.array.shape[0] != self.height or self.array.shape[1] != self.width):
            raise ValueError("Array dimensions must match the width and height.")
        if int(np.sum(self.array.flatten())) != int(np.ceil(self.width*self.height*self.obstacles_perc/100)):
            raise ValueError(f"Obstacles percentage must match the array. Expected {np.sum(self.array.flatten())} but got {int(np.ceil(self.width*self.height*self.obstacles_perc/100))}")
    

    def generate_graph(self) -> None:
        '''
        Generates the graph representing the map and stores it in the attribute g.
        The graph is a grid graph with width x height nodes and edges connecting
        each node to its 4 neighbors.

        Returns:
            None
        '''

        edges = []
        for i in range(self.height):
            for j in range(self.width):
                node_id = i * self.width + j
                if i != 0:
                    edges.append((node_id, node_id - self.width))
                if j != 0:
                    edges.append((node_id, node_id - 1))
        self.g = Graph(edges=edges, directed=False)


    def create_obstacles(self) -> None:
        '''
        Creates the obstacles in the map. The obstacles are created by traversing
        the graph and marking some nodes as valid. The percentage of obstacles
        is given by the attribute obstacles_perc. The percentage of random jumps
        while traversing the graph is given by the attribute jump_perc. The attribute
        shuffle_edges determines whether the edges are shuffled while traversing the
        graph. The method stores the crossable attribute in each node of the graph in 
        the class attribute g.
        '''
        count = 0
        source = np.random.choice(range(0, self.g.vcount()), 1, replace=False)
        available_nodes = source.tolist()
        self.g.vs['crossable'] = False
        
        obs = int(np.ceil(self.g.vcount() * self.obstacles_perc / 100))
        while count < self.g.vcount() - obs:
            if np.random.rand() <= self.jump_perc/100:
                current_node = np.random.choice(available_nodes, 1)[0]
            else:
                current_node = available_nodes[-1]
            self.g.vs[current_node]['crossable'] = True
            available_nodes.remove(current_node)
            count += 1
            available_edegs = self.g.incident(current_node)
            if self.shuffle_edges:
                np.random.shuffle(available_edegs)
            for e in available_edegs:
                e = self.g.es[e]
                new_node = e.target if e.source == current_node else e.source
                if not self.g.vs[new_node]['crossable'] and new_node not in available_nodes:
                    available_nodes.append(new_node)


    def init_obstacles(self, array: np.array = None) -> None:
        """
        Initializes the obstacles in the map. If array is None, it creates the obstacles
        using the create_obstacles method. Otherwise, it sets the crossable attribute
        of each node in the graph according to the array.

        Args:
            array (np.array, optional): A 2D array representing the map. 0 means the cell is
                                        crossable, 1 means it is an obstacle. Defaults to None.
        
        Returns:
            None
        """
        if array is None:
            self.create_obstacles()
        else:
            for i in range(self.height):
                for j in range(self.width):
                    node_id = i * self.width + j
                    self.g.vs[node_id]['crossable'] = array[i, j]


    def to_pddl(self, source_target: Tuple[int, int]) -> str:
        '''
        Converts the map to a PDDL file.

        Args:
            source_target (Tuple[int, int]): Tuple with the source and target

        Returns:
            str: The PDDL file as a string.
        '''
        source, target = source_target
        indent = '    '
        s = '(define (problem p01) (:domain map)\n\n'
        s += f'(:objects\n{indent}'
        for i in range(self.height):
            for j in range(self.width):
                s += f'c{i*self.width+j} '
        s += '- cell\n'
        s += f'{indent}a - agent\n'
        s += ')\n\n\n'
        s += '(:init\n'
        for i in range(self.height):
            for j in range(self.width):
                if i > 0:
                    if self.array[i, j] == 0 and self.array[i-1, j] == 0:
                        s += f'{indent}(is_up c{(i-1)*self.width+j} c{i*self.width+j})\n'
                        s += f'{indent}(is_down c{i*self.width+j} c{(i-1)*self.width+j})\n'
                if j > 0:
                    if self.array[i, j] == 0 and self.array[i, j-1] == 0:
                        s += f'{indent}(is_left c{i*self.width+j-1} c{i*self.width+j})\n'
                        s += f'{indent}(is_right c{i*self.width+j} c{i*self.width+j-1})\n'
        s += f'{indent}(in a c{source})\n'
        s += f')\n\n\n'
        s += '(:goal (and\n'
        s += f'{indent}(in a c{target})\n'
        s += '))\n'
        s += ')'
        return s

    
    def __str__(self) -> str:
        """
        Returns a string representation of the map.

        Returns:
            str: The string representation of the map.
        """
        return f'{self.array}'
    

    def select_source_target(self, source: int = None, target: int = None) -> Tuple[int, int]:
        """
        Selects the source and target nodes for the map. If source and target are None,
        it selects two random crossable nodes. If source is not None, it selects a random
        crossable node for the target. If target is not None, it selects a random crossable
        node for the source.

        Args:
            source (int, optional): The source node. Defaults to None.
            target (int, optional): The target node. Defaults to None.

        Raises:
            ValueError: If the source or target nodes are not crossable.

        Returns:
            Tuple[int, int]: The source and target nodes.
        """
        valid_nodes = [i for i in range(self.g.vcount()) if self.g.vs[i]['crossable']]
        if source is None and target is None:
            (source, target) = np.random.choice(valid_nodes, 2, replace=False)
        elif source is not None:
            if source not in valid_nodes:
                raise ValueError(f'The source node {source} is not crossable.')
            target = np.random.choice(valid_nodes - {source}, 1)[0]
        elif target is not None:
            if target not in valid_nodes:
                raise ValueError(f'The target node {target} is not crossable.')
            source = np.random.choice(valid_nodes - {target}, 1)[0]
        return source, target
    

    def select_sources_targets(self, n: int) -> List[Tuple[int, int]]:
        """
        Selects n pairs of source and target nodes for the map.

        Args:
            n (int): The number of pairs to select.

        Returns:
            List[Tuple[int, int]]: A list of n pairs of source and target nodes.
        """
        tuples = []
        valid_nodes = [i for i in range(self.g.vcount()) if self.g.vs[i]['crossable']]
        for i in range(len(valid_nodes)):
            for j in range(len(valid_nodes)):
                if i != j:
                    tuples.append((valid_nodes[i], valid_nodes[j]))
        if n > len(tuples):
            print(f'The number of possible pairs is {len(tuples)}. Returning all of them.')
            return tuples
        
        selected = np.random.choice(range(len(tuples)), n, replace=False)
        return [tuples[i] for i in selected]