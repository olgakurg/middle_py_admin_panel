from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 50 
    page_size_query_param = 'page_size'
    max_page_size = 50 

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data = {
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'prev': self.page.previous_page_number() if self.page.has_previous() else None,
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'results': response.data['results']
        }
        return response