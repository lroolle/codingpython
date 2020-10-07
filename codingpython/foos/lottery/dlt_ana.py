import json
import collections

if __name__ == "__main__":
    with open("dlt_data.json", "r") as fp:
        data = json.loads(fp.read())

    temp = [[], [], [], [], [], [], []]

    for bf in data:
        if bf[0].startswith("2020"):
            for i in range(1, 8):
                temp[i - 1].append(bf[i])

    for x, y in enumerate(temp):
        counter = collections.Counter(y)
        print("---------------------------------------------------------------")
        print(x + 1, counter.most_common())
