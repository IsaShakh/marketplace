from rest_framework.routers import DefaultRouter
from marketplace.api.views import ProductViewSet, CategoryViewSet, StyleViewSet
from django.urls import include, path

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('styles', StyleViewSet)

app_name = 'products'
urlpatterns = [
    path('', include(router.urls)),
]
