from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class ItemlimitPgination(LimitOffsetPagination):
    # page_size = 2
    default_limit = 10
