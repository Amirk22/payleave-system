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
# LeaveRequest API View

class LeaveRequestAPIView(generics.ListCreateAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsEMPLOYEE]

    def get_queryset(self):
        user_id = self.request.session.get('user_id')
        if not user_id:
            return LeaveRequest.objects.none()

        this_month = timezone.now().month
        return LeaveRequest.objects.filter( employee_id=user_id, start_date__month=this_month)

    def perform_create(self, serializer):
        user_id = self.request.session.get('user_id')
        employee = User.objects.get(id=user_id, role='EMPLOYEE')
        serializer.save(employee=employee)

class LeaveListAPIView(generics.ListAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsManager]
    def get_queryset(self):
        this_month = timezone.now().month
        return LeaveRequest.objects.filter(status="PENDING", start_date__month=this_month)

class LeaveResponseDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = LeaveResponseSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        return LeaveRequest.objects.all()
    def perform_update(self, serializer):
        user_id = self.request.session.get('user_id')
        manager = User.objects.get(id=user_id,role='MANAGER')
        serializer.save(approved_by=manager)

#.............
# OvertimeLog API View

class OvertimeLogListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OvertimeLogSerializer
    permission_classes = [IsEMPLOYEE]

    def get_queryset(self):
        user_id = self.request.session.get('user_id')
        return OvertimeLog.objects.filter(employee_id=user_id)

    def perform_create(self, serializer):
        user_id = self.request.session.get('user_id')
        employee = User.objects.get(id=user_id, role='EMPLOYEE')
        serializer.save(employee=employee)