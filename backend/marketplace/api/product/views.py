from django.utils.decorators import method_decorator
from django.db.models import F
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.views.decorators.cache import cache_page

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import *
from core.settings import MINUTE

from marketplace.models import Product, Category, Style
from marketplace.api.product_filter import ProductFilter






class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    ordering_fields = ['price']
    ordering = ['id']
    filterset_fields = ['category', 'style']
    filterset_class = ProductFilter
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(published=True).order_by('?')

        # полнотекстовый поиск
        search_query = self.request.GET.get('search')
        if search_query:
            query = SearchQuery(search_query, config='russian')

            queryset = queryset.annotate(
                rank=SearchRank(F('search_vector'), query)
            ).filter(search_vector=query).filter(rank__gte=0.2).order_by('-rank')

        return queryset.prefetch_related('images')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer
        
    
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializer
    ordering_fields = '__all__'
    search_fields = ['name']
    pagination_class = None
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(1 * MINUTE))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer
    
    
class StyleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Style.objects.prefetch_related('products').all()
    serializer_class = StyleSerializer
    ordering_fields = '__all__'
    search_fields = ['name']
    pagination_class = None
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(1 * MINUTE))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StyleDetailSerializer
        return StyleSerializer
    
  

    
    
