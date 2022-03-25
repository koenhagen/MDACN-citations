import json

def get_head():
    N = 100
    file_object = open("D:/citation -KOEN/citation_data/dblp.v12_head.json", 'a', encoding="utf-8")
    with open("D:/citation -KOEN/citation_data/dblp.v12.json", encoding='utf-8') as f:

        for i in range(1, N):
            print(f.readline())
            file_object.write(f.readline())
    file_object.close()


if __name__ == '__main__':
    get_head()

