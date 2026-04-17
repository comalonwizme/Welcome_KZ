from django.contrib import admin
from .models import Company, Profile, EmploymentRequest, Tour, Booking
# Register your models here.

admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(EmploymentRequest)
admin.site.register(Tour)
admin.site.register(Booking)