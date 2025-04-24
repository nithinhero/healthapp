from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    fitness_goal = models.CharField(max_length=255, blank=True, default="General Fitness")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Optional: Add a field to track step count or other fitness metrics
    step_count = models.PositiveIntegerField(default=0)  # For tracking steps or fitness progress
    
    def __str__(self):
        return self.user.username

    # Optional: Add custom clean methods or validation logic
    def clean(self):
        # Ensure that the age is reasonable (e.g., 18-100)
        if self.age and not (18 <= self.age <= 100):
            raise ValidationError("Age must be between 18 and 100.")
        # You can add more custom validation or processing logic here.


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name} ({self.email})'
