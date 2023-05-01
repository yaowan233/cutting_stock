from itertools import chain
import timeit

from item import Item
from draw import draw

L = 2440
W = 1220


def get_f(
    x: int, y: int, old_items: list[Item], res: float, x_pos: int
) -> tuple[float, list[Item]]:
    items = [item for item in old_items if item.demand > 0 and item.length <= x and item.width <= y]
    if not items:
        return res, old_items
    item = max(items, key=lambda x: x.value)
    # 如果没有需要切割的物件的话 直接返回值
    e_i = min(x // item.length, item.demand)  # 在一行中物品能切割的最多数量
    item.demand -= e_i  # 减少需求量
    item.place.append((L - x_pos, W - y, e_i))  # 增加物品坐标与切割数量
    # 在 (x, y - item.width) 的板子上递归的求解
    return get_f(x, y - item.width, old_items, res + e_i * item.value, x_pos)


# 考虑 W * x 板子的切割
def generate_pattern(
    items: list[Item], res: float, x: int
) -> tuple[float, list[Item]]:
    # 如果没有需要切割的物件的话 直接返回值
    items_new = [item for item in items if item.demand > 0 and item.length <= x]
    if not items_new:
        return res, items
    item = max(items, key=lambda x: x.value)
    l = item.length
    res, items = get_f(l, W, items, res, x)
    return generate_pattern(items, res, x - l)


def generate(items: list[Item], begin=0, end=1, output=False, test=True) -> list[Item]:
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
