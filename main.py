import random
import sys, timeit, cProfile
from item import Item
from read_file import read_file
from generate_pattern import generate
from draw import draw

sys.setrecursionlimit(3000)

SHUFFLE = False  # 是否打乱
SCALE = (0, 5)  # 数据取值，items = items[SCALE[0]:SCALE[1]]
TEST = True  # 是否输出测试信息
PROFILE = False  # 是否使用 cProfile 性能分析


total_items: list[Item] = read_file("dataA/dataA1.csv")
pattern_used = 0

if SHUFFLE:
    random.shuffle(total_items)
total_items = total_items[SCALE[0] : SCALE[1]]

if PROFILE:
    cProfile.run("generate(tuple(total_items), 0)")
    sys.exit(0)

# while...
items = total_items  # [...:...]
items.sort()
# debug
print(items)

start_test = timeit.default_timer()
ans = generate(tuple(items), 0)
if TEST:
    stop_test = timeit.default_timer()
    print(f"scale: {SCALE[1] - SCALE[0]}, ({SCALE[0]},{SCALE[1]})\tSHUFFLE: {SHUFFLE}")
    print("timeit: ", stop_test - start_test)
    print("ans: ", ans)

draw(ans[1])
