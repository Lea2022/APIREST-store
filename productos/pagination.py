from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    # Número de elementos por página (puedes ajustar según tu caso)
    page_size = 5

    # Parámetro para definir la página
    page_query_param = "p"

    # Permitir al cliente definir el tamaño de página
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Personalizar la respuesta paginada.
        """
        return Response(
            {
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next_page": self.get_next_link(),
                "previous_page": self.get_previous_link(),
                "results": data,
            }
        )
