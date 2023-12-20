from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
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
