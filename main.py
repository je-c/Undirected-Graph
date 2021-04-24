import sys
import random
from graph import Graph
from tests import UnitTest

"""
Main
============

Allows for command line inputs to build a random graph and to search between specified
or randomly chosen vertices.

Usage:
    To be run as main, builds test cases for the program from command line inputs.
"""

def returnValidInput(msg):
    """
    Runs a typecheck on incomping user input
    """
    try:
        input_msg = int(
            input(
                msg
            )
        )
    except ValueError:
        print('Invalid input. Please retry and enter an integer!')
        quit()

    return input_msg

def main():
    """
    Handles incoming command line arguments and generates a randomised, undirected graph.
    If desired, can perform shortest path computation between initial and specified vertex, or randomises
    the goal vertex.
    """
    if sys.argv[1].lower() == 'test': 
        return UnitTest.BuildTestCase()

    if sys.argv[1].lower() ==  'build':
        depth = returnValidInput(
            'Enter an integer value for desired number of layers in the graph: '
        )

        branching_complexity = returnValidInput(
            'Enter an integer value for desired maximum branching factor: '
        )
        
        G = Graph()
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

        next_step = input(
            'Graph created. Would you like to select a node to traverse to by index? [y/n]: '
        )
        
        if next_step.lower() == 'y':
            idx = returnValidInput(
                f'Enter a single integer between 0 and {num_nodes-1}: '
            )
            start, finish = Nodes[0], Nodes[idx]
            print(f'Finding path between nodes at index 0, {idx}')
            print(
                G.find_path(
                    start,
                    finish
                )
            )

        else: 
            idx = random.randint(0,num_nodes)
            start, finish = Nodes[0], Nodes[idx]
            print(f'Finding path between nodes at index 0, {idx}')
            print(
                G.find_path(
                    start,
                    finish
                )
            )
    else:
        print('No valid directive entered, please supply a directive. [build/test]')
        quit()

if __name__ == '__main__':
    main()