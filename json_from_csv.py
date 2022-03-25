import json
import csv


def json_from_csv():
    file_object = open("D:/citation -KOEN/citation_data/dblp.v12_filtered.json", 'w', encoding='utf-8')
    with open("D:/citation -KOEN/citation_data/dblp.v12.json", 'r', encoding='utf-8') as f:
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

            # with open("C:/Users/koenh/PycharmProjects/MDACN-citations/citations.csv", 'r', encoding='utf-8') as csv_file:
            #     reader = csv.DictReader(csv_file)
                # for row in reader:

                #     print(row)
                #     print(data)
                #     if row['paper_id'] == data['id']:
                #         print(data)
                #         file_object.write(data)
                #         break
    file_object.close()


if __name__ == '__main__':
    json_from_csv()

