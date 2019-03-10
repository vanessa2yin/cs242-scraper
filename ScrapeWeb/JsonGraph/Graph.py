import json

from Api_Request_handler import Query_util
from JsonGraph import ActorNode
from JsonGraph.Edge import Edge
from JsonGraph.Movie_node import MovieNode


class Graph:
    def __init__(self, fname, is_provided):
        """
        initialize graph, create nodes and connect them.
        if is_provided is True, input json will have total_gross setup, so no need to calculate edge weight again
        if is_provided is False, input json will have no total_gross setup and therefore need preset total_gross
        to 0. More details can be found in Actor_node and Movie_node.
        :param fname: input json file name
        :param is_provided: True if json file is provided, False if json file is given by crawler
        """
        self.actor_node_list = []  # ActorNode
        self.movie_node_list = []  # MovieNode
        self.edge_list = []  # Edge

        with open(fname, "r") as json_file:
            data = json.load(json_file)
        data_dict = data[0]

        # add actor_node and movie_node into lists
        for name, info in data_dict.items():
            self.setup_graph_nodes(info)
        if is_provided:
            for name, info in data[1].items():
                self.setup_graph_nodes(info)

        # add edges into lists (movie -> action) and assign gross to each actor
        if is_provided:
            self.setup_graph_edges_with_total_gross()
            self.setup_actor_connections()  # for data analysis
        else:
            self.setup_graph_edges()

    def find_movie_gross(self, movie_name):
        """
        find gross of movie node
        :param movie_name: given movie name
        :return: gross of movie node
        """
        movie_node = self.get_movie_node(movie_name)
        if movie_node is not None:
            return movie_node.box_office

    def list_movies_of_actor(self, actor_name):
        """
        find movies of actor node
        :param actor_name: given actor name
        :return: movies of actor node
        """
        actor_node = self.get_actor_node(actor_name)
        if actor_node is not None:
            return actor_node.movies

    def list_actors_of_movie(self, movie_name):
        """
        find actors of movie node
        :param movie_name: given movie name
        :return: actors of movie node
        """
        movie_name = self.get_movie_node(movie_name)
        if movie_name is not None:
            return movie_name.actors

    # return (actor_name, grossing)
    def list_top_n_actors_with_highest_grossing(self, n):
        """
        find top n actors with highest total_gross
        :param n: number of result user want
        :return: a list of (actor_name, total_gross) sorted by total_gross
        """
        if n <= 0:
            return []
        grossing_list = []
        for actor_node in self.actor_node_list:
            grossing_list.append((actor_node.name, actor_node.total_gross))
        grossing_list.sort(key=lambda tup: tup[1], reverse=True)
        return grossing_list[0:n]

    # return (actor_name, age)
    def list_top_n_oldest_actors(self, n):
        """
        find top n actors with biggest ages
        :param n: number of result user want
        :return: a list of (actor_name, age) sorted by age
        """
        if n <= 0:
            return []
        age_list = []
        for actor_node in self.actor_node_list:
            age_list.append((actor_node.name, actor_node.age))
        age_list.sort(key=lambda tup: tup[1], reverse=True)
        return age_list[0:n]

    def list_movies_for_a_year(self, year):
        """
        find all movies released in a given year
        :param year: release year of the movies
        :return: a list of all movies released in a given year
        """
        result = []
        for movie_node in self.movie_node_list:
            if movie_node.year == year:
                result.append(movie_node.name)
        return result

    def list_actors_for_a_year(self, year):
        """
        find all actors born in a given year
        :param year: born year of the actors
        :return: a list of all actors born in a given year
        """
        result = []
        for actor_node in self.actor_node_list:
            if actor_node.year == year:
                result.append(actor_node.name)
        return result

    def get_hub_actors_rank(self, n):
        """
        data analysis question 1
        :param n: number of hub actors user want
        :return: list of hub actor's name
        """
        if n <= 0:
            return []
        connections_list = []
        for actor_node in self.actor_node_list:
            connections_list.append((actor_node.name, actor_node.connections))
        connections_list.sort(key=lambda tup: tup[1], reverse=True)
        return connections_list[0:n]

    def get_highest_gross_rank(self):
        """
        data analysis question 2
        :return: a list of (name, total_gross, age) sorted by grossing value
        """
        grossing_age_list = []
        for actor_node in self.actor_node_list:
            grossing_age_list.append((actor_node.name, actor_node.total_gross, actor_node.age))
        grossing_age_list.sort(key=lambda tup: tup[1], reverse=True)
        return grossing_age_list

    def setup_graph_nodes(self, info):
        """
        add items in dictionary into graph as appropriate nodes
        :param info: one node dict
        """
        for key, value in info.items():
            if (key == 'type' and value == 'actor') or \
               (key == 'json_class' and value == 'Actor'):
                actor_node = ActorNode(info)
                self.actor_node_list.append(actor_node)
            if (key == 'type' and value == 'movie') or \
               (key == 'json_class' and value == 'Movie'):
                movie_node = MovieNode(info)
                self.movie_node_list.append(movie_node)

    def setup_graph_edges(self):
        """
        will be called if total_gross is not set in input json
        connect from movie node to its actors and add custom edge weight
        """
        for movie_node in self.movie_node_list:
            if len(movie_node.actors) != 0:
                age_total_count = 0
                for actor_name in movie_node.actors:
                    # if it exists in graph, connect it with movie node
                    actor_node = self.get_actor_node(actor_name)
                    if actor_node is not None:
                        self.add_edge(movie_node, actor_node, 0)
                        age_total_count += actor_node.age

                # add gross assigned to the edge weight and add gross weight of the actors
                if age_total_count > 0:
                    for actor_node in movie_node.neighbors:
                        gross_assigned = actor_node.age/age_total_count * movie_node.box_office
                        self.set_edge_weight(movie_node, actor_node, gross_assigned)
                        actor_node.total_gross += gross_assigned

    def setup_graph_edges_with_total_gross(self):
        """
        will be called only if total_gross is already set in input json
        connect from movie node to its actors and put actor's total_gross as edge weight
        """
        for movie_node in self.movie_node_list:
            for actor_name in movie_node.actors:
                actor_node = self.get_actor_node(actor_name)
                if actor_node is not None:
                    self.add_edge(movie_node, actor_node, actor_node.total_gross)

    def setup_actor_connections(self):
        """
        helper for data analysis question 1 (find hub actors)
        setup connections of actor node in the graph for data analysis
        """
        for movie_node in self.movie_node_list:
            connections = max(len(movie_node.neighbors) - 1, 0)
            for actor_node in movie_node.neighbors:
                actor_node.connections += connections

    def add_edge(self, u, v, weight):
        """
        make (u,v) a new edge and put into edge_list
        add the other node to their neighbors
        :param u: node one (convention: movie_node)
        :param v: node two (convention: actor_node)
        :param weight: given weight (convention: total_gross)
        """
        new_edge = Edge(u, v, weight)
        self.edge_list.append(new_edge)
        u.add_neighbors(v)
        v.add_neighbors(u)

    def remove_edge(self, u, v):
        """
        remove edge from the edge list and delete neighbors in each node
        will also change actor or movie list of each node
        :param u: node one (convention: movie_node)
        :param v: node two (convention: actor_node)
        """
        target_edge = self.get_edge(u, v)
        if target_edge is None:
            return
        self.edge_list.remove(target_edge)
        u.delete_neighbor(v)
        v.delete_neighbor(u)

    def get_actor_node(self, actor_name):
        """
        find the actor node and return
        :param actor_name: given actor_name of target node
        :return: actor node if found, None if not found
        """
        for node in self.actor_node_list:
            if node.name == actor_name:
                return node
        return None

    def get_movie_node(self, movie_name):
        """
        find the movie node and return
        :param movie_name: given movie_name of target node
        :return: movie node if found, None if not found
        """
        for node in self.movie_node_list:
            if node.name == movie_name:
                return node
        return None

    def get_edge(self, u, v):
        """
        find edge and return. no matter if it should be (u,v) or (v,u)
        :param u: node one (convention: movie_node)
        :param v: node two (convention: actor_node)
        """
        for edge in self.edge_list:
            if edge.equals(u, v):
                return edge
        return None

    def set_edge_weight(self, u, v, new_weight):
        """
        find edge and set its weight
        :param u: node one (convention: movie_node)
        :param v: node two (convention: actor_node)
        :param new_weight: given new weight
        """
        edge = self.get_edge(u, v)
        if edge is not None:
            edge.weight = new_weight

    def save_to_json(self, fname):
        """
        save the graph to a Json file
        :param fname: output file name
        """
        json_dict = {}
        for actor_node in self.actor_node_list:
            current_actor_dict = actor_node.change_to_dict()
            json_dict[actor_node.name] = current_actor_dict
        for movie_node in self.movie_node_list:
            current_movie_dict = movie_node.change_to_dict()
            json_dict[movie_node.name] = current_movie_dict

        # Store json_dict as json file
        with open(fname, 'w') as outfile:
            array = [json_dict]
            json.dump(array, outfile, indent=2)

    @staticmethod
    def node_list_to_dict(node_list):
        """
        given a node list, transfer it to a dictionary that can be jsonified after
        :param node_list: given list of nodes
        :return: a dict wrapped in array format
        """
        json_dict = {}
        for node in node_list:
            current_dict = node.change_to_dict()
            json_dict[node.name] = current_dict
        array = [json_dict]
        return array

    def query_by_actor_info(self, attr_list):
        """
        query function for Get /actors?attr={attr_value}
        :param attr_list: attr_list parsed from url request
        :return: dict filtered
        """
        actor_list = []
        for actor_node in self.actor_node_list:
            if Query_util.is_valid_actor_for_query(actor_node, attr_list):
                actor_list.append(actor_node)
        return self.node_list_to_dict(actor_list)

    def query_by_movie_info(self, attr_list):
        """
        query function for Get /movies?attr={attr_value}
        :param attr_list: attr_list parsed from url request
        :return: dict filtered
        """
        movie_list = []
        for movie_node in self.movie_node_list:
            if Query_util.is_valid_movie_for_query(movie_node, attr_list):
                movie_list.append(movie_node)
        return self.node_list_to_dict(movie_list)

    def query_by_actor_name(self, actor_name):
        """
        query function for Get /actors/:{actor_name}
        :return: False if cannot find this node, return dict if find this node
        """
        wrapped_dict = {}
        actor_node = self.get_actor_node(actor_name)
        if actor_node is None:
            return False
        actor_dict = actor_node.change_to_dict()
        wrapped_dict[actor_node.name] = actor_dict
        return wrapped_dict

    def query_by_movie_name(self, movie_name):
        """
        query function for Get /movies/:{movie_name}
        :return: return False if cannot find this node, return dict if find this node
        """
        wrapped_dict = {}
        movie_node = self.get_movie_node(movie_name)
        if movie_node is None:
            return False
        movie_dict = movie_node.change_to_dict()
        wrapped_dict[movie_node.name] = movie_dict
        return wrapped_dict

    def update_actor_info(self, actor_name, update_dict):
        """
        update function for Put /actors/:{actor_name} with update info in request body
        :param actor_name: given actor_name from url request
        :param update_dict: new actor info, in dict format
        :return: return False if cannot find this node, return True if processed successfully
        """
        actor_node = self.get_actor_node(actor_name)
        if actor_node is None:
            return False
        actor_node.update_by_dict(update_dict)
        return True

    def update_movie_info(self, movie_name, update_dict):
        """
        update function for Put /movies/:{movie_name} with update info in request body
        :param movie_name: given movie_name from url request
        :param update_dict: new movie info, in dict format
        :return: return False if cannot find this node, return True if processed successfully
        """
        movie_node = self.get_movie_node(movie_name)
        if movie_node is None:
            return False
        movie_node.update_by_dict(update_dict)
        return True

    def insert_actor_dict(self, actor_info):
        """
        insert function for Post /actors with new info in request body
        :param actor_info: new actor info, in dict format
        :return: return False if new info is in invalid format, return True if processed successfully
        """
        new_actor_node = ActorNode(actor_info)
        if actor_info is None or 'name' not in actor_info.keys():  # not valid dict to insert
            return False
        self.actor_node_list.append(new_actor_node)
        for movie_node in self.movie_node_list:
            if actor_info['name'] in movie_node.actors:  # will only connect if movie has this actor
                self.add_edge(movie_node, new_actor_node, new_actor_node.total_gross)
        return True

    def insert_movie_dict(self, movie_info):
        """
        insert function for Post /actors with new info in request body
        :param movie_info: new movie info, in dict format
        :return: return False if new info is in invalid format, return True if processed successfully
        """
        new_movie_node = MovieNode(movie_info)
        if movie_info is None or 'name' not in movie_info.keys():  # not valid dict to insert
            return False
        self.movie_node_list.append(new_movie_node)
        for actor_node in self.actor_node_list:
            if actor_node.name in new_movie_node.actors:  # will only connect if movie has this actor
                self.add_edge(new_movie_node, actor_node, actor_node.total_gross)
        return True

    def delete_actor_node_by_name(self, actor_name):
        """
        delete function for Delete /actors/:{actor_name}
        :param actor_name: given actor_name from url request
        :return: return False if cannot find this node, return True if processed successfully
        """
        actor_node = self.get_actor_node(actor_name)
        if actor_node is None:
            return False
        for movie_node in actor_node.neighbors:     # disconnect with neighbors
            self.remove_edge(movie_node, actor_node)
        self.actor_node_list.remove(actor_node)
        return True

    def delete_movie_node_by_name(self, movie_name):
        """
        delete function for Delete /movies/:{movie_name}
        :param movie_name: given movie_name from url request
        :return: return False if cannot find this node, return True if processed successfully
        """
        movie_node = self.get_movie_node(movie_name)
        if movie_node is None:
            return False
        for actor_node in movie_node.neighbors:     # disconnect with neighbors
            self.remove_edge(movie_node, actor_node)
        self.movie_node_list.remove(movie_node)
        return True
