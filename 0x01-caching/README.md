# Caching Algorithms Project

## Overview
This project implements different caching algorithms in Python. Caching is a technique used to store frequently accessed data in a fast-accessible storage space to improve overall system performance.

## Caching Algorithms Implemented
1. **LRU (Least Recently Used):** Removes the least recently used items first.
2. **FIFO (First-In-First-Out):** Removes the oldest items first.
3. **LIFO (Last-In-First-Out):** Removes the newest items first.
4. **MRU (Most Recently Used):** Removes the most recently used items first.
5. **LFU (Least Frequently Used):** Removes the least frequently used items first.

## Project Structure
- `base_caching.py`: Base class containing constants and methods common to all caching algorithms.
- `lru_cache.py`: Implementation of the LRU caching algorithm.
- `fifo_cache.py`: Implementation of the FIFO caching algorithm.
- `lifo_cache.py`: Implementation of the LIFO caching algorithm.
- `mru_cache.py`: Implementation of the MRU caching algorithm.
- `lfu_cache.py`: Implementation of the LFU caching algorithm.

## How to Use
1. Each caching algorithm is implemented as a separate class inheriting from `BaseCaching`.
2. Instantiate the desired caching class (e.g., `LRUCache()`).
3. Use the `put` method to add items to the cache.
4. Use the `get` method to retrieve items from the cache.
5. Check the cache status using the `print_cache` method.

## Running the Code
Ensure that you have Python 3.7 or later installed. Execute the scripts on Ubuntu 18.04 LTS.

Example:
```bash
$ python3 lru_cache.py
