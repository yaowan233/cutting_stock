from contextlib import suppress
from functools import partial
import random, os
import sys, timeit, cProfile
from itertools import chain

from item import Item
from read_file import read_file
from generate_pattern import generate, W, L

sys.setrecursionlimit(3000)

SHUFFLE = False  # 是否打乱
SCALE = (200, 400)  # 数据取值，items = items[SCALE[0]:SCALE[1]]
TEST = True  # 是否输出测试信息
PROFILE = False  # 是否使用 cProfile 性能分析
OUTPUT = True  # 是否输出日志


total_items: list[Item] = read_file("dataA/dataA1.csv")
pattern_used = 0

if SHUFFLE:
    random.shuffle(total_items)
total_items = total_items[SCALE[0] : SCALE[1]]

if PROFILE:
    cProfile.run("generate(tuple(total_items), 0)")
    sys.exit(0)

generate_part = partial(generate, output=OUTPUT, test=TEST)


def main():
    K = 1.3  # 大于 K 倍面积为一组；K = 1.9 时太慢了
    global pattern_used, total_items, TEST
    while total_items:
        tasks = []
        # 双指针获取区间
        begin, end, _sum = 0, 0, 0
        # 数据太少就直接跑，多了就拆
        if len(total_items) > 10:
            while end < len(total_items) - 8:
                _sum += total_items[end].value * total_items[end].demand
                end += 1
                # 面积达到要求或者数据太多
                if _sum >= W * L * K or end - begin >= 13:
                    tasks.append(
                        generate_part(tuple(sorted(total_items[begin:end])), begin, end)
                    )
                    begin = end
                    _sum = 0
            if _sum >= W * L * 0.7 or end - begin >= 13:
                tasks.append(
                    generate_part(tuple(sorted(total_items[begin:end])), begin, end)
                )
                tasks.append(
                    generate_part(
                        tuple(sorted(total_items[end:])), end, len(total_items)
                    )
                )
            elif end < len(total_items):
                tasks.append(
                    generate_part(
                        tuple(sorted(total_items[begin:])), begin, len(total_items)
                    )
                )
        else:
            total_items.sort()
            tasks.append(generate_part(tuple(total_items), 0, len(total_items)))

        pattern_used += len(tasks)
        # first_result = await asyncio.gather(*tasks)
        total_items = list(filter(lambda x: x.demand != 0, chain(*tasks)))
        print("\nitems_remain: ", len(total_items), total_items)


if __name__ == "__main__":
    # 清空上次 log
    if OUTPUT:
        with suppress(FileExistsError):
            os.mkdir("output")
        with open("output/log.txt", "w") as f:
            f.write("")
    # 计算总时间
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print(f"total_time: {stop - start}, pattern_used: {pattern_used}")
