from django.db.models import Q, Max, Subquery
from datetime import datetime

from .models import Trajectories

class BaseUtils:
    def __init__(self, request):
        self.request = request
    
    def filter_objects(self, queryset, filter_by):
        if filter_by is None:
            return queryset
        if hasattr(queryset, 'filter'):
            return queryset.filter(Q(taxi__id=int(filter_by)) if filter_by.isdigit() else Q(taxi__plate__iexact=filter_by))
        else:
            return [item for item in queryset if str(item.taxi.id) == filter_by or item.taxi.plate.lower() == filter_by.lower()]

    def sort_objects(self, queryset, sort_by):
        if sort_by is not None:
            ascending = not sort_by.startswith('-')
            field_name = sort_by.lstrip('-')
            if isinstance(queryset, list):
                return sorted(queryset, key=lambda obj: (
                getattr(obj.taxi, field_name) if hasattr(obj.taxi, field_name) else getattr(obj, field_name),
            ), reverse=not ascending)
            else:
                model_field = f'taxi__{field_name}' if hasattr(Trajectories, 'taxi') and hasattr(Trajectories.taxi, field_name) else field_name
                return queryset.order_by(model_field if ascending else f'-{model_field}')
        return queryset

    def search_objects(self, queryset, search, *fields):
        if search is not None:
            search_lower = search.lower()
            search_date = None
            try:
                search_date = datetime.fromisoformat(search.replace('Z', '+00:00'))  # Parse ISO format with timezone
            except ValueError:
                pass
            if isinstance(queryset, list):  # Verifica se é uma lista
                return [item for item in queryset if any(str(getattr(item.taxi, field)).lower() == search_lower for field in ['id', 'plate']) or str(item.id).lower() == search_lower or (search_date and item.date == search_date) or str(item.latitude).lower() == search_lower or str(item.longitude).lower() == search_lower]
            else:  # Se for um queryset
                query = Q()
                for field in ['id', 'taxi__id', 'taxi__plate', 'latitude', 'longitude']:
                    query |= Q(**{f'{field}__icontains': search_lower})
                if search_date is not None:
                    query |= Q(date=search_date)
                return queryset.filter(query)
        return queryset
    
    def get_page_size(self):
        page_size = self.request.query_params.get('page_size', 10)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 10
        return page_size
    
    def get_page_number(self):
        page_number = self.request.query_params.get('page', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1
        return page_number

class TaxiUtils(BaseUtils):

    def filter_taxis(self, taxis, filter_by):
        if filter_by is None:
            return taxis
        if hasattr(taxis, 'filter'):
            return taxis.filter(Q(id=int(filter_by)) if filter_by.isdigit() else Q(plate__iexact=filter_by))
        else:
            return [taxi for taxi in taxis if str(taxi.id) == filter_by or taxi.plate.lower() == filter_by.lower()]

    def sort_taxis(self, taxis, sort_by):
        if sort_by is not None:
            ascending = not sort_by.startswith('-')
            field_name = sort_by.lstrip('-')
            if isinstance(taxis, list):
                return sorted(taxis, key=lambda taxi: getattr(taxi, field_name), reverse=not ascending)
            else:
                ordering = [field_name if ascending else '-' + field_name]
                return taxis.order_by(*ordering)
        return taxis
    
    def search_taxis(self, taxis, search):
        if search is not None:
            search_lower = str(search).lower()
            if isinstance(taxis, list):  # Verifica se é uma lista
                return [taxi for taxi in taxis if any(str(getattr(taxi, field)).lower() == search_lower for field in ['id', 'plate'])]
            else:  # Se for um queryset
                query = Q()
                for field in ['id', 'plate']:
                    query |= Q(**{f'{field}__icontains': search_lower})
                return taxis.filter(query)
        return taxis
       
class TrajectoriesUtils(BaseUtils):

    def filter_trajectories(self, trajectories, filter_by):
        return self.filter_objects(trajectories, filter_by)
    
    def sort_trajectories(self, trajectories, sort_by):
        return self.sort_objects(trajectories, sort_by)

    def search_trajectories(self, trajectories, search):   
        if search:
            return self.search_objects(trajectories, search, 'id', 'taxi__id', 'taxi__plate', 'date', 'latitude', 'longitude')
        return trajectories

class LastTaxisLocationUtils(BaseUtils):
    
    def get_taxis_last_location(self, search_date=None):
        # Filtra os trajetos com base na data, se fornecida
        if search_date:
            last_trajectories = Trajectories.objects.filter(date__lte=search_date).order_by('-date').distinct('taxi_id')
        else:
            # Obtém o último trajeto de cada táxi
            last_trajectories = Trajectories.objects.filter(
                id__in=Subquery(
                    Trajectories.objects.values('taxi_id').annotate(
                        last_trajectory_id=Max('id')
                    ).values('last_trajectory_id')
                )
            )
        return last_trajectories
    
    def filter_last_locations(self, last_locations, filter_by):
        return self.filter_objects(last_locations, filter_by)
 
    def sort_last_locations(self, last_locations, sort_by):
        return self.sort_objects(last_locations, sort_by)
    
    def search_last_locations(self, last_locations, search):  
        if search:
            return self.search_objects(last_locations, search, 'id', 'taxi__id', 'taxi__plate', 'date', 'latitude', 'longitude')
        return last_locations

