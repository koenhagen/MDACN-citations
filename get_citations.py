import json
import csv


def get_citations():
    citation_list = []
    with open("D:/citation -KOEN/citation_data/dblp.v12.json", "r", encoding='utf-8') as f:
        for line in f:
            if line == '[\n' or line == ']\n':
                continue
            if line[0] == ',':
                line = line[1:]
            data = json.loads(line)
            citation_list.append((data['id'], data['n_citation']))
    print(citation_list)
    sorted_citation_list = sorted(citation_list, key=lambda tup: tup[1], reverse=True)
    print(sorted_citation_list)

    with open('citations.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['paper_id', 'n_citations'])
        for row in sorted_citation_list:
            csv_out.writerow(row)


if __name__ == '__main__':
    get_citations()
