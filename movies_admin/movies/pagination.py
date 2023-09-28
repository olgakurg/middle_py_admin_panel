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
            'prev': self.get_previous_link(),
            'next': self.get_next_link(),
            'results': response.data['results']
        }
        return response