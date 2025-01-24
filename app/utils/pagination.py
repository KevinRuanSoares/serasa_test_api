from rest_framework.pagination import PageNumberPagination
from urllib.parse import urlparse, parse_qs
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        next_page = None
        previous_page = None

        if self.get_next_link():
            next_url = self.get_next_link()
            parsed_next_url = urlparse(next_url)
            next_page = parse_qs(parsed_next_url.query).get('page', [None])[0]

        if self.get_previous_link():
            previous_url = self.get_previous_link()
            parsed_previous_url = urlparse(previous_url)
            previous_page = parse_qs(parsed_previous_url.query).get('page', [None])[0]
            if previous_page is None and self.page.number > 1:
                previous_page = str(self.page.number - 1)

        return Response({
            'count': self.page.paginator.count,
            'next': next_page,
            'previous': previous_page,
            'results': data
        })
