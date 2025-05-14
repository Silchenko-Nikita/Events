import django_filters

from events_app.models import Event


class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFromToRangeFilter()
    organizer = django_filters.CharFilter(field_name='organizer__username', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'organizer']
