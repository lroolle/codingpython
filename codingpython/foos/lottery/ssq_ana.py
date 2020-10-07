import json
import collections

if __name__ == "__main__":
    with open("ssq_data.json", "r") as fp:
        data = json.loads(fp.read())

    temp = [[], [], [], [], [], [], []]
    temp2 = []
    target = "03 09 16 21 27 33 13"

    for bf in data:
        if " ".join(bf[1:]) == target:
            print("Fuxk")
        temp2.append((bf[0], " ".join(bf[1:])))
        if bf[0].startswith("2020"):
            for i in range(1, 8):
                temp[i - 1].append(bf[i])

    print("-" * 66)
    print(temp2[:10])
    print("-" * 66)

    for x, y in enumerate(temp):
        counter = collections.Counter(y)
        print("-" * 66)
        print(x + 1, counter.most_common())
