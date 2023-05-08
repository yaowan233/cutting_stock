from pandas import read_csv
from item import Item

L = 2440
W = 1220


def read_file(filename: str, a1, a2) -> list[Item]:
    data = read_csv(filename)
    temp = {}
    for i in data.iterrows():
        length = i[1]["item_length"]
        width = i[1]["item_width"]
        # ensure length >= width always true
        if width > length:
            (length, width) = (width, length)
        if (length, width) not in temp.keys():
            temp[(length, width)] = Item(i[0], length, width, i[1]["item_num"])
        else:
            temp[(length, width)].demand += i[1]["item_num"]
    items = list(temp.values())
    del temp
    for item in items:
        if item.length >= 0.5 * L and item.width >= 0.5 * W:
            item.value = a1 * item.length * item.width
        elif item.length >= 0.5 * L or item.width >= 0.5 * W:
            item.value = a2 * item.length * item.width
        else:
            item.value = item.length * item.width
    return items


# test
if __name__ == "__main__":
    items = read_file("dataA/dataA5.csv", 10, 5)
    print(sum([item.area for item in items]))
