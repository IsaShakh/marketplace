import django_filters
from django_filters import rest_framework as filters
from marketplace.models import Category, Product, Style
from django.db.models import Q

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class ProductFilter(filters.FilterSet):
    category = NumberInFilter(method='filter_by_category')
    style = NumberInFilter(method='filter_by_style')
    moderation_status = filters.MultipleChoiceFilter(choices=Product.ModerationStatuses.choices)

    class Meta:
        model = Product
        fields = ['category', 'style', 'moderation_status', 'published']

    @staticmethod
    def filter_by_category(queryset, name, value):
        if not value:
            return queryset
        
        # Получаем все потомки выбранных категорий
        categories = Category.objects.filter(id__in=value).get_descendants(include_self=True)
        return queryset.filter(category__in=categories)

    @staticmethod
    def filter_by_style(queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(style__id__in=value)
