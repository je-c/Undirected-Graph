import math
import random
from vertex import Vertex
from graph import Graph
"""
Test Module
============

Generates a test case for the graph class, creating vertices/edges and computing a 
shortest path from the root node to a random node in the graph.
"""

class UnitTest:
    """
    UnitTest Class
    -------------

    Packages the BuildTestCase staticmethod. Runs without arguements.
    """
    @staticmethod
    def BuildTestCase():
        G = Graph()
        
        depth = random.randint(1, 9)
        branching_complexity = random.randint(1, 5)
        Nodes = [G.insert_vertex(0, 0)]

        for i in range(depth*branching_complexity):
            Nodes.append(
                G.insert_vertex(
                    random.randint(-10, 10),
                    random.randint(-10, 10)
                )
            )

        num_nodes = len(Nodes)
        for node in Nodes:
            for i in random.sample(range(num_nodes), random.randint(0, branching_complexity)):
                G.insert_edge(
                    node,
                    i
                )

        
        print(
            G.find_path(
                random.randint(0,num_nodes),
                random.randint(0,num_nodes)
            )
        )
