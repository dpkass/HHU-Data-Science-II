from networkx import DiGraph
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


get_google = lambda: read_graph(google_file)
get_wiki = lambda: read_graph(wiki_file)
