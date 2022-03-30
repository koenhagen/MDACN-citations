import json
import igraph
import bigjson
import matplotlib.pyplot as plt

with open("dblp.v12_filtered_stripped.json", 'r', encoding='utf-8') as f:
	data = json.load(f)

	g = igraph.Graph(directed=True)

	vertices = []
	edges = []

	print("Data Loaded")

	for index, paper in enumerate(data):
		id = str(paper['id'])
		vertices.append(id)
		if 'references' in list(paper.keys()):
			for reference in paper['references']:
				ref_string = str(reference)
				vertices.append(ref_string)
				edges.append((id, ref_string))

g.add_vertices(vertices)
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
	for neighbour_id

	for neighbour in neighbours:
		new_edges.append([(seed_id, neighbour)])
		new_edges.append(get_reference_edges(neighbour, graph, order - 1))

	flat_edges = [item for sublist in new_edges for item in sublist]
	# print(flat_edges)
	return flat_edges


def get_reference_graph_seed_id(seed_id, graph, order):
	reference_graph = igraph.Graph(directed=True)
	new_vertex_ids = graph.neighborhood(seed_id, order=order)
	new_vertices = []
	for vertex_id in new_vertex_ids:
		new_vertices.append(graph.vs[vertex_id]['name'])

	print(new_vertices)
	reference_graph.add_vertices(new_vertices)

	# for vertex in reference_graph.vs:
	# 	print(vertex)

	ref_edges = get_reference_edges(seed_id, graph, order)
	reference_graph.add_edges(ref_edges)

	return reference_graph


ref_graph = get_reference_graph_seed_id(1, g, 1)
igraph.plot(ref_graph)
