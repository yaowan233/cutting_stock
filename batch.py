from pandas import read_csv
from item import Item
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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


batch = read_file("dataB/dataB1.csv")
for i in batch.values():
    if sum([item.demand for item in i]) <= 1000 and sum([item.area for item in i]) <= 250000000:
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
    print(123)
    num, area = 0, 0
    ls = []
    batch_ls = []

    while True:
        if not item_t1 and not item_t2 and not item_t3:
            batch_ls.append(ls)
            break
        if item_t2:
            if num + item_t2[-1].demand > 1000 or area + item_t2[-1].area > 250000000:
                batch_ls.append(ls)
                ls = []
                num, area = 0, 0
                continue
            num += item_t2[-1].demand
            area += item_t2[-1].area
            ls.append(item_t2.pop())
        for _ in range(2):
            if item_t1:
                if num + item_t1[-1].demand > 1000 or area + item_t1[-1].area > 250000000:
                    batch_ls.append(ls)
                    ls = []
                    num, area = 0, 0
                    continue
                num += item_t1[-1].demand
                area += item_t1[-1].area
                ls.append(item_t1.pop())
            if item_t3:
                if num + item_t3[-1].demand > 1000 or area + item_t3[-1].area > 250000000:
                    batch_ls.append(ls)
                    ls = []
                    num, area = 0, 0
                    continue
                num += item_t3[-1].demand
                area += item_t3[-1].area
                ls.append(item_t3.pop())
    print('???')
    # batch_ls.append()
    # 可视化结果
    # plt.scatter(X[:, 0], X[:, 1], c=labels)
    # plt.xlabel('Width-to-Height Ratio')
    # plt.ylabel('Area')
    # plt.title('Clustering Based on Rectangle Properties')
    # plt.show()
