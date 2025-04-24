from django.contrib import admin
from .models import UserProfile
from .models import ContactMessage
admin.site.register(UserProfile)
admin.site.register(ContactMessage)
