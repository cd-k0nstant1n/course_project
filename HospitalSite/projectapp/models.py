from django.db import models
from django.contrib.auth.models import User
    
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  blank=True, null=True)
    phone = models.CharField(max_length=13)
    date_of_birth = models.DateField(null=True, blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    ]
    role = models.CharField(max_length=7, choices=ROLE_CHOICES)
    def save(self, *args, **kwargs):
        # Create a User instance if it doesn't exist
        if not self.user_id:
            self.user = User.objects.create(username='default_username')
            self.user.save()
        super().save(*args, **kwargs)














































#     def save(self, *args, **kwargs):
#         # Only hash the password if it's not already hashed
#         if not self.password.startswith('$2'):
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)
    
#     def check_password(self, raw_password):
#         # Manually check the hashed password
#         return django_check_password(raw_password, self.password)



# class Code(models.Model):
#     code = models.CharField(max_length=1000)

# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from .backends import UserManager

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     fname = models.CharField(max_length=150)
#     lname = models.CharField(max_length=150)
#     phone = models.CharField(max_length=13)
#     date_of_birth = models.DateField(null=True, blank=True)
#     specialty = models.CharField(max_length=100, null=True, blank=True)
#     role = models.CharField(max_length=7)
#     password = models.CharField(max_length=500, null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     @property
#     def __str__(self):
#         return self.email