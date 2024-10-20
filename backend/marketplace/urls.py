from django.urls import include, path
from rest_framework.routers import DefaultRouter
from marketplace.api.product.views import ProductViewSet, CategoryViewSet, StyleViewSet
from marketplace.api.seller.views import SellerProductViewSet




router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet)
router.register(r'styles', StyleViewSet)

app_name = 'marketplace'
urlpatterns = [
    path('', include(router.urls)),
]

