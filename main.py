import copy
from functools import lru_cache
from pandas import read_csv
import sys
from PIL import Image, ImageDraw

sys.setrecursionlimit(3000)


class Item:
    def __init__(self, id, length: float, width: float, demand: int):
        self.id = id
        self.length = int(length)
        self.width = int(width)
        self.demand = demand
        self.value = None  # to be determined later
        self.place = []

    def __hash__(self):
        return self.id * 100 + self.demand

    # for Item printing
    def __repr__(self) -> str:
        return f"\nid: {self.id}, length: {self.length}, width: {self.width}, demand: {self.demand}"

    # for sorting
    def __lt__(self, other):
        return (
            self.length < other.length
            if self.length != other.length
            else self.width < other.width
        )


L = 2440
W = 1220
data = read_csv("dataA/dataA1.csv")
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
        item.value = 4 * item.length * item.width
    elif item.length >= 0.5 * L or item.width >= 0.5 * W:
        item.value = 1.2 * item.length * item.width
    else:
        item.value = item.length * item.width


@lru_cache(2**16)
def get_f(x: int, y: int, items: tuple[Item], res) -> tuple[float, tuple[Item]]:
    ls = [item.width for item in items if item.demand > 0]
    miny = min(ls) if ls else 10000000000000000
    if y < miny:
        return 0, items
    # if y % 250 == 1 and y > 200:
    #     print(res, y)
    items = list(items)
    items = copy.deepcopy(items)
    value_ls = [0]
    for item in items:
        if y >= item.width and x >= item.length and item.demand > 0:
            e_i = min(x // item.length, item.demand)
            item.demand -= e_i
            item.place.append((x - item.length, W - y, e_i))
            ans, items = get_f(x, y - item.width, tuple(items), res)
            ans += e_i * item.value
            if ans > 0:
                value_ls.append(ans)
        elif y >= item.width and x >= item.length:
            break
    res = max(value_ls)
    return res, tuple(items)


@lru_cache(2**16)
def generate_pattern(items: tuple[Item], res, x) -> tuple[float, tuple[Item]]:
    ls = [item.length for item in items if item.demand > 0]
    minx = min(ls) if ls else 10000000000000
    if x < minx:
        return res, items
    l_set = set()
    l_set.add(x)
    for item in items:
        count = 1
        while count * item.length < L and count <= item.demand:
            l_set.add(count * item.length)
            count += 1
    l_set = sorted(l_set)
    ans = []
    for l in l_set:
        res1, items1 = get_f(l, W, items, res)
        res2, items2 = generate_pattern(items1, 0, x - l)
        res1 += res2
        if res1 > 0:
            ans.append((res1, tuple(items2)))
    return max(ans, key=lambda x: x[0]) if ans else (0, tuple())


items = items[:5]
items.sort()

ans = generate_pattern(tuple(items), 0, L)
print(ans)
# print(use / (W * L))
print(get_f(W, L, tuple(items), 0))
for i in ans[1]:
    print(i.place)

img = Image.new("RGB", (2440, 1220))
draw = ImageDraw.Draw(img)
for item in ans[1]:
    for i in item.place:
        draw.rectangle((i[0], i[1], i[0] + item.length, i[1] + item.width))
img.show()
