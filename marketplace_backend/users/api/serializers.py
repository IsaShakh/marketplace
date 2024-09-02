from rest_framework import serializers
from users.models import User
from marketplace.api.product.serializers import ProductSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('nickname', 'password', 'password2', 'email', 'first_name', 'second_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            nickname=validated_data['nickname'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            second_name=validated_data['second_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    owned_positions = ProductSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'email',
            'phone',
            'birthday',
            'first_name',
            'second_name',
            'profile_photo',
            'is_superuser',
            'email_verified',
            'owned_positions',
        ]
        read_only_fields = [
            'email',
        ]
        
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nickname'] = user.nickname
        token['email'] = user.email

        return token