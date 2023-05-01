import copy
import random
from functools import lru_cache
from pandas import read_csv
import sys
from PIL import Image, ImageDraw
import timeit
import cProfile

sys.setrecursionlimit(3000)
SHUFFLE = False  # 是否打乱
SCALE = (0, 20)  # 数据取值，items = items[SCALE[0]:SCALE[1]]
TEST = True  # 是否输出测试信息
PROFILE = False  # 是否使用 cProfile 性能分析


class Item:
    def __init__(
        self,
        id: int,
        length: float,
        width: float,
        demand: int,
        value: float = None,
        place: list = None,
    ):
        if place is None:
            place = []
        self.id = id
        self.length = int(length)
        self.width = int(width)
        self.demand = demand
        self.value = value
        self.place = place

    __hash__ = object.__hash__
    __slots__ = "id", "length", "demand", "width", "value", "place"

    # for Item printing
    def __repr__(self) -> str:
        return f"\nid: {self.id:3} ,length: {self.length:4} ,width:{self.width:4} ,demand: {self.demand:2} ,value: {self.value:8} ,pos: {self.place}"

    # for sorting
    def __lt__(self, other):
        return (
            self.width < other.width
            if self.width != other.width
            else self.length < other.length
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
    # if item.length >= 0.5 * L and item.width >= 0.5 * W:
    #     item.value = 4 * item.length * item.width
    # elif item.length >= 0.5 * L or item.width >= 0.5 * W:
    #     item.value = 1.2 * item.length * item.width
    # else:
    item.value = item.length * item.width


@lru_cache(2**16)
def get_f(
    x: int, y: int, old_items: tuple[Item], res: float, x_pos: int
) -> tuple[float, tuple[Item]]:
    # 筛选出待切割目标物件的宽度
    ls = [
        item.width
        for item in old_items
        if item.demand > 0 and item.length <= x and item.width <= y
    ]
    # 如果没有需要切割的物件的话 直接返回值
    if not ls:
        return res, old_items
    miny = min(ls)
    value_ls = (res, old_items)
    for index, item in enumerate(old_items):
        if item.width < miny:
            continue
        # 如果物品能够在长 x 宽 y 的板子上被切割的话
        if y >= item.width and x >= item.length and item.demand > 0:
            new_items = list(old_items)
            new_item = Item(
                item.id,
                item.length,
                item.width,
                item.demand,
                item.value,
                copy.copy(item.place),
            )
            e_i = min(x // item.length, item.demand)  # 在一行中物品能切割的最多数量
            new_item.demand -= e_i  # 减少需求量
            new_item.place.append((L - x_pos, W - y, e_i))  # 增加物品坐标与切割数量
            new_items[index] = new_item
            # 在 (x, y - item.width) 的板子上递归的求解
            f, ans_items = get_f(
                x, y - item.width, tuple(new_items), res + e_i * item.value, x_pos
            )
            # 挑选出最能切割出最多 value 的切割方式
            if f > value_ls[0]:
                value_ls = (f, ans_items)
        elif y < item.width:  # 剪枝，提前跳出循环
            break
    return value_ls


# 考虑 W * x 板子的切割
@lru_cache(2**16)
def generate_pattern(
    items: tuple[Item], res: float, x: int
) -> tuple[float, tuple[Item]]:
    # 如果没有需要切割的物件的话 直接返回值
    if not any(item.demand > 0 and item.length <= x for item in items):
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
    # ans 为总体最优解
    ans = (0, tuple())
    for l in l_set:
        # 计算出 l x W 板中切割所能产生的 value
        res1, items1 = get_f(l, W, items, res, x)
        # 递归求解 (x - l, W) 板子的最大 value
        res2, items2 = generate_pattern(items1, res1, x - l)
        if res2 > ans[0]:
            ans = (res2, items2)
    return ans


if SHUFFLE:
    random.shuffle(items)
items = items[SCALE[0] : SCALE[1]]
items.sort()

if PROFILE:
    cProfile.run("generate_pattern(tuple(items), 0, L)")
    sys.exit(0)

start_test = timeit.default_timer()
ans = generate_pattern(tuple(items), 0, L)

if TEST:
    stop_test = timeit.default_timer()
    print(f"scale: {SCALE[1] - SCALE[0]}, ({SCALE[0]},{SCALE[1]})\tSHUFFLE: {SHUFFLE}")
    print("timeit: ", stop_test - start_test)
    print("ans: ", ans)

img = Image.new("RGB", (2440, 1220))
draw = ImageDraw.Draw(img)
for item in ans[1]:
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    for i in item.place:
        for num in range(i[2]):
            draw.rectangle(
                (
                    i[0] + num * item.length,
                    i[1],
                    i[0] + (num + 1) * item.length,
                    i[1] + item.width,
                ),
                fill=color,
                outline=(155, 155, 155),
                width=10,
            )
img.show()
