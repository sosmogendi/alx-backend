#!/usr/bin/python3
""" FIFO Caching """

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO caching """

    def __init__(self):
        """ Initialize FIFO Cache """
        super().__init__()
        self.key_queue = []

    def put(self, key, item):
        """ Add item to cache using FIFO algorithm """
        if key is None or item is None:
            return

        if key not in self.key_queue:
            self.key_queue.append(key)
        else:
            self.move_key_to_end(key)

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key = self.get_first_key(self.key_queue)
            if first_key:
                self.key_queue.pop(0)
                del self.cache_data[first_key]
                print("DISCARD: {}".format(first_key))

    def get(self, key):
        """ Get item from cache """
        return self.cache_data.get(key, None)

    def move_key_to_end(self, key):
        """ Move key to the end of the queue """
        if self.key_queue[-1] != key:
            self.key_queue.remove(key)
            self.key_queue.append(key)

    @staticmethod
    def get_first_key(keys):
        """ Get the first key from the queue or None """
        return keys[0] if keys else None
