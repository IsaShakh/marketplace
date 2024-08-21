import django_filters
from django_filters import rest_framework as filters
from marketplace.models import Category, Product, Style
from django.db.models import Q



class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class ProductFilter(filters.FilterSet):
    category = NumberInFilter(method='category_filter')
    style = NumberInFilter(method='style_filter')
    moderation_status = filters.MultipleChoiceFilter(choices=Product.ModerationStatuses.choices)
    
    class Meta:
        model = Product
        fields = ['category', 'style', 'moderation_status', 'published']
        
    @staticmethod
    def category_filter(queryset, name, value):
        if not value:
            return queryset
        
        categories = Category.objects.filter(id__in=value)
        q = Q()
        for category in categories:
            q |= Q(category__in=category.get_descendants(include_self=True))
        
        return queryset.filter(q)
    
    @staticmethod
    def style_filter(queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(style__id__in=value)