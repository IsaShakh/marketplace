from django.shortcuts import render
from users.models import User

from core.permissions import IsAdmin, IsModerator
from .serializers import RegisterSerializer, UserProfileSerializer, MyTokenObtainPairSerializer
from rest_framework.generics import CreateAPIView
from core.helpers import DefaultViewSetMixin
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,

)
# Create your views here.


class UserViewSet(RetrieveModelMixin, GenericViewSet, UpdateModelMixin):
    lookup_value_regex = '\\d+|me'
    lookup_field = 'id_or_me'
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsModerator, IsAdmin]

    def get_object(self) -> User:
        if self.kwargs.get(self.lookup_field) != 'me':
            raise ValidationError('You can only request data for "me"')
        return self.request.user
    

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer