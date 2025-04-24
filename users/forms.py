from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_confirm_password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'height', 'weight', 'fitness_goal', 'profile_picture']
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and not (18 <= age <= 100):
            raise forms.ValidationError("Age must be between 18 and 100.")
        return age

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('height')
        weight = cleaned_data.get('weight')
        
        if height and weight:
            # Optional validation: check if height and weight are within reasonable limits
            if height < 50 or height > 250:
                self.add_error('height', "Height must be between 50 cm and 250 cm.")
            if weight < 10 or weight > 300:
                self.add_error('weight', "Weight must be between 10 kg and 300 kg.")
        
        return cleaned_data