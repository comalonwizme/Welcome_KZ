from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tourist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    email_address = models.EmailField()
    profile_image = models.ImageField()
    birth_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    gender_party = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=gender_party, null=True, blank=True)

    def __str__(self):
        return f"Name: {self.name}\nSurname: {self.surname}"