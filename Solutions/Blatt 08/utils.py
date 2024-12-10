import networkx as nx
from networkx import DiGraph
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm

google_file = './data/web-Google.txt'
wiki_file = './data/wiki-topcats.txt'


def read_graph(file):
    with open(file) as f: lines = f.readlines()
    lines = tqdm(lines, desc='Reading graph from file')
    lines = filter(lambda line: not line.startswith('#') and line, lines)
    lines = map(str.split, lines)
    lines = map(lambda l: tuple(map(int, l)), lines)
    return DiGraph(lines)


def get_neighbors(G, nodes):
    return set.union(*(set(G[n]) for n in nodes))


def neighbors(G, node, depth=2):
    neighbors = {node}
    for _ in range(depth): neighbors |= get_neighbors(G, neighbors)
    return G.subgraph(neighbors)


def top_nodes(rank_dict, count=5, as_dict=True):
    top = sorted(rank_dict.keys(), key=rank_dict.get, reverse=True)[:count]
    return {k: rank_dict[k] for k in top} if as_dict else top


def plot_bar(V, ranking1, ranking2):
    msr_values = [ranking1[v] for v in V]
    pr_values = [ranking2[v] for v in V]

    x = range(len(V))
    width = 0.35

    fig, ax1 = plt.subplots(figsize=(12, 6))

    bars1 = ax1.bar(x, msr_values, width, label='My PageRank', color='blue')
    ax1.set_ylabel('PageRank Score')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    bars2 = ax2.bar([i + width for i in x], pr_values, width, label='True PageRank', color='orange')
    ax2.set_ylabel('PageRank Score')
    ax2.tick_params(axis='y')

    ax1.set_xticks([i + width / 2 for i in x])
    ax1.set_xticklabels(V, rotation=45, ha='right')
    ax1.set_xlabel('Nodes')

    fig.legend([bars1, bars2], ['My PageRank', 'True PageRank'])

    plt.title('Comparison of PageRank Implementations (Separate Scales)')
    plt.tight_layout()
    plt.show()


def plot_scatter(V, ranking1, ranking2):
    msr_values = [ranking1[v] for v in V]
    pr_values = [ranking2[v] for v in V]

    xmin, xmax = min(msr_values), max(msr_values)
    ymin, ymax = min(pr_values), max(pr_values)

    plt.figure(figsize=(8, 6))
    plt.scatter(msr_values, pr_values)
    plt.xlabel('My PageRank')
    plt.ylabel('True PageRank')
    plt.title('Correlation between Rankings')
    plt.plot([xmin, xmax], [ymin, ymax], 'r--')
    plt.show()


def plot(V, ranking1, ranking2):
    plot_bar(sorted(V), ranking1, ranking2)
    plot_scatter(sorted(ranking1.keys()), ranking1, ranking2)


get_google = lambda: read_graph(google_file)
get_wiki = lambda: read_graph(wiki_file)
