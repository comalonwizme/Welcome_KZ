from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, Profile, Tour, Booking
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 150)
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length = 6,
        write_only = True,
        validators = [validate_password]
    )

    phone_number = serializers.CharField(max_length = 20)

    role = serializers.ChoiceField(
        choices=Profile.ROLES_CHOICES,
        default = 'tourist',
    )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Уже существует аккаунт с таким email!")
        return value
    
    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                username = validated_data['username'],
                email = validated_data['email'],
                password = validated_data['password']
            )

            Profile.objects.create(
                user = user,
                phone_number = validated_data['phone_number'],
                role = validated_data['role']
            )
        return user
    

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['rating', 'is_verified', 'created_at']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['rating', 'role']


class TourSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source = "company.name")
    guide_name = serializers.ReadOnlyField(source = "guide.user.username")
    class Meta:
        model = Tour
        fields = "__all__"
        read_only_fields = ['is_active', 'company', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    tour_title = serializers.ReadOnlyField(source = 'tour.title')
    tour_location = serializers.ReadOnlyField(source = 'tour.location')
    username = serializers.ReadOnlyField(source = 'user.username')

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ['username', 'created_at', 'status']

    def validate_rating(self, value):
        if self.instance and self.instance.status != 'completed':
            raise serializers.ValidationError("Можете оценить только после завершения тура")
        return value