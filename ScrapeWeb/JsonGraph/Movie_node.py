class MovieNode:
    def __init__(self, movie_dict):
        self._type = "movie"            # cannot be changed
        self._neighbors = []            # preset, will not included if transfer to json format

        # set other fields by an actor_dict
        for key, value in movie_dict.items():
            if key == 'name':
                self._name = value
            if key == 'year':
                self._year = value
            if key == 'box_office':             # only set when the input is provided_data.json file
                self._box_office = value
            if key == 'actors':
                self._actors = value

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def year(self):
        return self._year

    @property
    def box_office(self):
        return self._box_office

    @property
    def actors(self):
        return self._actors

    @property
    def neighbors(self):
        return self._neighbors

    def add_actors(self, actor_name):
        self._actors.append(actor_name)

    def add_neighbors(self, node):
        self._neighbors.append(node)

    def delete_neighbor(self, node):
        if node in self.neighbors:
            self.neighbors.remove(node)
        if node.name in self.actors:
            self.actors.remove(node.name)

    def change_to_dict(self):
        movie_dict = {"type": "movie",
                      "name": self.name,
                      "year": self.year,
                      "box_office": self.box_office,
                      "actors": self.actors}
        return movie_dict

    def change_to_text(self):
        return "name: " + self.name + "<br>" + "year: " + str(self.year) + "<br>box_office: " + str(self.box_office)

    # update movie_node by info in new_dict
    # helper for api PUT method
    def update_by_dict(self, update_dict):
        for key, value in update_dict.items():
            if key == 'name':
                self._name = value
            if key == 'year':
                self._year = value
            if key == 'box_office':
                self._box_office = value
            if key == 'actors':
                self._actors = value
