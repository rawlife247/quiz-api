from django_filters import rest_framework as filters
from .models import Participant


class ParticipantFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='quiz__categories__name', lookup_expr='iexact')
    tag = filters.CharFilter(field_name='quiz__tags__name', lookup_expr='iexact')
    quiz_id = filters.NumberFilter(field_name='quiz_id')

    class Meta:
        model = Participant
        fields = ['category', 'tag', 'quiz_id']
