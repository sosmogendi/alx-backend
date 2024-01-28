#!/usr/bin/env python3
'''
    Simple helper function
'''


def index_range(page, page_size):
    '''
        Returns the range of indexes for a given page.
    '''
    start_p = (page - 1) * page_size
    end_p = page * page_size
    return start_p, end_p
