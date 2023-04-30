import copy
import random
from functools import lru_cache
from random import shuffle

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
        return f"\nid: {self.id}, length: {self.length}, width: {self.width}, demand: {self.demand}, pos: {self.place}"

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
def get_f(x: int, y: int, old_items: tuple[Item], res, x_pos) -> tuple[float, tuple[Item]]:
    ls = [item.width for item in old_items if item.demand > 0 and item.length <= x and item.width <= y]  # 筛选出待切割目标物件的宽度
    if not ls:
        return res, old_items  # 如果没有需要切割的物件的话 直接返回值
    miny = min(ls)
    value_ls = [(res, old_items)]
    items = list(old_items)
    items = copy.deepcopy(items)
    items.sort(key=lambda x1: x1.width)
    for index, item in enumerate(items):
        if item.width < miny:
            continue
        if y >= item.width and x >= item.length and item.demand > 0:  # 如果物品能够在长x宽y的板子上被切割的话
            item = copy.deepcopy(item)
            new_items = copy.deepcopy(items)
            e_i = min(x // item.length, item.demand)  # 在一行中物品能切割的最多数量
            item.demand -= e_i  # 减少需求量
            item.place.append((L - x_pos, W - y, e_i))  # 增加物品坐标与切割数量
            new_items[index] = item
            f, ans_items = get_f(x, y - item.width, tuple(new_items), res, x_pos)  # 在(x, y - item.width)的板子上递归的求解
            f += e_i * item.value  # 得到总体的value
            if f > 0:  # 防止0值append加快速度
                value_ls.append((f, ans_items))
        elif y < item.width and item.demand != 0:  # 剪枝，提前跳出循环
            break
    # 挑选出最能切割出最多 value 的切割方式
    res = max(value_ls, key=lambda v: v[0])
    return res


# 考虑 W * x 板子的切割
@lru_cache(2**16)
def generate_pattern(items: tuple[Item], res, x) -> tuple[float, tuple[Item]]:
    # 筛选出待切割目标物件的长度
    ls = [item.length for item in items if item.demand > 0 and item.length <= x]
    # 如果没有需要切割的物件的话 直接返回值
    if not ls:
        return res, items
    l_set = set()
    # 首先整个板子的长度需要考虑
    l_set.add(x)
    # 然后待切割的目标物品的倍数长度也要考虑
    for item in items:
        count = 1
        while count * item.length < x and count <= item.demand:
            l_set.add(count * item.length)
            count += 1
    # 根据长度排序
    l_set = sorted(l_set)
    ans = []
    for l in l_set:
        res1, items1 = get_f(l, W, items, res, x)  # 计算出l x W板中切割所能产生的value
        res2, items2 = generate_pattern(items1, res1, x - l)  # 递归的求解(x - l, W)板子的最大value
        res1 += res2  # 得到最优解
        if res1 > 0:
            ans.append((res1, tuple(items2)))
    # 返回总体最优解
    return max(ans, key=lambda x: x[0]) if ans else (0, tuple())


items = items[200:210]
items.sort()

ans = generate_pattern(tuple(items), 0, L)

print(ans)
img = Image.new("RGB", (2440, 1220))
draw = ImageDraw.Draw(img)
for item in ans[1]:
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    for i in item.place:
        for num in range(i[2]):
            draw.rectangle((i[0] + num * item.length, i[1], i[0] + (num + 1) * item.length, i[1] + item.width), fill=color, outline=(155, 155, 155), width=10)
img.show()
