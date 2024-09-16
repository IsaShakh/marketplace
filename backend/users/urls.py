from django.urls import include, path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.api.views import UserViewSet, TokenObtainPairView, RegisterView
from marketplace.api.seller.views import SellerProductViewSet

router = SimpleRouter()
router.register('user', UserViewSet)
router.register('products', SellerProductViewSet)


app_name = 'users'

urlpatterns = [
    path('user/', include(router.urls)),
    
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('registration/', RegisterView.as_view(), name='register'),

    path('user/create-product/', SellerProductViewSet.as_view({'post': 'create'}), name='create-product'),
]