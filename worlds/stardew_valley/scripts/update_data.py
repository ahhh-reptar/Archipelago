import csv
import itertools
import os
from typing import List

from worlds.stardew_valley.items import load_item_csv, Group, ItemData, load_resource_pack_csv

RESOURCE_PACK_CODE_OFFSET = 500
world_folder = os.path.dirname(__file__)


def write_item_csv(items: List[ItemData]):
    with open(world_folder + "/../data/items.csv", 'w') as file:
        item_writer = csv.DictWriter(file, ['id', 'name', 'classification', 'groups'])
        item_writer.writeheader()
        for item in items:
            item_dict = {
                'id': item.code_without_offset,
                'name': item.name,
                'classification': item.classification.name,
                'groups': ','.join(group.name for group in item.groups)
            }
            item_writer.writerow(item_dict)


if __name__ == '__main__':
    loaded_items = load_item_csv()

    item_counter = itertools.count(max(item.code_without_offset
                                       for item in loaded_items
                                       if Group.RESOURCE_PACK not in item.groups
                                       and item.code_without_offset is not None) + 1)
    items_to_write = []
    for item in loaded_items:
        if Group.RESOURCE_PACK in item.groups:
            continue

        if item.code_without_offset is None:
            items_to_write.append(ItemData(next(item_counter), item.name, item.classification, item.groups))
            continue

        items_to_write.append(item)

    all_resource_packs = load_resource_pack_csv()
    resource_pack_counter = itertools.count(RESOURCE_PACK_CODE_OFFSET)
    items_to_write.extend(item for resource_pack in all_resource_packs for item in resource_pack.as_item_data(resource_pack_counter))

    write_item_csv(items_to_write)
