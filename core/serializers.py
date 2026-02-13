from datetime import timedelta
from rest_framework import serializers
from django.utils import timezone
from django.db.models import Q
from core.models import User, LeaveRequest, OvertimeLog, PayrollRun
from datetime import datetime





#.............
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
# LeaveRequest

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LeaveRequest
        fields = "__all__"
        read_only_fields = ["id","status","end_date","approved_by"]

    def validate(self, data):
        request = self.context['request']
        user_id = request.session.get('user_id')

        if not user_id:
            raise serializers.ValidationError("Authentication required.")

        employee = User.objects.get(id=user_id)
        start_date = data['start_date']
        first_day = start_date.replace(day=1)
        if start_date.month == 12:
            next_month = start_date.replace(year=start_date.year + 1, month=1, day=1)
        else:
            next_month = start_date.replace(month=start_date.month + 1, day=1)
        monthly_requests_count = LeaveRequest.objects.filter(
            employee=employee,
            start_date__gte=first_day,
            start_date__lt=next_month
        ).filter(
            Q(status='APPROVED') | Q(status='PENDING')
        ).count()
        if monthly_requests_count >= 2:
            raise serializers.ValidationError(
                "You can submit a maximum of 2 optional leave requests per month."
            )
        if start_date.weekday() == 6:
            raise serializers.ValidationError(
                "Optional leave cannot be requested for Sundays."
            )
        today = timezone.localdate()
        if start_date < today:
            raise serializers.ValidationError(
                "Optional leave cannot be requested for past dates."
            )
        if LeaveRequest.objects.filter(employee=employee, start_date=start_date).exists():
            raise serializers.ValidationError("You already have an optional leave request for this date.")
        return data

    def create(self, validated_data):
        start_date = validated_data['start_date']
        validated_data['end_date'] = start_date + timedelta(days=1)
        return super().create(validated_data)

class LeaveResponseSerializer(serializers.ModelSerializer):
    approved_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LeaveRequest
        fields = "__all__"
        read_only_fields = ["id","employee","end_date","start_date","description"]

#.............
# OvertimeLog

class OvertimeLogSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OvertimeLog
        fields = "__all__"

    def validate(self, data):
        request = self.context['request']
        user_id = request.session.get('user_id')
        if not user_id:
            raise serializers.ValidationError("User not authenticated.")

        try:
            employee = User.objects.get(id=user_id, role='EMPLOYEE')
        except User.DoesNotExist:
            raise serializers.ValidationError("Employee not found.")

        date_obj = data.get('date')
        if not date_obj:
            raise serializers.ValidationError("Date is required.")

        if LeaveRequest.objects.filter(employee=employee, start_date=date_obj).filter(Q(status="PENDING")| Q(status="APPROVED")).exists():
            raise serializers.ValidationError("You already had a day off on this date.")

        if OvertimeLog.objects.filter(employee=employee,date=date_obj).exists():
            raise serializers.ValidationError("You already have an overtime on this date.")

        if date_obj.weekday() == 6:
            raise serializers.ValidationError("Overtime cannot be recorded on Sundays.")

        payroll = PayrollRun.objects.filter(
            year=date_obj.year,
            month=date_obj.month
        ).first()

        if not payroll:
            raise serializers.ValidationError("Payroll period is not opened yet.")

        if payroll.is_finalized:
            raise serializers.ValidationError("The overtime registration period for this month has expired.")

        return data

#.............
# PayrollRun

class PayrollRunSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(read_only=True)
    executed_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = PayrollRun
        fields = "__all__"

class PayrollRunUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollRun
        fields = "__all__"
        read_only_fields = ['year','month','executed_by','run_date']

