from rest_framework.pagination import LimitOffsetPagination

class SnippetListOPagination(LimitOffsetPagination): #/?limit=5&offset=10 (we will skip first 10 elements)
    default_limit = 3