import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def calculate_total_resources(start_dates, durations, resource_requirements):
    total_resources = {activity: resource_requirements[activity] + start_dates[activity] for activity in start_dates}
    return max(total_resources.values())

def burgess_algorithm(activities, durations, prerequisites, resource_requirements):
    #create a graph
    G = nx.DiGraph()

    #Add nodes to our graph
    for activity in activities:
        G.add_node(activity, duration=durations[activity])

    #Add edges that shows prerequisites
    for activity, prereq_list in prerequisites.items():
        for prereq in prereq_list:
            G.add_edge(prereq, activity)

    #Draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.show()

    #Initial start dates
    start_dates = {activity: 0 for activity in activities}

    while True:
        for node in nx.topological_sort(G):
                #Calculate Earliest Start (ES)
            earliest_start = max([start_dates[predecessor] + durations[predecessor] for predecessor in G.predecessors(node)], default=0)
            start_dates[node] = max(start_dates[node], earliest_start)

        new_total_resources = calculate_total_resources(start_dates, durations, resource_requirements)

        if new_total_resources >= calculate_total_resources({activity: start_dates[activity] for activity in start_dates}, durations, resource_requirements):
            break

    # Calculate Latest Start (LS)
    ls_dates = {activity: start_dates[activity] for activity in start_dates}
    for node in nx.topological_sort(G):
        ls_dates[node] = min([ls_dates[successor] - durations[node] for successor in G.successors(node)], default=start_dates[node])

    return new_total_resources, start_dates, ls_dates

# Example inputs
activities = ["A", "B", "C", "D", "E", "F", "G"]
durations = {"A": 1, "B": 4, "C": 2, "D": 3, "E": 3, "F": 2, "G": 3}
prerequisites = {"C": ["A"], "D": ["A"], "E": ["B", "C"], "F": ["D"], "G": ["E", "F"]}
resource_requirements = {"A": 1, "B": 2, "C": 3, "D": 2, "E": 1, "F": 4, "G": 4}

min_total_resources, start_dates, ls_dates = burgess_algorithm(activities, durations, prerequisites, resource_requirements)

print("Minimum Total Resources:", min_total_resources)
print("Start Dates (ES):", start_dates)
print("Latest Start Dates (LS):", ls_dates)
