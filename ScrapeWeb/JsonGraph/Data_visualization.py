import plotly.offline as py
import plotly.graph_objs as go
import numpy as np


def get_location_pair(edge, actor_list, movie_list):
    """
    helper for et_edge_info()
    find the index of actor_node and movie_node of the given edge
    will help find the position of actor_node and movie_node after
    :param edge: (actor_node, movie_node), edge to check, need to find its node's positions
    :param actor_list: list of first 40 nodes of actor_node_list in graph
    :param movie_list: list of first 80 nodes of movie_node_list in graph
    :return: index of actor_node, index of movie_node. will be -1 if not found,.
    """
    actor_index = -1
    movie_index = -1
    for i in range(len(actor_list)):
        if actor_list[i] is edge.v:
            actor_index = i
    for i in range(len(movie_list)):
        if movie_list[i] is edge.u:
            movie_index = i
    return actor_index, movie_index


def get_actor_dot_info(actor_list):
    """
    randomly choose 40 positions and non-randomly choose actor nodes
    :param actor_list: list of first 40 nodes of actor_node_list in graph
    :return: 40 position and actor node info
    """
    actor_x = np.random.randn(40).tolist()
    actor_y = np.random.randn(40).tolist()
    actor_info = []
    for actor in actor_list:
        actor_info.append(actor.change_to_text())
    return actor_x, actor_y, actor_info


def get_movie_dot_info(movie_list):
    """
    randomly choose 80 positions and non-randomly choose movie nodes
    :param movie_list: list of first 80 nodes of movie_node_list in graph
    :return: 80 position and movie node info
    """
    movie_x = np.random.randn(80).tolist()
    movie_y = np.random.randn(80).tolist()
    movie_info = []
    for movie in movie_list:
        movie_info.append(movie.change_to_text())
    return movie_x, movie_y, movie_info


def get_edge_info(actor_list, movie_list, edge_list, actor_loc, movie_loc):
    """

    :param actor_list: list of first 40 nodes of actor_node_list in graph
    :param movie_list: list of first 80 nodes of movie_node_list in graph
    :param edge_list: complete edge_list in graph
    :param actor_loc: randomly generated actor location get from get_actor_dot_info()
    :param movie_loc: randomly generated movie location get from get_movie_dot_info()
    :return: edge location info pair
    """
    edge_x_pair = []
    edge_y_pair = []
    for edge in edge_list:
        (actor_index, movie_index) = get_location_pair(edge, actor_list, movie_list)
        # cannot find actor_node or movie_node of this edge in the chosen actor_list or movie_list
        if actor_index == -1 or movie_index == -1:
            continue
        edge_x_pair += tuple([actor_loc[0][actor_index], movie_loc[0][movie_index], None])
        edge_y_pair += tuple([actor_loc[1][actor_index], movie_loc[1][movie_index], None])
    return edge_x_pair, edge_y_pair


def get_node_trace(actor_list, movie_list):
    """
    get scatter plot info for 40 actor_node and 80 movie_node
    :param actor_list: list of first 40 nodes of actor_node_list in graph
    :param movie_list: list of first 80 nodes of movie_node_list in graph
    :return: scatter plot info and location info
    """
    actor_x, actor_y, actor_info = get_actor_dot_info(actor_list)
    movie_x, movie_y, movie_info = get_movie_dot_info(movie_list)
    actor_trace = go.Scatter(
        x=actor_x,
        y=actor_y,
        text=actor_info,
        mode='markers',
        name="actors",
        hoverinfo='text',
        marker=dict(color=(['#39CAF6'] * 40))
    )
    movie_trace = go.Scatter(
        x=movie_x,
        y=movie_y,
        text=movie_info,
        mode='markers',
        name='movies',
        hoverinfo='text',
        marker=dict(color=(['#F6BD39'] * 80))
    )
    return actor_trace, movie_trace, (actor_x, actor_y), (movie_x, movie_y)


def get_edge_trace(actor_list, movie_list, edge_list, actor_loc, movie_loc):
    """
    get scatter plot info for edge
    :param actor_list: list of first 40 nodes of actor_node_list in graph
    :param movie_list: list of first 80 nodes of movie_node_list in graph
    :param edge_list: complete edge_list in graph
    :param actor_loc: actor_node locations
    :param movie_loc: movie_node locations
    :return: scatter plot info for edge
    """
    edge_x_pair, edge_y_pair = get_edge_info(actor_list, movie_list, edge_list, actor_loc, movie_loc)
    edge_trace = go.Scatter(
        x=edge_x_pair,
        y=edge_y_pair,
        name='connections',
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    return edge_trace


def visualize(graph):
    """
    draw nodes and edges and show it in visualize.html
    :param graph: given data
    """
    actor_list = graph.actor_node_list[0:40]
    movie_list = graph.movie_node_list[0:80]
    edge_list = graph.edge_list

    actor_trace, movie_trace, actor_loc, movie_loc = get_node_trace(actor_list, movie_list)
    edge_trace = get_edge_trace(actor_list, movie_list, edge_list, actor_loc, movie_loc)

    fig = go.Figure(data=[edge_trace, actor_trace, movie_trace],
                    layout=go.Layout(
                        title='<br>Network graph made with Python',
                        titlefont=dict(size=16),
                        hovermode='closest',
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    py.plot(fig, filename='visualize.html')
