import re
import igraph as ig

sample_input = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

sample_result = (7, "co,de,ka,ta")

def solve(input_string):
    computers = re.findall(r"[a-z]+", input_string)
    vertices = list(set(computers))
    edges = [(v, w) for v, w in zip(computers[::2], computers[1::2])]
    graph = ig.Graph()
    graph.add_vertices(vertices)
    graph.add_edges(edges)
    lan_t_cliques = compute_lan_t_cliques(graph)
    lan_password = compute_lan_password(graph)
    return (lan_t_cliques, lan_password)

def compute_lan_t_cliques(graph):
    t_cliques = []
    cliques = graph.cliques(3, 3)
    for clique in cliques:
        for vertex in clique:
            if graph.vs[vertex]["name"].startswith("t"):
                t_cliques.append(clique)
                break
    return len(t_cliques)

def compute_lan_password(graph):
    largest_clique = graph.largest_cliques()[0]
    password = ",".join(sorted(graph.vs[v]["name"] for v in largest_clique))
    return password
