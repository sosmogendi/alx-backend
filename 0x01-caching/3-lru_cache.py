#!/usr/bin/python3
""" LRU Caching """

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRU caching """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.access_order = []

    def put(self, key, item):
        """ Puts item in cache using LRU algorithm """
        if key is None or item is None:
            return

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            least_recently_used = self.get_first_list(self.access_order)
            if least_recently_used:
                self.access_order.pop(0)
                del self.cache_data[least_recently_used]
                print("DISCARD: {}".format(least_recently_used))

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

    @staticmethod
    def get_first_list(array):
        """ Get first element of list or None """
        return array[0] if array else None
