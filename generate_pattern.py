from functools import lru_cache
from sortedcontainers import SortedSet
from itertools import chain
import copy
import timeit

from item import Item
from draw import draw

L = 2440
W = 1220


@lru_cache(2**16)
def get_f(
    x: int, y: int, old_items: tuple[Item], res: float, x_pos: int
) -> tuple[float, tuple[Item]]:
    miny = 1e7
    for temp in old_items:
        if (
            temp.demand > 0
            and temp.length <= x
            and temp.width <= y
            and miny > temp.width
        ):
            miny = temp.width
    # 如果没有需要切割的物件的话 直接返回值
    if miny == 1e7:
        return res, old_items
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
    l_set = SortedSet()
    # 首先整个板子的长度需要考虑
    l_set.add(x)
    # 然后待切割的目标物品的倍数长度也要考虑
    for item in items:
        count = 1
        while count * item.length < x and count <= item.demand:
            l_set.add(count * item.length)
            count += 1
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


def generate(items: tuple[Item], begin=0, end=1, output=False, test=True) -> list[Item]:
    print(
        f"running scale: {len(items):2}, [{begin},{end - 1}]\tvalue_sum: {sum(i.value*i.demand for i in items)}\tdemand_sum: {sum(i.demand for i in items)}"
    )
    start_test = timeit.default_timer()
    ans = generate_pattern(items, 0, L)
    stop_test = timeit.default_timer()
    if output:
        with open("output/log.txt", "a") as f:
            f.write(
                f"scale: {len(items)}, [{begin},{end - 1}]\ntimeit: {stop_test - start_test}\nans: {ans}\n"
            )
    elif test:
        print("timeit: ", stop_test - start_test)
        print("ans: ", ans)
    draw(ans[1], output, L=L, W=W)
    result: list[Item] = list(filter(lambda x: x.demand != 0, chain(ans[1])))
    # debug：重复绘制
    for temp in result:
        if temp.place:
            temp.place.clear()
    return result
