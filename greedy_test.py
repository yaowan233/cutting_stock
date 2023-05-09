from item import Item
from greedy import generate


def main(total_items: list[Item], output=True, test=False):
    pattern_used = 0
    item_areas = sum([item.length * item.width * item.demand for item in total_items])
    while total_items:
        pattern_used += 1
        total_items = generate(
            total_items, 0, len(total_items), output=output, test=test
        )
        # print("\nitems_remain: ", len(total_items))
    return pattern_used, item_areas / (pattern_used * 1220 * 2440)
