"""
Edge Module
============

Represents the edge in the undirected graph.
Contains the two connected vertices u and w.

Usage:
    * Not to be run as the main class.
    * Used as a link between vertices.

Example:
    u = Vertex(x1, y1)
    v = Vertex(x2, y2)
    # Undirected, so Edge(v, u) == Edge(u, v)
    e = Edge(v, u)
"""

class Edge:
    """
    Edge Class
    ----------

    Represents the edge between two vertices

    Attributes:
        * u (Vertex): The vertex connected.
        * v (Vertex): The vertex connected.
    """

    def __init__(self, u, v):
        """
        Initialises the edge with two vertices
            * :param u (Vertex): Vertex U connected with this edge.
            * :param v (Vertex): Vertex V connected with this edge.
        """
        self.u = u
        self.v = v

    def __eq__(self, other):
        """
        Overrides the base equality so we can check that
        two edges are equal to each other.
            * :param other: The other object we are comparing
        :return: Bool if equal
        """

        # If it's the same class, then it should have the same vertices.
        if isinstance(other, Edge):
            return (other.u == self.v or other.u == self.u) \
                and (other.v == self.u or other.v == self.v)

        # If it's not the same class, it's not equal
        return False

    def __repr__(self):
        """
        Defines the string representation of the edge.
        """

        return "<{}-{}>".format(self.u, self.v)

    def __hash__(self):
        """
        Makes the class hashable
        """
        return hash(repr(self))
