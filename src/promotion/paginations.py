from rest_framework.pagination import PageNumberPagination


class CustomPagePagination(PageNumberPagination):
    # Default page size
    page_size = 6
    page_size_query_param = 'page_size'
