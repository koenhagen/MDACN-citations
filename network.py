import json
from collections import Counter
import igraph

fos_list = ["Chemistry", "Biology", "Computer science", "Mathematics", "Physics"]


def get_main_fos(research_paper):
    if "fos" in research_paper:
        paper_fos = research_paper['fos']

        for fos in sorted(paper_fos, key=lambda x: x['w'], reverse=True):
            if fos['name'] in fos_list:
                return fos['name']

    return "Other"


with open("dblp.v12_filtered_stripped.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

g = igraph.Graph(directed=True)



print("Data Loaded")

vertices = []
seen_vertices = set()
edges = []
main_fos_list = []
title_list = []

paper_d = {}
for paper in data:
    id = str(paper['id'])
    paper_d[id] = paper
    vertices.append(id)
    seen_vertices.add(id)
    main_fos = get_main_fos(paper)
    main_fos_list.append(main_fos)
    title_list.append(paper['title'])

for paper in data:
    id = str(paper['id'])
    if 'references' in paper:
        for reference in paper['references']:
            ref_string = str(reference)
            if ref_string not in seen_vertices:
                seen_vertices.add(ref_string)
                vertices.append(ref_string)
                main_fos_list.append("Unknown")
                title_list.append(paper['title'])
            edges.append((id, ref_string))

def find_bidirectional_citations(edges):
    edges_set = edges
    return [e for e in edges_set if (e[1], e[0]) in edges_set]

def print_duplicate_papers():
    bidirectional_citation_edges = find_bidirectional_citations(edges)
    print("Papers that reference eachother")
    for edge in bidirectional_citation_edges:
        a = edge[0]
        b = edge[1]
        year_diff = abs(paper_d[a]['year'] - paper_d[b]['year'])
        # if paper_d[a]['n_citation'] > 500 and paper_d[b]['n_citation'] > 500 and year_diff <= 1 and paper_d[a]['year'] > 2010:
        print("Edge ids:", edge)
        print(paper_d[a]['title'], paper_d[a]['n_citation'], paper_d[a]['year'])
        print(paper_d[b]['title'], paper_d[b]['n_citation'], paper_d[b]['year'])
        print("Years between papers published", year_diff)
        print()

print("Fos counter all papers:", Counter(main_fos_list))

g.add_vertices(vertices)
g.vs["fos"] = main_fos_list
g.vs["title"] = title_list
for x in g.vs[:10]:
    print(x)
g.add_edges(edges)

degree = g.degree(mode="in")
max_degree = max(degree)
print("Max degree", max_degree)

max_degree_index = degree.index(max_degree)
print("Max degree node", g.vs[max_degree_index])

pagerank = g.pagerank()
max_pagerank = max(pagerank)
max_pr_index = pagerank.index(max_pagerank)

max_pr_vertex = g.vs[max_pr_index]
print("Max pagerank node", max_pr_vertex)

def get_reference_graph_seed_id(seed_id, graph, order):
    vertex_names = [v['name'] for v in graph.vs]
    seed_index = vertex_names.index(seed_id)

    reference_graph = igraph.Graph(directed=True)
    new_vertex_indices = graph.neighborhood(seed_index, order=order, mode="in")

    new_vertices = [graph.vs[vertex_index]['name'] for vertex_index in new_vertex_indices]
    ref_fos_list = [graph.vs[vertex_index]['fos'] for vertex_index in new_vertex_indices]
    title_list = [graph.vs[vertex_index]['title'] for vertex_index in new_vertex_indices]

    reference_graph.add_vertices(new_vertices)
    reference_graph.vs['fos'] = ref_fos_list
    reference_graph.vs['title'] = title_list

    vertex_set = set(new_vertices)

    ref_edges = [e for e in edges if e[0] in vertex_set and e[1] in vertex_set]

    reference_graph.add_edges(ref_edges)

    return reference_graph


# data_science_graph = get_fos_graph("Data science")
# print(len(data_science_graph.degree()))

color_dict = {
    "Chemistry": "green",
    "Biology": "red",
    "Computer science": "orange",
    "Mathematics": "purple",
    "Other": "yellow",
    "Physics": "cyan",
    "Unknown": "pink"
}



ORDER = 1

for x in range(10):
    seed = g.vs[x]['name']
    ref_graph = get_reference_graph_seed_id(seed, g, ORDER)
    assert ref_graph.vs[0]['name'] == seed

    print("Seed node:", ref_graph.vs[0]['name'], ", FOS:", ref_graph.vs[0]['fos'])
    print(Counter([x['fos'] for x in ref_graph.vs]))
    print()

    color_list = [color_dict[x["fos"]] for x in ref_graph.vs]
    seed_vertex = ref_graph.vs.find(name=seed)
    color_list[seed_vertex.index] = "blue"

    visual_style = {
        "vertex_label": [x['title'] for x in ref_graph.vs],
        "vertex_color": color_list,
        "bbox": (1400, 1400),
        "vertex_size": 20,
        "vertex_label_dist": 1.5,
        "vertex_font": "bold",
        "margin": 300,
        "vertex_label_size": 22
    }
    igraph.plot(ref_graph, **visual_style)
    igraph.plot(ref_graph, **visual_style, target=f"plots/{seed}_order{ORDER}.png")