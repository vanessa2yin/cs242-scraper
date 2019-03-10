from bs4 import BeautifulSoup
import requests
import Actor_crawler
import Film_crawler
import logging
import json


def bfs_crawl(start, fname):
    print("Crawler start...")
    logging.info("Crawler starts. Start url: {0}".format(start))
    required_actor_count = 20
    required_film_count = 40
    actor_queue = [start]
    actor_visited = set()
    real_actor_visited_count = 0
    film_queue = []
    film_visited = set()
    real_film_visited_count = 0
    json_dict = {}

    while real_film_visited_count < required_film_count or real_actor_visited_count < required_actor_count:
        if should_get_next(real_actor_visited_count, required_actor_count, actor_queue):
            actor_url = actor_queue.pop(0)
            scraped_actor_info = get_next_actor(actor_url, actor_visited)
            if is_complete_info(scraped_actor_info):
                # update tracked info
                real_actor_visited_count += 1
                successful_logging_for_fetch_actor(actor_url, real_actor_visited_count)

                # store data as a dict into json_dict
                actor_dict_insert_to_json_dict(json_dict, scraped_actor_info)

                # update film queue
                film_queue = update_film_queue(scraped_actor_info, film_queue)

            else:
                failed_logging_for_fetch_actor(actor_url)

        if should_get_next(real_film_visited_count, required_film_count, film_queue):
            film_url = film_queue.pop(0)
            scraped_film_info = get_next_film(film_url, film_visited)

            if is_complete_info(scraped_film_info):
                real_film_visited_count += 1
                successful_logging_for_fetch_film(film_url, real_film_visited_count)

                # store data as a dict into json_dict
                movie_dict_insert_to_json_dict(json_dict, scraped_film_info)

                # update actor_queue
                update_actor_queue(scraped_film_info, actor_queue)

            else:
                failed_logging_for_fetch_movie(film_url)

    # Store json_dict as json file
    store_into_json_file(json_dict, fname)
    print("Scraped data is written as JSON format into >>>", fname)
    logging.info("Scraped data is written as JSON format into >>> {0}".format(fname))

    # Crawler Done.
    print("Crawler done!")
    logging_crawl_done(real_film_visited_count, real_actor_visited_count, film_visited, actor_visited)


def should_get_next(real_count, required_count, queue):
    return real_count < required_count and len(queue) > 0


# can ONLY be called after should_get_next()
# if next actor_url is not url, return None
def get_next_actor(actor_url, actor_visited):
    if actor_url not in actor_visited and is_url(actor_url):
        actor_visited.add(actor_url)
        soup = get_soup(actor_url)
        return Actor_crawler.get_actor_info(soup)
    return None


# can ONLY be called after should_get_next()
# if next film_url is not url, return None
def get_next_film(film_url, film_visited):
    if film_url not in film_visited and is_url(film_url):
        film_visited.add(film_url)
        soup = get_soup(film_url)
        return Film_crawler.get_movie_info(soup)
    return None


def successful_logging_for_fetch_actor(actor_url, real_actor_visited_count):
    logging.info("Successfully fetch data from actor_url: {0}".format(actor_url))
    logging.info("Actor count = {0}".format(real_actor_visited_count))


def successful_logging_for_fetch_film(film_url, real_film_visited_count):
    logging.info("Successfully fetch data from film_url: {0}".format(film_url))
    logging.info("Movie count = {0}".format(real_film_visited_count))


def failed_logging_for_fetch_actor(actor_url):
    logging.warning("Cannot fetch complete data from actor_url: {0}".format(actor_url))


def failed_logging_for_fetch_movie(movie_url):
    logging.warning("Cannot fetch complete data from movie_url: {0}".format(movie_url))


def actor_dict_insert_to_json_dict(json_dict, scraped_data):
    actor_dict = actor_change_to_dict(scraped_data)
    actor_name = scraped_data[0]
    json_dict[actor_name] = actor_dict


def movie_dict_insert_to_json_dict(json_dict, scraped_data):
    movie_dict = movie_change_to_dict(scraped_data)
    movie_name = scraped_data[0]
    json_dict[movie_name] = movie_dict


# push url into movie_queue, start from the latest movie
def update_film_queue(scraped_data, film_queue):
    movie_url = scraped_data[4]
    movie_url.reverse()
    if len(movie_url) > 10:
        film_queue = film_queue + movie_url[0:10]
    else:
        film_queue = film_queue + movie_url

    return film_queue


def update_actor_queue(scraped_data, actor_queue):
    actor_url = scraped_data[4]
    for actor in actor_url:
        actor_queue.append(actor)


def logging_crawl_done(real_film_visited_count, real_actor_visited_count, film_visited, actor_visited):
    logging.info("Crawler done.")
    logging.info("--------------------------------Report--------------------------------")
    logging.info("Successfully Fetch movie count: {0} Actually visited movie count: {1} "
                 .format(real_film_visited_count, len(film_visited)))
    logging.info("Successfully Fetch actor count: {0} Actually visited actor count: {1} "
                 .format(real_actor_visited_count, len(actor_visited)))
    logging.info("----------------------------------------------------------------------")


def store_into_json_file(json_dict, fname):
    with open(fname, 'w') as outfile:
        array = [json_dict]
        json.dump(array, outfile, indent=2)


def is_complete_info(scraped_info):
    if scraped_info is None:
        return False
    for info in scraped_info:
        if info == 'N/A':
            return False
    return True


def is_url(url):
    try:
        result = requests.get(url)
        return True
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        logging.error("Invalid url: {0}".format(url))
        return False


def get_soup(url):
    content = requests.get(url).text
    return BeautifulSoup(content, 'lxml')


def actor_change_to_dict(scraped_data):
    # actor_name, actor_age, actor_year, movie_name, movie_url
    actor_dict = {"type": "actor",
                  "name": scraped_data[0],
                  "age": scraped_data[1],
                  "year": scraped_data[2],
                  "total_gross": 0,  # will be changed in graph
                  "movies": scraped_data[3]}
    return actor_dict


def movie_change_to_dict(scraped_data):
    # movie_name, movie_year, movie_gross, actor_name, actor_url
    movie_dict = {"type": "movie",
                  "name": scraped_data[0],
                  "year": scraped_data[1],
                  "box_office": scraped_data[2],
                  "actors": scraped_data[3]}
    return movie_dict

