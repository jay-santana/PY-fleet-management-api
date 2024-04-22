from django.db.models import Q

class TaxiUtils:
    def __init__(self, request):
        self.request = request
    # Function to filter taxis
    def filter_taxis(self, taxis, filter_by):
        if filter_by is not None:
            # Check if it's a number (ID) or plate
            if filter_by.isdigit():  # If it's a number, assume it's the ID
                return taxis.filter(id=int(filter_by))
            else:  # If it's not a number, assume it's the plate
                return taxis.filter(plate__icontains=filter_by)
        return taxis

    # Function to order taxis
    def sort_taxis(self, taxis, sort_by):
        if sort_by is not None:
            return taxis.order_by('-' + sort_by[1:] if sort_by.startswith('-') else sort_by)
        return taxis

    # Function to search for taxis
    def search_taxis(self, taxis, search):
        if search is not None:
            return taxis.filter(Q(id__icontains=search) | Q(plate__icontains=search))
        return taxis

    # Function to get the page size of a request
    def get_page_size(self):
        page_size = self.request.query_params.get('page_size', 10)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 10
        return page_size

    # Function to get the page number of a request
    def get_page_number(self):
        page_number = self.request.query_params.get('page', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1
        return page_number
