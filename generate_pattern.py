from item import Item
from functools import lru_cache, partial
import copy

L = 2440
W = 1220


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


generate = partial(generate_pattern, x=L)
