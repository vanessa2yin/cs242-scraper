from bs4 import BeautifulSoup
import bs4
import requests
import logging
import datefinder
import re


def is_filmography_list_section(current_section):
    return current_section.name == 'table' or current_section.name == 'ul'


def is_filmography_url_section(current_section):
    return current_section.has_attr('class') and current_section['class'] == ['hatnote', 'navigation-not-searchable']


def is_filmography_section(current_section, search_again):
    if not isinstance(current_section, bs4.element.Tag):
        return False
    if not search_again:
        return is_filmography_list_section(current_section)
    return is_filmography_url_section(current_section)


def get_section_before_movie_list(soup, section_name):
    search_again = False
    section_before_movie_list = soup.find(
        lambda tag: tag.name == 'span' and tag.has_attr('id') and tag['id'] == section_name)
    if section_before_movie_list is None:
        section_before_movie_list = soup.find(
            lambda tag: tag.name == 'span' and tag.has_attr('id') and tag['id'] == 'Filmography_and_awards')
        search_again = True
    return section_before_movie_list, search_again


def get_detail_info(movie_section):
    if not isinstance(movie_section, bs4.element.Tag):
        logging.warning('Incorrect Movie Section Type. Expected: bs4.element.Tag. Actual: {0}'.format(movie_section))
        return "N/A", "N/A"

    movie_name = []
    movie_url = []
    for movie_info in movie_section.find_all('a'):
        if movie_info.has_attr('href') and movie_info.has_attr('title'):
            movie_url.append("https://en.wikipedia.org" + movie_info['href'])
            movie_name.append(movie_info['title'])
    return movie_name, movie_url


def get_actor_movies_helper(soup, section_name):
    section_before_movie_list, search_again = get_section_before_movie_list(soup, section_name)
    if section_before_movie_list is None:
        return "N/A", "N/A", False

    section_before_movie_list = section_before_movie_list.parent
    while True:
        if is_filmography_section(section_before_movie_list, search_again):
            break
        section_before_movie_list = section_before_movie_list.next_element

    movie_section = section_before_movie_list
    movie_name, movie_url = get_detail_info(movie_section)

    return movie_name, movie_url, search_again


def get_actor_movies(soup):
    movie_name, movie_url, search_again = get_actor_movies_helper(soup, "Filmography")
    if search_again:
        new_page = requests.get(movie_url[0]).content
        new_soup = BeautifulSoup(new_page, 'lxml')
        movie_name, movie_url, _ = get_actor_movies_helper(new_soup, "Film")
    return movie_name, movie_url


# get (name, age, year) of the actor from infobox
def get_actor_name_age_year(soup):
    infobox = soup.find('table', {'class': "infobox biography vcard"})
    if infobox is None:
        return "N/A", "N/A", "N/A"

    actor_infobox = infobox.tbody.findAll('tr')
    actor_name = "N/A"
    actor_age = "N/A"
    actor_year = "N/A"
    for line in actor_infobox:
        if line.th and line.th.div and line.th.div.has_attr('class') and line.th.div['class'][0] == "fn":
            # get actor_name
            actor_name = line.th.div.text
        if line.th and line.th.string == "Born":
            text = line.text
            # get actor_year
            matches = list(datefinder.find_dates(text))
            if len(matches) > 0:
                actor_year = matches[0].year

            # get actor_age
            age_substr = text[text.find("age"): -1]
            actor_age = re.search(r'\d+', age_substr)
            if actor_age:
                actor_age = int(actor_age.group())
        if line.th and line.th.string == "Died":
            text = line.text

            # get actor_age if died
            age_substr = text[text.find("age"): -1]
            actor_age = int(re.search(r'\d+', age_substr).group())
    return actor_name, actor_age, actor_year


# get (name, age, year, movie_name, movie_url) of the actor
def get_actor_info(soup):
    # logging.info("Enter get_actor_info() with", soup)
    actor_name, actor_age, actor_year = get_actor_name_age_year(soup)
    movie_name, movie_url = get_actor_movies(soup)
    return actor_name, actor_age, actor_year, movie_name, movie_url
