#!/usr/bin/python3
""" MRU Caching """

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRU caching """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.access_order = []

    def put(self, key, item):
        """ Puts item in cache using MRU algorithm """
        if key is None or item is None:
            return

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            most_recently_used = self.access_order.pop()
            del self.cache_data[most_recently_used]
            print("DISCARD: {}".format(most_recently_used))

        if key not in self.access_order:
            self.access_order.append(key)
        else:
            self.move_last_list(key)

    def get(self, key):
        """ Gets item from cache and updates access order """
        item = self.cache_data.get(key, None)
        if item is not None:
            self.move_last_list(key)
        return item

    def move_last_list(self, key):
        """ Moves key to the end of the access order list """
        if self.access_order[-1] != key:
            self.access_order.remove(key)
            self.access_order.append(key)
