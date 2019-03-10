import numpy as np
import matplotlib.pyplot as plt


def analyze_actor_connections(data):
    """
    analyze the connections of actors and plot top n hub actors
    will get a bar char
    :param data: a list of (hub actor's name, connection number), contain only top n actors
    """
    data = np.array(data)
    name_list = np.array(data[:, 0])
    y_pos = np.arange(len(name_list))
    connections = np.array(data[:, 1], dtype=np.int32)

    plt.figure(figsize=(10, 3))
    plt.bar(y_pos, connections, align='center', width=0.3)
    plt.xticks(y_pos, name_list)
    plt.xlabel('actors')
    plt.ylabel('connections')
    plt.title('Top hub actors Analysis')

    plt.show()


def analyze_age_grossing_of_individuals(data):
    """
    analyze the grossing and value of individual actor
    will get a scatter plot
    :param data: a list of (name, total_gross, age) sorted by grossing value, contain all actors
    """
    data_list = np.array(data)
    grossing_list = np.array(data_list[:, 1], dtype=np.int32)
    age_list = np.array(data_list[:, 2], dtype=np.int32)

    plt.scatter(age_list, grossing_list)
    plt.xlim([0, 100])
    plt.ylim([100000000, 600000000])
    plt.xticks(np.arange(0, 100, 5))
    plt.yticks(np.arange(100000000, 600000000, 50000000))
    plt.xlabel('age')
    plt.ylabel('grossing value')
    plt.title('Actor age VS actor grossing value Analysis')
    plt.show()


def analyze_average_grossing_of_age_group(data):
    """
    analyze the grossing and value of actors in each age group
    will get a bar char
    :param data: a list of (name, total_gross, age) sorted by grossing value, contain all actors
    :return: average_gross_dict, (age_range: average_gross)
    """
    data_list = np.array(data)
    age_group_dict = get_age_group_dict(data_list)
    average_gross_dict = get_average_gross_for_age_group(age_group_dict)

    plt.bar(range(len(average_gross_dict)), list(average_gross_dict.values()), align='center')
    plt.xticks(range(len(average_gross_dict)), list(average_gross_dict.keys()))
    plt.xlabel('age range')
    plt.ylabel('average actor gross')
    plt.title('Actor age VS actor average gross Analysis')
    plt.show()

    return average_gross_dict


def get_age_group_dict(data_list):
    """
    put actor total gross sum and age info into different age group
    age_group_dict has age range as key: (age range start, age range end)
                   has info pair as value: (actor_total_gross_sum, actor_count)
    :param data_list: np data, storing (actor_name, actor_total_gross, actor_age)
    :return: age_group_dict
    """
    # preset these age range as the only valid ones
    age_group_dict = {(20, 29): (0, 0), (30, 39): (0, 0), (40, 49): (0, 0),
                      (50, 59): (0, 0), (60, 69): (0, 0), (70, 79): (0, 0),
                      (80, 89): (0, 0), (90, 99): (0, 0)}
    for data in data_list:
        actor_gross = max(int(data[1]), 0)
        actor_age = int(data[2])
        age_group = round_to_group(actor_age)
        if age_group:
            new_gross_sum = age_group_dict[age_group][0] + actor_gross
            new_count = age_group_dict[age_group][1] + 1
            age_group_dict[age_group] = (new_gross_sum, new_count)
    return age_group_dict


def round_to_group(n):
    """
    helper for categorize_gross_into_age_group()
    round n to (n-n%10, n-n%10+9)
    :param n: number to round
    :return: age range for n
    """
    rem = n % 10
    group_start = n - rem
    group_end = group_start + 9
    if group_start < 20 or group_start > 90:
        return False
    else:
        return group_start, group_end


def get_average_gross_for_age_group(age_group_dict):
    """
    calculate total_gross_sum/actor_count for each age group
    :param age_group_dict: given age_group_dict from get_age_group_dict()
    :return: average_gross_dict
    """
    result_dict = {}
    for key, value in age_group_dict.items():
        total_gross_sum = value[0]
        actor_count = value[1]
        if actor_count == 0:
            result_dict[key] = 0
        else:
            result_dict[key] = total_gross_sum/actor_count
    return result_dict


def find_highest_average_gross(average_gross_dict):
    """
    find highest average gross in average_gross_dict and return (key,value)
    :param average_gross_dict: given average_gross_dict
    :return: (age range, average gross)
    """
    max_average_gross = 0
    for key, value in average_gross_dict.items():
        if value > max_average_gross:
            result = (key, value)
            max_average_gross = value
    return result
