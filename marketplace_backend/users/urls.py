from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.api.views import UserViewSet, TokenObtainPairView, RegisterView


router = SimpleRouter()
router.register('users', UserViewSet)


app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
    
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('registration/', RegisterView.as_view(), name='register'),
]