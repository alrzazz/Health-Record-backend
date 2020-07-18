from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class ItemlimitPagination(LimitOffsetPagination):
    # page_size = 2
    default_limit = 5
