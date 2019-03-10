import datefinder
import re


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def change_money_to_integer(money):
    money = money.lower()
    end = money.find("[")
    if end != -1:
        money = money[0:end]
    money = money.replace("$", "").replace(",", "")
    result = int(re.search(r'\d+', money).group(0))

    multiple = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
    possibles = ["thousand", "million", "billion"]
    end_position = -1
    scale_found = ""

    for magnitude in possibles:
        tmp = money.find(magnitude)
        if tmp != -1:
            end_position = tmp
            scale_found = magnitude
    if end_position != -1 and isfloat(money[0:end_position]):
        result = result * multiple[scale_found]
        return int(result)
    else:
        return "N/A"


def get_movie_name(soup):
    movie_name_section = soup.find('h1', {'class': "firstHeading"})
    if movie_name_section is not None:
        return movie_name_section.text
    return "N/A"


def get_movie_info(soup):
    find_result = soup.find('table', {'class': "infobox vevent"})
    if find_result is None:
        return "N/A", "N/A", "N/A", "N/A", "N/A"
    movie_infobox = find_result.tbody.findAll('tr')
    movie_name = get_movie_name(soup)
    movie_year = "N/A"
    movie_gross = "N/A"
    actor_url = []
    actor_name = []
    for line in movie_infobox:
        # get movie_year
        if line.th and line.th.div and line.th.div.text == 'Release date':
            text = line.th.next_sibling.text
            matches = list(datefinder.find_dates(text))
            if len(matches) > 0:
                movie_year = matches[0].year
        # get movie_gross
        if line.th and line.th.text == 'Box office':
            gross_money = line.th.next_sibling.text
            movie_gross = change_money_to_integer(gross_money)

        # get movie_starring
        if line.th and line.th.text == 'Starring':
            for star_row in line.th.next_sibling.find_all('a'):
                if star_row.has_attr('href') and star_row.has_attr('title'):
                    actor_url.append("https://wikipedia.org" + star_row['href'])
                    actor_name.append(star_row['title'])
    if actor_url is [] or actor_name is []:
        if actor_url is []:
            actor_url = "N/A"
        if actor_name is []:
            actor_name = "N/A"
    return movie_name, movie_year, movie_gross, actor_name, actor_url
