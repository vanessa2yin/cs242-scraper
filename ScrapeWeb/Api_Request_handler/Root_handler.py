# coding=utf-8
from flask import Flask, jsonify, request, Response
from JsonGraph import Graph
from urllib.parse import urlparse, parse_qs
import json

app = Flask(__name__)
provided_data = "/Users/june/PycharmProjects/cs242/ScrapeWeb/Resource/provided_data.json"
small_data = "/Users/june/PycharmProjects/cs242/ScrapeWeb/Crawler/small_data.json"
# graph = Graph(provided_data, True)
graph = Graph(small_data, False)    # only for testing


@app.route("/actors", methods=['GET'])
def get_actors_by_attr():
    """
    GET endpoint
    /actors?attr={attr_value} Example: /actors?name=”Bob”
    :return: json object of actors filtered
    """
    parsed_url = urlparse(request.url)
    attr_list = parse_qs(parsed_url.query)
    actor_dict = graph.query_by_actor_info(attr_list)
    return jsonify(actor_dict)


@app.route("/movies", methods=['GET'])
def get_movies_by_attr():
    """
    GET endpoint
    /movies?attr={attr_value} Example: /movies?
    :return: json object of movies filtered
    :return:
    """
    parsed_url = urlparse(request.url)
    attr_list = parse_qs(parsed_url.query)
    movie_dict = graph.query_by_movie_info(attr_list)
    return jsonify(movie_dict)


@app.route("/actors/<actor_name>", methods=['GET'])
def get_actor_by_name(actor_name):
    """
    GET endpoint
    find the first Actor object that has name <actor_name>
    :param actor_name: given actor_name
    :return: json object of actor node, Nothing with status 400 if not found
    """
    result = graph.query_by_actor_name(actor_name)
    if result:
        return jsonify(result)
    else:
        return Response(status=400)      # BAD REQUEST:  cannot find this actor


@app.route("/movies/<movie_name>", methods=['GET'])
def get_movie_by_name(movie_name):
    """
    GET endpoint
    find the first Movie object that has name <movie_name>
    :param movie_name: given movie_name
    :return: json object of movie node, Nothing with status 400 if not found
    """
    result = graph.query_by_movie_name(movie_name)
    if result:
        return jsonify(result)
    else:
        return Response(status=400)     # BAD REQUEST:  cannot find this actor


@app.route("/actors/<actor_name>", methods=['PUT'])
def put_actor_info(actor_name):
    """
    PUT endpoint
    update standing content for <actor_name> node in backend
    :param actor_name: given actor_name
    :return: status code
    """
    update_dict = json.loads(request.data)
    result = graph.update_actor_info(actor_name, update_dict)
    if result:
        return Response(status=204)
    else:
        return Response(status=400)     # BAD REQUEST:  cannot find this actor


@app.route("/movies/<movie_name>", methods=['PUT'])
def put_movie_info(movie_name):
    """
    PUT endpoint
    update standing content for <movie_name> node in backend
    :param movie_name: given movie_name
    :return: status code
    """
    update_dict = json.loads(request.data)
    result = graph.update_movie_info(movie_name, update_dict)
    if result:
        return Response(status=204)
    else:
        return Response(status=400)     # BAD REQUEST: cannot find this movie


@app.route("/actors", methods=['POST'])
def post_actor_info():
    """
    POST endpoint
    add standing content with dict in request data in backend
    :return: status code
    """
    new_dict = json.loads(request.data)
    result = graph.insert_actor_dict(new_dict)
    if result:
        return Response(status=201)
    else:
        return Response(status=400)     # BAD REQUEST: is not valid actor_info to insert


@app.route("/movies", methods=['POST'])
def post_movies_info():
    """
    POST endpoint
    add standing content with dict in request data in backend
    :return: status code
    """
    new_dict = json.loads(request.data)
    result = graph.insert_movie_dict(new_dict)
    if result:
        return Response(status=201)
    else:
        return Response(status=400)    # BAD REQUEST: is not valid actor_info to insert


@app.route("/actors/<actor_name>", methods=['DELETE'])
def delete_actor_by_name(actor_name):
    """
    DELETE endpoint
    delete standing content for <actor_name> node in backend
    :return: status code
    """
    result = graph.delete_actor_node_by_name(actor_name)
    if result:
        return Response(status=204)
    else:
        return Response(status=400)     # BAD REQUEST: cannot find this actor


@app.route("/movies/<movie_name>", methods=["DELETE"])
def delete_movie_by_name(movie_name):
    """
    DELETE endpoint
    delete standing content for <movie_name> node in backend
    :return: status code
    """
    result = graph.delete_movie_node_by_name(movie_name)
    if result:
        return Response(status=204)
    else:
        return Response(status=400)     # BAD REQUEST: cannot find this actor


if __name__ == '__main__':
    app.run(debug=True)
