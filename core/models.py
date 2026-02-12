from django.db import models



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
