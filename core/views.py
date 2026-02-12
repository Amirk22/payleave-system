from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework import generics ,status
from rest_framework.permissions import BasePermission
from rest_framework import permissions





def home(request):
    return HttpResponse("<h1>Pay Leave</h1>")

#.............
# Authentication API View

class IsLoggedIn(permissions.BasePermission):
    message = "You must be logged in to access this."

    def has_permission(self, request, view):
        return request.session.get('user_id') is not None

class IsManager(BasePermission):
    def has_permission(self,request,view):
        user_id = request.session.get('user_id')
        if not user_id:
            return False
        user = User.objects.get(id=user_id)
        return user.role == 'MANAGER'

class IsEMPLOYEE(BasePermission):
    def has_permission(self,request,view):
        user_id = request.session.get('user_id')
        if not user_id:
            return False
        user = User.objects.get(id=user_id)
        return user.role == "EMPLOYEE"



class UserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email'].lower()
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({'error': 'This user does not exist.'}, status=400)
        request.session['user_id'] = user.id
        return Response({'message': 'Logged in', 'user': user.full_name}, status=200)

class LogoutAPIView(APIView):

    def post(self,request,*args, **kwargs):
        request.session.flush()
        return Response({'message': 'Logged out'}, status=200)

class ProfileAPIView(APIView):
    def get(self,request,*args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'error': 'Not Login'}, status=401)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=404)
        serializer = ProfileSerializer(user)
        return Response(serializer.data,status=200)

#.............
