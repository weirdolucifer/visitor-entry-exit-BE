from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Class to set pagination attributes for standard results"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000
