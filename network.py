import json
import igraph
import bigjson
import matplotlib.pyplot as plt

fos_list = ["Chemistry", "Biology", "Computer science", "Mathematics", "Physics"]


def get_main_fos(research_paper):
	if "fos" in research_paper.keys():
		paper_fos = research_paper['fos']

		for fos in paper_fos:
			if fos['name'] in fos_list:
				return fos['name']

	return "Other"


with open("dblp.v12_filtered_stripped.json", 'r', encoding='utf-8') as f:
	data = json.load(f)

	g = igraph.Graph(directed=True)

	vertices = []
	edges = []
	main_fos_list = []

	print("Data Loaded")

	for index, paper in enumerate(data):
		id = str(paper['id'])
		vertices.append(id)
		main_fos = get_main_fos(paper)
		main_fos_list.append(main_fos)
		if 'references' in list(paper.keys()):
			for reference in paper['references']:
				ref_string = str(reference)
				vertices.append(ref_string)
				main_fos_list.append("Unknown")
				edges.append((id, ref_string))

g.add_vertices(vertices)
g.vs["fos"] = main_fos_list
g.add_edges(edges)

print(g.is_directed())

degree = g.degree(mode="in")
max_degree = max(degree)
print(max_degree)

max_degree_index = degree.index(max_degree)
print(g.vs[max_degree_index])

pagerank = g.pagerank()
max_pagerank = max(pagerank)
max_pr_index = pagerank.index(max_pagerank)

max_pr_vertex = g.vs[max_pr_index]
print(max_pr_vertex)


def get_fos_graph(fos_name):
	fos_graph = igraph.Graph(directed=True)

	fos_vertices = []
	fos_edges = []

	for x in data:
		if 'fos' in x.keys():
			fos = x['fos']
			fos_names = [x['name'] for x in fos]

			if fos_name in fos_names:
				id = str(x['id'])
				fos_vertices.append(id)
				if 'references' in list(paper.keys()):
					for reference in paper['references']:
						ref_string = str(reference)
						fos_vertices.append(ref_string)
						fos_edges.append((ref_string, id))

	fos_graph.add_vertices(fos_vertices)
	fos_graph.add_edges(fos_edges)

	return fos_graph


data_science_graph = get_fos_graph("Data science")
print(len(data_science_graph.degree()))


# visual_style = {}
# visual_style["bbox"] = (1200, 1200)
# visual_style["vertex_size"] = 7
# igraph.plot(data_science_graph, **visual_style)


def get_reference_edges(seed_id, graph, order):
	new_edges = []

	if order == 0:
		return new_edges

	neighbour_ids = graph.predecessors(seed_id)
	neighbours = []
	for neighbour_id in neighbour_ids:
		neighbours.append(graph.vs[neighbour_id]['name'])

	for neighbour in neighbours:
		new_edges.append([(seed_id, neighbour)])
		new_edges.append(get_reference_edges(neighbour, graph, order - 1))

	flat_edges = [item for sublist in new_edges for item in sublist]
	return flat_edges


def get_reference_graph_seed_id(seed_name, graph, order):
	vertex_names = [v['name'] for v in graph.vs]
	seed_id = vertex_names.index(seed_name)

	reference_graph = igraph.Graph(directed=True)
	new_vertex_ids = graph.neighborhood(seed_id, order=order, mode="in")
	new_vertices = []
	ref_fos_list = []
	for vertex_id in new_vertex_ids:
		new_vertices.append(graph.vs[vertex_id]['name'])
		ref_fos_list.append(graph.vs[vertex_id]['fos'])

	reference_graph.add_vertices(new_vertices)
	reference_graph.vs['fos'] = ref_fos_list

	ref_edges = get_reference_edges(seed_name, graph, order)
	reference_graph.add_edges(ref_edges)

	return reference_graph


seed = str(1967005434)
ref_graph = get_reference_graph_seed_id(seed, g, 2)

# color_list = ["red" for i in range(len(ref_graph.vs))]
color_dict = {
	"Chemistry": "green",
	"Biology": "red",
	"Computer science": "orange",
	"Mathematics": "purple",
	"Other": "yellow",
	"Physics": "cyan",
	"Unknown": "pink"
}
color_list = [color_dict[x["fos"]] for x in ref_graph.vs]
seed_vertex = ref_graph.vs.find(name=seed)
color_list[seed_vertex.index] = "blue"

visual_style = {}
visual_style["vertex_color"] = color_list
visual_style["bbox"] = (1600, 1600)
igraph.plot(ref_graph, **visual_style)

count = 0
for v in g.vs:
	print(v)
	count += 1
	if count > 10:
		break

neighbor_counts = []
for vertex in g.vs:
	n_neighbours = len(g.neighbors(vertex.index))
	neighbor_counts.append((vertex['name'], vertex['fos'], n_neighbours))

# sorted_neighbor_counts = sorted(neighbor_counts, key=lambda tup: tup[2], reverse=True)
# print(sorted_neighbor_counts[:50])

new_seed = None
for x in neighbor_counts:
	if x[1] == "Biology" and x[2] > 100:
		new_seed = x
		break

print(new_seed)

