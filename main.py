from contextlib import suppress
import os
import timeit

from item import Item
from read_file import read_file
from greedy_test import main

OUTPUT = True  # 是否输出日志


def main_func(a1, a2):
    total_items: list[Item] = read_file("dataA/dataA4.csv", a1, a2)
    # print("total_scale: ", len(total_items))
    # 清空上次 log
    if OUTPUT:
        with suppress(FileExistsError):
            os.mkdir("output")
        with open("output/log.txt", "w") as f:
            f.write("")
    # 计算总时间
    start = timeit.default_timer()
    pattern_used = main(total_items, output=OUTPUT)
    stop = timeit.default_timer()
    # print(f"total_time: {stop - start}, pattern_used: {pattern_used}")
    return pattern_used


if __name__ == "__main__":
    print(main_func(10, 5))
    # print(main_func(10, 2))

    from sko.GA import GA
    #
    # ga = GA(func=main_func, n_dim=2, size_pop=30, max_iter=100, prob_mut=0.001, lb=[1, 1], ub=[1000, 1000], precision=1)
    # best_x, best_y = ga.run()
    # print('best_x:', best_x, '\n', 'best_y:', best_y)
    # main_func(100, 20)
