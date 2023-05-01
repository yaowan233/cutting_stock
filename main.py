from contextlib import suppress
import random, os
import sys, timeit, cProfile

from item import Item
from read_file import read_file

sys.setrecursionlimit(3000)

SHUFFLE = False  # 是否打乱
SCALE = (0, 200)  # 数据取值
TEST = False  # 是否输出测试信息
PROFILE = False  # 是否使用 cProfile 性能分析
OUTPUT = True  # 是否输出日志


total_items: list[Item] = read_file("dataA/dataA1.csv")

if SHUFFLE:
    random.shuffle(total_items)
total_items = total_items[SCALE[0] : SCALE[1]]
print("total_scale: ", len(total_items))

if PROFILE:
    cProfile.run("generate(tuple(total_items), 0)")
    sys.exit(0)


from double_pointer import main

if __name__ == "__main__":
    # 清空上次 log
    if OUTPUT:
        with suppress(FileExistsError):
            os.mkdir("output")
        with open("output/log.txt", "w") as f:
            f.write("")
    # 计算总时间
    start = timeit.default_timer()
    pattern_used = main(total_items, output=OUTPUT, test=TEST)
    stop = timeit.default_timer()
    print(f"total_time: {stop - start}, pattern_used: {pattern_used}")
