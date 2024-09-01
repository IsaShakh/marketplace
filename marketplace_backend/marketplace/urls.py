from django.urls import include, path
from rest_framework.routers import DefaultRouter
from marketplace.api.views import ProductViewSet, CategoryViewSet, StyleViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet)
router.register(r'styles', StyleViewSet)

app_name = 'marketplace'
urlpatterns = [
    path('', include(router.urls)),
]

