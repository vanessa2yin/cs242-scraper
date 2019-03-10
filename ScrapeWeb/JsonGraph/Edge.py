from JsonGraph.Movie_node import MovieNode


class Edge:
    # u = MovieNode, v = ActorNode
    def __init__(self, u, v, weight):
        if isinstance(u, MovieNode):
            self._u = u
            self._v = v
        else:
            self._u = v
            self._v = u
        self._weight = weight

    @property
    def u(self):
        return self._u

    @property
    def v(self):
        return self._v

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    def equals(self, u, v):
        return u == self.u and v == self.v or u == self.v and v == self.u
