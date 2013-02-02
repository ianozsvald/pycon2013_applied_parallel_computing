import json
import random
import networkx as nx
import pylab


MENTION_THRESHOLD = 60  # threshold above which we draw edges
SHOW_NAME_THRESHOLD = 240  # only show usernames if they're mentioned at least this much

FILE = "mapreduceout_wordcount.json"
G = nx.DiGraph()


container = open(FILE)
# Example of the data we're expecting
#container2 = ['[["antocuni", "fijall"], 16]',
#            '[["antocuni", "ian"], 1]',
#            '[["fijall", "antocuni"], 2]',
#            '[["a", "b"], 12]',
#            '[["b", "a"], 42]']

for line in container:
    items = json.loads(line)
    # extract the count of nbr of times user_from mentions user_to
    (user_from, user_to), count = items

    if count > MENTION_THRESHOLD:
        G.add_edge(user_from, user_to, count=count)


if __name__ == "__main__":
    # programs used in graphviz include dot, neato, sfdp
    prog = 'neato'  # 'neato'  # 'sfdp'
    pos = nx.graphviz_layout(G, prog=prog, root=None, args='')
    #pos=nx.spring_layout(G) # positions for all nodes
    #nx.draw_networkx(G, pos, with_labels=True, alpha=0.2, node_size=2)
    #C = nx.connected_component_subgraphs(G)
    C = nx.weakly_connected_component_subgraphs(G)

    for g in C:
        node_sizes = []
        labels = {}
        for node in g.nodes():
            count_total = 0
            for predecessor in g.predecessors(node):
                count = g.get_edge_data(predecessor, node)['count']
                count_total += count
            # take the log of the count_total (so use a minimum of 1)
            #count_total = max(count_total, 1)
            #node_sizes.append(math.log(count_total) * 5)
            node_sizes.append(count_total / 5.0)
            if count_total > SHOW_NAME_THRESHOLD:
                labels[node] = node
            else:
                labels[node] = ""

        c = [random.random()] * nx.number_of_nodes(g)  # random color...
        nx.draw(g,
                pos,
                node_size=node_sizes,
                node_color=c,
                vmin=0.0,
                vmax=1.0,
                labels=labels,
                with_labels=True,
                font_size=15.0,
                )

    #pylab.ylim((-100, 1700.0))
    #pylab.xlim((0, 1800))

    pylab.axis("off")
    pylab.title("Users mentioning users in tweet sample")
    pylab.show()
