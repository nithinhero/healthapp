# meals/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Meal
from notifications.models import Notification
from django.conf import settings

@receiver(post_save, sender=Meal)
def meallog_post_save(sender, instance, created, **kwargs):
    """
    Sends a notification when a new meal is added or an existing meal is updated.
    Also sends an email notification when a new meal is added.
    """
    if created:
        # Meal added - Create notification
        Notification.objects.create(
            user=instance.user,
            message=f"🍽️ You added a new meal: {instance.food_name} with {instance.total_calories} kcal"
        )

        # Send email to the user notifying about the new meal
        send_mail(
            subject=f"New Meal Added: {instance.food_name}",
            message=f"Hello {instance.user.username},\n\nYou have successfully added a new meal:\n\nFood: {instance.food_name}\nCalories: {instance.total_calories} kcal\n\nThank you for using our app!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
        )
    else:
        # Meal updated - Create notification
        Notification.objects.create(
            user=instance.user,
            message=f"🔥 Calories updated for: {instance.food_name} → {instance.total_calories} kcal"
        )
