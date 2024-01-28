#!/usr/bin/env python3
'''
    Simple helper function for pagination.
'''

def index_range(page, page_size):
    '''
        Returns the range of indexes for a given page.

        Parameters:
    - page (int): The current page number (1-indexed).
    - page_size (int): The number of items per page.
    '''
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index
