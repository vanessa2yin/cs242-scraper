import json
from unittest import TestCase

from JsonGraph import Graph
from JsonGraph.__init__ import main


class TestGraph(TestCase):
    @classmethod
    def setUpClass(cls):
        scraped_data = ".././Crawler/data copy.json"
        cls.graph = Graph(scraped_data, False)

    def test_find_movie_gross(self):
        self.assertEqual(Graph.find_movie_gross(self.graph, "Mamma Mia! Here We Go Again"), 394000000)

    def test_list_movies_of_actor(self):
        self.assertEqual(Graph.list_movies_of_actor(self.graph, "Idris Elba"), [])
        self.assertEqual(len(Graph.list_movies_of_actor(self.graph, "Kat Dennings")), 18)

    def test_list_actors_of_movie(self):
        result = ["Luke Wilson", "Eddie Izzard", "J. K. Simmons", "Lewis Black", "Kenan Thompson",
                  "Mae Whitman", "Jorge Garcia", "Matt Dillon", "Sam Elliott"]
        self.assertEqual(Graph.list_actors_of_movie(self.graph, "Rock Dog"), result)

    def test_list_top_n_actors_with_highest_grossing(self):
        result = [('Morgan Freeman', 1478645424.3410835), ('Mark Ruffalo', 1388182722.8246493),
                  ('Benedict Cumberbatch', 1174366097.5609756), ('Chris Hemsworth', 1140525353.673485),
                  ('Anna Faris', 1125487943.7627554)]
        self.assertEqual(Graph.list_top_n_actors_with_highest_grossing(self.graph, 5), result)
        self.assertEqual(Graph.list_top_n_actors_with_highest_grossing(self.graph, -1), [])

    def test_list_top_n_oldest_actors(self):
        result = [('Ellen Burstyn', 86), ('Alan Arkin', 84), ('Kris Kristofferson', 82), ('Morgan Freeman', 81),
                  ('Linda Lavin', 81)]
        self.assertEqual(Graph.list_top_n_oldest_actors(self.graph, 5), result)
        self.assertEqual(Graph.list_top_n_oldest_actors(self.graph, -1), [])

    def test_list_movies_for_a_year(self):
        result = ['Ernest & Celestine', 'The Twilight Saga: Breaking Dawn – Part 2', 'Bachelorette (film)',
                  'The Dark Knight Rises', 'Lincoln (film)', 'This Is 40', 'Liberal Arts (film)',
                  'The Dictator (2012 film)']
        self.assertEqual(Graph.list_movies_for_a_year(self.graph, 2012), result)

    def test_list_actors_for_a_year(self):
        result = ['Keira Knightley', 'Dave Franco', 'Amanda Seyfried', 'Kellan Lutz', 'Anna Kendrick']
        self.assertEqual(Graph.list_actors_for_a_year(self.graph, 1985), result)

    def test_get_movie_node(self):
        self.assertEqual(Graph.get_movie_node(self.graph, "THIS IS A FAKE MOVIE NAME"), None)

    def test_get_edge(self):
        self.assertEqual(Graph.get_edge(self.graph, "FAKE_A", "FAKE_B"), None)

    def test_save_to_json(self):
        Graph.save_to_json(self.graph, "test_output.json")
        with open ("test_output.json", 'r') as json_file:
            self.assertNotEqual(json.load(json_file), None)

    def test_get_type(self):
        self.assertEqual("actor", self.graph.actor_node_list[0].type)
        self.assertEqual("movie", self.graph.movie_node_list[0].type)

    def test_remove_neighbor(self):
        actor_node = self.graph.actor_node_list[0]
        movie_neighbor = actor_node.neighbors[0]
        original_len = len(actor_node.neighbors)
        actor_node.delete_neighbor(movie_neighbor)
        original_len_2 = len(movie_neighbor.neighbors)
        movie_neighbor.delete_neighbor(actor_node)
        self.assertEqual(len(actor_node.neighbors), original_len - 1)
        self.assertEqual(len(movie_neighbor.neighbors), original_len_2 - 1)

    def test_update_by_dict(self):
        actor_name = self.graph.actor_node_list[0].name
        movie_name = self.graph.movie_node_list[0].name
        self.graph.update_actor_info(actor_name, {'name': 'test', 'age': 100, 'movies': [], 'total_gross': 0})
        self.graph.update_movie_info(movie_name, {'name': 'test_movie', 'year': 2000, 'box_office': 999, 'actors': []})
        self.assertEqual("test", self.graph.actor_node_list[0].name)
        self.assertEqual("test_movie", self.graph.movie_node_list[0].name)

    def test_query(self):
        self.assertEqual(1, len(self.graph.query_by_actor_info({'name': 'Clive Owen'})))
        self.assertEqual(1, len(self.graph.query_by_movie_info({'name': 'A Single Man'})))
        movie_name = self.graph.movie_node_list[0].name
        self.assertEqual(movie_name, self.graph.query_by_movie_name(movie_name)[movie_name]['name'])
        actor_name = self.graph.actor_node_list[0].name
        self.assertEqual(actor_name, self.graph.query_by_actor_name(actor_name)[actor_name]['name'])

    def test_data_processing(self):
        main()
