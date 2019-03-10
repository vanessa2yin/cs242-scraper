from JsonGraph import Data_analysis, Data_visualization
from JsonGraph.Actor_node import ActorNode
from JsonGraph.Graph import Graph


def main():
    scraped_data = ".././Crawler/data copy.json"
    my_graph = Graph(scraped_data, False)
    # output_fname = "output.json"
    # graph.save_to_json(output_fname)

    # for data analysis and API
    provided_data = "../Resource/provided_data.json"
    graph_with_provided_data = Graph(provided_data, True)

    # data analysis 1
    # Find the top hub actors
    analysis1 = graph_with_provided_data.get_hub_actors_rank(5)
    print_analysis(analysis1, 1)
    Data_analysis.analyze_actor_connections(analysis1)

    # data analysis 2
    # Find actors with highest grossing values and see the relationship between grossing value and age
    analysis2 = graph_with_provided_data.get_highest_gross_rank()
    print_analysis(analysis2, 2)
    Data_analysis.analyze_age_grossing_of_individuals(analysis2)
    average_gross_dict = Data_analysis.analyze_average_grossing_of_age_group(analysis2)
    highest_age_group_result = Data_analysis.find_highest_average_gross(average_gross_dict)
    print("age group with highest average gross: ", highest_age_group_result)

    # Data visualization
    Data_visualization.visualize(my_graph)


def print_result(result, n):
    print("-----result{0}-----".format(n))
    print(result)
    print()


def print_analysis(analysis, n):
    print("----analysis{0}----".format(n))
    print(analysis)
    print()


if __name__ == "__main__":
    main()
