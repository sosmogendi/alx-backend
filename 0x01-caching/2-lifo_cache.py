#!/usr/bin/python3
""" LIFO Caching """

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO caching """

    def __init__(self):
        """ Initialize LIFO Cache """
        super().__init__()
        self.key_stack = []

    def put(self, key, item):
        """ Add item to cache using LIFO algorithm """
        if key is None or item is None:
            return

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            if self.key_stack:
                last_key = self.key_stack.pop()
                del self.cache_data[last_key]
                print("DISCARD: {}".format(last_key))

        if key not in self.key_stack:
            self.key_stack.append(key)
        else:
            self.move_key_to_top(key)

    def get(self, key):
        """ Get item from cache """
        return self.cache_data.get(key, None)

    def move_key_to_top(self, key):
        """ Move key to the top of the stack """
        if self.key_stack[-1] != key:
            self.key_stack.remove(key)
            self.key_stack.append(key)
