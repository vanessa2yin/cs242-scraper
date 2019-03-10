class ActorNode:
    def __init__(self, actor_dict):
        self._type = "actor"        # cannot be changed
        self._total_gross = 0       # preset
        self._neighbors = []        # preset, will not included if transfer to json format
        self._connections = 0       # preset, will not included if transfer to json format

        # set other fields by an actor_dict
        for key, value in actor_dict.items():
            if key == 'name':
                self._name = value
            if key == 'age':
                self._age = value
            if key == 'year':
                self._year = value              # only set when the input is NOT provided_data.json file
            if key == 'movies':
                self._movies = value
            if key == 'total_gross':            # only set when the input is provided_data.json file
                self._total_gross = value

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def year(self):
        return self._year

    @property
    def movies(self):
        return self._movies

    @property
    def total_gross(self):
        return self._total_gross

    @property
    def neighbors(self):
        return self._neighbors

    @property
    def connections(self):
        return self._connections

    @total_gross.setter
    def total_gross(self, value):
        self._total_gross = value

    @connections.setter
    def connections(self, value):
        self._connections = value

    def add_movies(self, movie_name):
        self._movies.append(movie_name)

    def add_neighbors(self, node):
        self._neighbors.append(node)

    def delete_neighbor(self, node):
        if node in self.neighbors:
            self.neighbors.remove(node)
        if node.name in self.movies:
            self.movies.remove(node.name)

    def change_to_dict(self):
        actor_dict = {"type": "actor",
                      "name": self.name,
                      "age": self.age,
                      # "year": self.year,
                      "total_gross": self.total_gross,  # will be changed in graph
                      "movies": self.movies}
        return actor_dict

    def change_to_text(self):
        return "name: " + self.name + "<br>" + "age: " + str(self.age) + "<br>" + "total_gross: " + str(self.total_gross)

    # update actor_node by info in new_dict
    # helper for api PUT method
    def update_by_dict(self, update_dict):
        for key, value in update_dict.items():
            if key == 'name':
                self._name = value
            if key == 'age':
                self._age = value
            if key == 'movies':
                self._movies = value
            if key == 'total_gross':
                self._total_gross = value
