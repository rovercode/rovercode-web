"""Mission Control pagination."""
from collections import OrderedDict

from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    """Pagination that allows settings page size and displays total pages."""

    page_size_query_param = 'size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """Paginated response."""
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('free_max', settings.FREE_TIER_PROGRAM_LIMIT),
            ('total_pages', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
