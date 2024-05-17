from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 6


class CustomPagePagination(PageNumberPagination):
    # Default page size
    page_size = 6
    page_size_query_param = 'page_size'

