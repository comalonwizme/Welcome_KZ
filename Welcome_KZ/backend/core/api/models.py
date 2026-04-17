from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_company')
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    ROLES_CHOICES = [
        ('tourist', 'Tourist'),
        ('guide', 'Guide'),
        ('owner', 'Company Owner'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES_CHOICES, default='tourist')
    phone_number = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)

    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='guides')
    rating = models.FloatField(default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class EmploymentRequest(models.Model):
    STATUS_CH = [
        ('pending', 'Pending'),
        ("accepted", "Accepted"),
        ('rejected', "Rejected"),
    ]

    guide = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job application")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='recieved application')
    status = models.CharField(max_length=10, choices=STATUS_CH, default='pending')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guide.username} -> {self.company.name} ({self.status})"