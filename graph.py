"""
Usage:
    Contains the graph, requires the connection to vertices and edges.
"""
import math
from vertex import Vertex
from edge import Edge

class EdgeAlreadyExists(Exception):
    """Raised when edge already exists in the graph"""
    def __init__(self, message):
        super().__init__(message)


class Graph:
    """
    Graph Class
    -----------

    Represents the graph of vertices.

    Attributes:
        * vertices (list): The list of vertices
    """

    def __init__(self):
        """
        Initialise an empty graph
        """
        self._vertices = []

    def insert_vertex(self, x_pos, y_pos):
        """
        Insert the vertex storing the y_pos and x_pos
            * :param x_pos (float): The x position of the new vertex.
            * :param y_pos (float): The y position of the new vertex.
        :return: The new vertex, also stored in the graph.
        """

        v = Vertex(x_pos, y_pos)
        self._vertices.append(v)
        return v

    def insert_edge(self, u, v):
        """
        Inserts the edge between vertex u and v.
            * :param u (Vertex): Vertex U
            * :param v (Vertex): Vertex V
        :return: The new edge between U and V.
        """

        e = Edge(u, v)

        # Check that the edge doesn't already exist
        for i in u.edges:
            if i == e:
                # Edge already exists.
                raise EdgeAlreadyExists("Edge already exists between vertex!")

        # Add the edge to both nodes.
        u.add_edge(e)
        v.add_edge(e)

    def remove_vertex(self, v):
        """
        Removes the vertex V from the graph.
            * :param v (Vertex):  The pointer to the vertex to remove
        """

        # Remove it from the list
        del self._vertices[self._vertices.index(v)]

        # Go through and remove all edges from that node.
        while len(v.edges) != 0:
            e = v.edges.pop()
            u = self.opposite(e, v)
            u.remove_edge(e)

    @staticmethod
    def distance(u, v):
        """
        Get the distance between vertex u and v.
            * :param u (Vertex): A vertex to get the distance between.
            * :param v (Vertex): A vertex to get the distance between.
        :return: The Euclidean distance between two vertices.
        """

        # Euclidean Distance
        # sqrt( (x2-x1)^2 + (y2-y1)^2 )

        return math.sqrt(((v.x_pos - u.x_pos)**2) + ((v.y_pos - u.y_pos)**2))

    @staticmethod
    def opposite(e, v):
        """
        Returns the vertex at the other end of v.
            * :param e: The edge to get the other node.
            * :param v: Vertex on the edge.
        :return: Vertex at the end of the edge, or None if error.
        """
        if v not in (e.u, e.v): return None

        if v == e.u: return e.v
        
        return e.u

    def depth_find(self, v):
        """
        Returns the distance to the vertex W that is furthest from V.
            * :param v: The vertex to start at.
        :return: The distance of the vertex W furthest away from V.
        """

        furthest_dist = 0
        cur_dist = 0
        for vert in self._vertices:
            x_1, y_1 = v.x_pos,  v.y_pos
            x_2, y_2 = vert.x_pos, vert.y_pos

            cur_dist = math.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)

            if cur_dist > furthest_dist:
                furthest_dist = cur_dist

        return furthest_dist

    def find_path(self, b, s, r=math.inf):
        """
        Find a path from vertex B to vertex S, such that the distance from B to
        every vertex in the path is within R.  If there is no path between B
        and S within R, then return None.
            * :param b: Vertex B to start from.
            * :param s: Vertex S to finish at.
            * :param r: The maximum range of the radio.
        :return: The LIST of the VERTICES in the path.
        """
        path = self.dijkstra_traverse_path(b, s)
        furthest_node = 0
        if path == None:
            for i in self._vertices:
                return [i]
        
        else:
            if self.distance(b,s) <= r:
                for i in range(0, len(path)):
                    if i == (len(path) - 1):
                        if furthest_node < self.distance(path[i], path[0]):
                            furthest_node = self.distance(path[i], path[0])
                    else:
                        if furthest_node < self.distance(path[i], path[i+1]):
                            furthest_node = self.distance(path[i], path[i+1])

                if furthest_node <= r:
                    return path
                
                else:
                    return None
            
            else:
                return None
        
    def minimum_range(self, b, s):
        """
        Returns the minimum range required to go from Vertex B to Vertex S.
            * :param b: Vertex B to start from.
            * :param s: Vertex S to finish at.
        :return: The minimum range in the path to go from B to S.
        """

        path = self.dijkstra_traverse_path(b, s)
        max_dist = 0
        for i in range(0, len(path)):
            if max_dist < self.distance(path[0], path[i]):
                max_dist = self.distance(path[0], path[i])
                
        return max_dist

    def move_vertex(self, v, new_x, new_y):
        """
        Move the defined vertex. If there is already a vertex there, do nothing.
            * :param v: The vertex to move
            * :param new_x: The new X position
            * :param new_y: The new Y position
        """

        loc_not_empty = False
        for vertex in self._vertices:
            if vertex.x_pos == new_x and vertex.y_pos == new_y:
                loc_not_empty = True
            else:
                continue

        if not loc_not_empty:
            v.move_vertex(new_x, new_y)


    def retrace_path(self, parent, s, end):
        """
        Retrace a path from from goal node to start node in the graph.
            * :param parent: Parent of node
            * :param s: Vertex S to finish at.
            * :param end: Vertex at the other end of the graph edge
        :return: The LIST of the VERTICES in the path.
        """
        if end not in parent:
            return None
            
        cur = end
        path = [cur]

        while cur in parent:
            cur = parent[cur]
            path.append(cur)
            if cur == s:
                path = list(reversed(path))
                return path

        return None

    def dijkstra_traverse_path(self, s, end):
        """
        Implement Dijkstra's algorithm to traverse the graph and find a shortest path
            * :param s: Vertex S to finish at.
            * :param end: Vertex at the other end of the graph edge
        :return: The LIST of the VERTICES in the path.
        """
        dist_dict, parent, priorityQ, seen_dist = [{} for i in range(4)]
        
        if len(s.edges) == 0:
            return None

        for v in self._vertices:
            for e in v.edges:
                if v in dist_dict:
                    dist_dict[v].update({self.opposite(e, v) : self.distance(v, self.opposite(e, v))})
                else:
                    dist_dict[v] = {self.opposite(e, v) : self.distance(v, self.opposite(e, v))}
            
            parent[v] = None
            priorityQ[v] = math.inf 

        cur = s
        distance_curNode = 0
        priorityQ[cur] = distance_curNode

        if len(self._vertices) == 1:
            single_path = [self._vertices[0]]
            return single_path

        else:
            while priorityQ:
                if cur in dist_dict:
                    for incident, distance in dist_dict[cur].items():
                        if incident not in priorityQ:
                            continue
                        
                        else:
                            newDist = distance_curNode + distance

                            if priorityQ[incident] >= newDist:
                                priorityQ[incident] = newDist
                                parent[incident] = cur
                        
                    seen_dist[cur] = distance_curNode
                    del priorityQ[cur]

                    priorityQ_nodes = [
                        i for i in priorityQ.items() if i[1]
                    ]

                    if priorityQ_nodes:
                        cur, distance_curNode = sorted(priorityQ_nodes, key = lambda node: node[1])[0]
                
                else:
                    break

            return self.retrace_path(parent, s, end)

