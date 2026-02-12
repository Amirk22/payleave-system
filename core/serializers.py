from rest_framework import serializers
from core.models import *





# Authentication

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role'
            , 'monthly_salary', 'working_hours', 'manager', 'is_active', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'monthly_salary',
                  'working_hours', 'manager', 'is_active']
        read_only_fields = ['monthly_salary', 'working_hours', 'manager', 'is_active']

#.............
