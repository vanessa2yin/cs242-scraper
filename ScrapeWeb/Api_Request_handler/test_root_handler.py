from unittest import TestCase

from Api_Request_handler.Root_handler import app
import json


class TestRootHandler(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_actors_by_attr(self):
        response1 = self.app.get('/actors?name=Al')
        self.assertEqual(1, len(json.loads(response1.data)[0]))
        response2 = self.app.get('/actors?age=35')
        self.assertEqual(1, len(json.loads(response2.data)[0]))
        response3 = self.app.get('/actors?total_gross=100000000')
        self.assertEqual(5, len(json.loads(response3.data)[0]))
        response4 = self.app.get('/actors?movies=Syriana')
        self.assertEqual(1, len(json.loads(response4.data)[0]))

    def test_get_movies_by_attr(self):
        response1 = self.app.get('/movies?name=es')
        self.assertEqual(5, len(json.loads(response1.data)[0]))
        response2 = self.app.get('/movies?year=2014')
        self.assertEqual(5, len(json.loads(response2.data)[0]))
        response3 = self.app.get('/movies?actors=Clive Owen')
        self.assertEqual(1, len(json.loads(response3.data)[0]))

    def test_get_actor_by_name(self):
        response1 = self.app.get('/actors/Jonah Hill')
        self.assertEqual(35, json.loads(response1.data)['Jonah Hill']['age'])
        response2 = self.app.get('/actors/TestFail')
        self.assertEqual("400 BAD REQUEST", response2.status)

    def test_get_movie_by_name(self):
        response1 = self.app.get('/movies/A Single Man')
        self.assertEqual(2009, json.loads(response1.data)['A Single Man']['year'])
        response2 = self.app.get('/movies/TestFail')
        self.assertEqual("400 BAD REQUEST", response2.status)

    def test_put_actor_info(self):
        update_info_dict = {"total_gross": 1304285, "age": 60}
        response1 = self.app.put('/actors/Oscar Isaac', data=json.dumps(update_info_dict))
        self.assertEqual("204 NO CONTENT", response1.status)
        response2 = self.app.get('/actors/Oscar Isaac')
        self.assertEqual(1304285, json.loads(response2.data)['Oscar Isaac']['total_gross'])
        self.assertEqual(60, json.loads(response2.data)['Oscar Isaac']['age'])
        self.assertEqual("200 OK", response2.status)

    def test_put_movie_info(self):
        update_info_dict = {"box_office": 500}
        response1 = self.app.put('/movies/The Descendants', data=json.dumps(update_info_dict))
        self.assertEqual("204 NO CONTENT", response1.status)
        response2 = self.app.get('/movies/The Descendants')
        self.assertEqual(500, json.loads(response2.data)['The Descendants']['box_office'])
        self.assertEqual("200 OK", response2.status)

    def test_post_actor_info(self):
        new_info_dict = {"name": "Cute Yuki", "total_gross": 12345, "age": 2, "movies": ["Tom and Jerry", "Sunset"]}
        response1 = self.app.post('/actors', data=json.dumps(new_info_dict))
        self.assertEqual("201 CREATED", response1.status)
        response2 = self.app.get('/actors/Cute Yuki')
        self.assertEqual(2, json.loads(response2.data)['Cute Yuki']['age'])

    def test_post_movies_info(self):
        new_info_dict = {"name": "Happy CS242", "year": 2019, "box_office": 9999, "actors": ["Vanessa"]}
        response1 = self.app.post('/movies', data=json.dumps(new_info_dict))
        self.assertEqual("201 CREATED", response1.status)
        response2 = self.app.get('/movies/Happy CS242')
        self.assertEqual(9999, json.loads(response2.data)['Happy CS242']['box_office'])

    def test_delete_actor_by_name(self):
        new_info_dict = {"name": "Test Actor", "total_gross": 12345, "age": 2, "movies": ["Tom and Jerry", "Sunset"]}
        response1 = self.app.post('/actors', data=json.dumps(new_info_dict))
        self.assertEqual("201 CREATED", response1.status)
        response2 = self.app.delete('/actors/Test Actor')
        self.assertEqual("204 NO CONTENT", response2.status)
        response3 = self.app.get('/actors/Test Actor')
        self.assertEqual("400 BAD REQUEST", response3.status)

    def test_delete_movie_by_name(self):
        new_info_dict = {"name": "Test Movie", "year": 2019, "box_office": 9999, "actors": ["Vanessa"]}
        response1 = self.app.post('/movies', data=json.dumps(new_info_dict))
        self.assertEqual("201 CREATED", response1.status)
        response2 = self.app.delete('/movies/Test Movie')
        self.assertEqual("204 NO CONTENT", response2.status)
        response3 = self.app.get('/movies/Test Movie')
        self.assertEqual("400 BAD REQUEST", response3.status)
