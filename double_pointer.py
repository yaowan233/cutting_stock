from functools import partial
from itertools import chain

from item import Item
from generate_pattern import generate, W, L


def main(total_items: list[Item], output=True, test=False) -> int:
    generate_part = partial(generate, output=output, test=test)
    K = 1.17  # 大于 K 倍面积为一组
    pattern_used = 0
    while total_items:
        # total_items.sort(key=lambda x: x.value)
        # for i in range(2, len(total_items) // 2, 4):
        #     total_items[i], total_items[-i] = total_items[-i], total_items[i]
        # random.shuffle(total_items)
        print("\nitems_remain: ", len(total_items))
        # if TEST:
        #     print(total_items)
        # 前缀和
        prefix_sum = [item.demand for item in total_items]
        for i in range(1, len(total_items)):
            prefix_sum[i] += prefix_sum[i - 1]
        tasks = []
        # 双指针获取区间
        begin, end, _sum = 0, 0, 0
        # 数据太少就直接跑，多了就拆
        if len(total_items) >= 12:
            while end < len(total_items) - 8:
                _sum += total_items[end].value * total_items[end].demand
                end += 1
                # 面积达到要求或者数据太多
                if (_sum >= W * L * K and end - begin > 1) or end - begin >= 11:
                    tasks.append(
                        generate_part(tuple(sorted(total_items[begin:end])), begin, end)
                    )
                    begin = end
                    _sum = 0
                elif end - begin + prefix_sum[end] - prefix_sum[begin] >= 27:
                    end -= 1
                    tasks.append(
                        generate_part(tuple(sorted(total_items[begin:end])), begin, end)
                    )
                    begin = end
                    _sum = 0
            if _sum >= W * L * 0.6 or len(total_items) - begin >= 13:
                mid = (len(total_items) + begin) // 2
                tasks.append(
                    generate_part(tuple(sorted(total_items[begin:mid])), begin, mid)
                )
                tasks.append(
                    generate_part(
                        tuple(sorted(total_items[mid:])), mid, len(total_items)
                    )
                )
            else:
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
        total_items = list(chain(*tasks))
    return pattern_used
