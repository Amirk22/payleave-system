from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    ROLE_CHOICES = (
        ('EMPLOYEE', 'Employee'),
        ('MANAGER', 'Manager'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    monthly_salary = models.PositiveIntegerField(default=0)
    working_hours = models.PositiveIntegerField(default=8)
    manager = models.ForeignKey('self',null=True,blank=True,
        on_delete=models.SET_NULL,
        related_name='subordinates'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_leaves'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.employee}'


class OvertimeLog(models.Model):
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='overtime_logs'
    )

    date = models.DateField()
    overtime_minutes = models.PositiveIntegerField()

    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f'{self.employee} - {self.date}'



class PayrollRun(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(12),])

    executed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='payroll_runs'
    )

    run_date = models.DateTimeField(auto_now_add=True)
    is_finalized = models.BooleanField(default=False)

    class Meta:
        unique_together = ('year', 'month')

    def __str__(self):
        return f'Payroll {self.year}-{self.month}'


class PayrollRecord(models.Model):
    payroll_run = models.ForeignKey(
        PayrollRun,
        on_delete=models.CASCADE,
        related_name='records'
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payroll_records'
    )

    base_salary = models.PositiveIntegerField(validators=[MinValueValidator(2000), MaxValueValidator(10000)])

    unpaid_leave_days = models.PositiveIntegerField(default=0)
    unpaid_leave_deduction = models.PositiveIntegerField(default=0)

    overtime_hours = models.PositiveIntegerField(default=0)
    overtime_amount = models.PositiveIntegerField(default=0)

    final_salary = models.PositiveIntegerField()

    class Meta:
        unique_together = ('payroll_run', 'employee')

    def __str__(self):
        return f'{self.employee} - {self.final_salary}'