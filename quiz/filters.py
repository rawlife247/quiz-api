from django_filters import rest_framework as filters
from .models import Participant


class ParticipantFilter(filters.FilterSet):
    categories = filters.CharFilter(method='filter_by_categories', field_name='quiz__categories__name')
    tags = filters.CharFilter(method='filter_by_tags', field_name='quiz__tags__name')

    class Meta:
        model = Participant
        fields = ['categories', 'tags']

    def filter_by_categories(self, queryset, name, value):
        categories = value.split(',')
        for category in categories:
            category = category.strip()
            if category:
                queryset = queryset.filter(quiz__categories__name__iexact=category)
        return queryset

    def filter_by_tags(self, queryset, name, value):
        tags = value.split(',')
        for tag in tags:
            tag = tag.strip()
            if tag:
                queryset = queryset.filter(quiz__tags__name__iexact=tag)
        return queryset
