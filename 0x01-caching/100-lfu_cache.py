#!/usr/bin/python3
""" LFU Caching """

from base_caching import BaseCaching

class LFUCache(BaseCaching):
    """ LFU caching """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.frequency = {}
        self.access_order = []

    def put(self, key, item):
        """ Puts item in cache using LFU algorithm """
        if key is None or item is None:
            return

        self.cache_data[key] = item

        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)

        # Update frequency count
        self.frequency[key] = self.frequency.get(key, 0) + 1

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            self.discard_least_frequent()

    def get(self, key):
        """ Gets item from cache and updates frequency """
        item = self.cache_data.get(key, None)
        if item is not None:
            self.update_frequency(key)
        return item

    def discard_least_frequent(self):
        """ Discards the least frequent item, using LRU for tie-breaking """
        min_frequency = min(self.frequency.values())
        candidates = [key for key, freq in self.frequency.items() if freq == min_frequency]
        for key in self.access_order:
            if key in candidates:
                self.access_order.remove(key)
                del self.cache_data[key]
                del self.frequency[key]
                print("DISCARD: {}".format(key))
                break

    def update_frequency(self, key):
        """ Updates frequency of the accessed item """
        self.frequency[key] += 1
