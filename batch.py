from functools import cache

from pandas import read_csv
from item import Item
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from greedy_test import main
import warnings

warnings.filterwarnings('ignore')


L = 2440
W = 1220


def read_file(filename: str):
    batch = defaultdict(list)
    data = read_csv(filename)
    temp = {}
    for i in data.iterrows():
        length = i[1]["item_length"]
        width = i[1]["item_width"]
        material = i[1]["item_material"]
        # ensure length >= width always true
        if width > length:
            (length, width) = (width, length)
        if (length, width) not in temp.keys():
            temp[(length, width, material)] = Item(i[0], length, width, i[1]["item_num"], material=material)
        else:
            temp[(length, width, material)].demand += i[1]["item_num"]
    items = list(temp.values())
    del temp
    for item in items:
        if item.length >= 0.5 * L and item.width >= 0.5 * W:
            item.value = 10 * item.length * item.width
        elif item.length >= 0.5 * L or item.width >= 0.5 * W:
            item.value = 5 * item.length * item.width
        else:
            item.value = item.length * item.width
    for item in items:
        batch[item.material].append(item)
    return batch


ans_ls = []
def batch(a11, a22, a33):
    a11 = int(a11)
    a22 = int(a22)
    a33 = int(a33)
    ans = 0
    batch = read_file("dataB/dataB5.csv")
    for i in batch.values():
        if sum([item.demand for item in i]) <= 1000 and sum([item.area for item in i]) <= 250000000:
            # main(i)
            continue
        ratios = [item.ratios for item in i]
        areas = [item.area for item in i]
        X = np.column_stack((ratios, areas))

        # 特征缩放
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # 训练模型
        kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
        kmeans.fit(X_scaled)
        labels = kmeans.labels_
        for index, arr in enumerate(kmeans.cluster_centers_):
            if arr[0] > 0.5:
                t1 = index
            # elif arr[0] < -1:
            #     t2 = index
            elif arr[1] > 1:
                t2 = index
            else:
                t3 = index
        item_t1 = [item for index, item in enumerate(i) if labels[index] == t1]
        item_t2 = [item for index, item in enumerate(i) if labels[index] == t2]
        item_t3 = [item for index, item in enumerate(i) if labels[index] == t3]
        # item_t4 = [item for index, item in enumerate(i) if labels[index] == t4]
        # print(123)
        num, area = 0, 0
        ls = []
        batch_ls = []

        while True:
            if not item_t1 and not item_t2 and not item_t3:
                batch_ls.append(ls)
                break
            for _ in range(a11):
                if item_t2:
                    if num + item_t2[-1].demand > 1000 or area + item_t2[-1].area > 250000000:
                        batch_ls.append(ls)
                        ls = []
                        num, area = 0, 0
                        continue
                    num += item_t2[-1].demand
                    area += item_t2[-1].area
                    ls.append(item_t2.pop())
            for _ in range(a22):
                if item_t1:
                    if num + item_t1[-1].demand > 1000 or area + item_t1[-1].area > 250000000:
                        batch_ls.append(ls)
                        ls = []
                        num, area = 0, 0
                        continue
                    num += item_t1[-1].demand
                    area += item_t1[-1].area
                    ls.append(item_t1.pop())
            for _ in range(a33):
                if item_t3:
                    if num + item_t3[-1].demand > 1000 or area + item_t3[-1].area > 250000000:
                        batch_ls.append(ls)
                        ls = []
                        num, area = 0, 0
                        continue
                    num += item_t3[-1].demand
                    area += item_t3[-1].area
                    ls.append(item_t3.pop())
        use = 0
        for b in batch_ls:
            _, ans = main(b, output=False)
            ans_ls.append(ans)
            # ans += a1
    # return ans
            # print(a2)
         # print('good')
        # batch_ls.append()
        # 可视化结果
        # plt.scatter(X[:, 0], X[:, 1], c=labels)
        # plt.xlabel('Width-to-Height Ratio')
        # plt.ylabel('Area')
        # plt.title('Clustering Based on Rectangle Properties')
        # plt.show()


batch(3, 1, 7)
print(sum(ans_ls)/len(ans_ls))
# from sko.GA import GA
#
# ga = GA(func=batch, n_dim=3, size_pop=4, max_iter=10, prob_mut=0.001, lb=[1, 1, 1], ub=[20, 20, 20], precision=1)
# best_x, best_y = ga.run()
# print('best_x:', best_x, '\n', 'best_y:', best_y)
