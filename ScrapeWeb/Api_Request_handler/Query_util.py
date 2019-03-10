# helper for is_valid_actor_for_query()
def is_valid_actor_name(attr_value, actor_node):
    # support OR logic
    for name in attr_value:
        if name in actor_node.name:
            return True
    return False


# helper for is_valid_actor_for_query()
def is_valid_age(attr_value, actor_node):
    # support OR logic
    for age in attr_value:
        if int(age) == actor_node.age:
            return True
    return False


# helper for is_valid_actor_for_query()
def is_valid_movie_of_actor(attr_value, actor_node):
    # support OR logic
    for movie in attr_value:
        if movie in actor_node.movies:
            return True
    return False


def is_valid_actor_for_query(actor_node, attr_list):
    """
    check if the actor_node should be filtered out according to attr_list
    :param actor_node: actor_node to check
    :param attr_list: attr_list from url request
    :return:
    """
    for attr, attr_value in attr_list.items():
        if attr == 'name' and not is_valid_actor_name(attr_value, actor_node):
            return False
        if attr == 'age' and not is_valid_age(attr_value, actor_node):
            return False
        if attr == 'total_gross' and actor_node.total_gross < int(attr_value[0]):  # total_gross does not support OR
            return False
        if attr == 'movies' and not is_valid_movie_of_actor(attr_value, actor_node):
            return False
    return True


# helper for is_valid_movie_for_query()
def is_valid_movie_name(attr_value, movie_node):
    # support OR logic
    for name in attr_value:
        if name in movie_node.name:
            return True
    return False


# helper for is_valid_movie_for_query()
def is_valid_year(attr_value, movie_node):
    # support OR logic
    for year in attr_value:
        if int(year) == movie_node.year:
            return True
    return False


# helper for is_valid_movie_for_query()
def is_valid_actor_of_movie(attr_value, movie_node):
    # support OR logic
    for actor in attr_value:
        if actor in movie_node.actors:
            return True
    return False


def is_valid_movie_for_query(movie_node, attr_list):
    """
    check if the movie_node should be filtered out according to attr_list
    :param movie_node: movie_node to check
    :param attr_list: attr_list from url request
    :return:
    """
    for attr, attr_value in attr_list.items():
        if attr == 'name' and not is_valid_movie_name(attr_value, movie_node):
            return False
        if attr == 'box_office' and movie_node.box_office < int(attr_value[0]):
            return False
        if attr == 'year' and not is_valid_year(attr_value, movie_node):
            return False
        if attr == 'actors' and not is_valid_actor_of_movie(attr_value, movie_node):
            return False
    return True
