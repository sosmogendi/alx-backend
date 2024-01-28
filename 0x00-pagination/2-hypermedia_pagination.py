#!/usr/bin/env python3
'''
    Simple pagination.
'''
import csv
import math
from typing import List


def index_range(page, page_size):
    '''
        Returns the range of indexes for a given page.
    '''
    start_p = (page - 1) * page_size
    end_p = page * page_size
    return start_p, end_p


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''
            Returns a page of data.
        '''
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        self.dataset()

        if self.dataset() is None:
            return []

        indexRange1 = index_range(page, page_size)
        return self.dataset()[indexRange1[0]:indexRange1[1]]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        '''
            Returns info about datset.
        '''
        data = self.get_page(page, page_size)
        dataSet = self.__dataset
        lenSet = len(dataSet) if dataSet else 0

        totalPages = math.ceil(lenSet / page_size) if dataSet else 0
        page_size = len(data) if data else 0

        prevPagep = page - 1 if page > 1 else None
        nextPagep = page + 1 if page < totalPages else None

        hyperMedia = {
            'page_size': page_size,
            'page': page,
            'data': data,
            'next_page': nextPagep,
            'prev_page': prevPagep,
            'total_pages': totalPages
        }

        return hyperMedia
