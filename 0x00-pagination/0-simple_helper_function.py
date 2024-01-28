#!/usr/bin/env python3
'''
    Simple helper function for pagination.
'''

def index_range(page, page_size):
    '''
        Returns the range of indexes for a given page.
    '''
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index
