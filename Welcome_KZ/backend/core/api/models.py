from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

class CompanyManager(models.Manager):
    def verified(self):
        return self.filter(is_verified=True)
    
    def top_rated(self):
        return self.filter(is_verified=True).order_by('-rating')
    

class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_company')
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    objects = CompanyManager()


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

    guide = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_application")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='recieved_application')
    status = models.CharField(max_length=10, choices=STATUS_CH, default='pending')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guide.username} -> {self.company.name} ({self.status})"
    

class Tour(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='tours')
    guide = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tours')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    max_partipicant = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Booking(models.Model):
    STATUS_CH = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', "Cancelled"),
        ("completed", "Completed")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(choices=STATUS_CH, max_length=20, default='pending')
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"
