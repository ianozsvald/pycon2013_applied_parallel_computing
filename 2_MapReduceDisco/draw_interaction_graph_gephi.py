import json
"""Export graph of interactions for Gephi (with some filtering)"""
import networkx as nx

#MENTION_THRESHOLD = 100  # threshold above which we draw edges
MENTION_THRESHOLD = 70  # threshold above which we draw edges

FILE = "mapreduceout_wordcount.json"
G = nx.DiGraph()

container = open(FILE)

for line in container:
    items = json.loads(line)
    # extract the count of nbr of times user_from mentions user_to
    (user_from, user_to), count = items

    if count > MENTION_THRESHOLD:
        G.add_edge(user_from, user_to, count=count)

nx.write_graphml(G, "draw_interaction_graph_gephi.graphml")
