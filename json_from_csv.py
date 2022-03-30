import json
import csv

import bigjson


def json_from_csv():
	file_object = open("dblp.v12_filtered.json", 'w', encoding='utf-8')
	with open("dblp.v12.json", 'r', encoding='utf-8') as f:
		for line in f:
			if line == '[\n' or line == ']\n':
				continue
			if line[0] == ',':
				line = line[1:]
			data = json.loads(line)
			if int(data['n_citation']) < 100:
				continue
			else:
				print(f'paper added: {data["title"]} with {data["n_citation"]} citations')
				file_object.write(json.dumps(data, ensure_ascii=False))
				file_object.write(',\n')
	file_object.close()


def simple_json_from_csv():
	with open("dblp.v12_filtered.json", 'rb') as f:
		data = bigjson.load(f)

		filtered_data = []

		for x in data:
			if x['n_citation'] >= 100:
				filtered_data.append(x)
				print(f'Paper added: {x["title"]} with {x["n_citation"]} citations')

	with open("dblp.v12_filtered_new.json", 'w') as outputfile:
		json.dump(filtered_data, outputfile)


if __name__ == '__main__':
	simple_json_from_csv()
