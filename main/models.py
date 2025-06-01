from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("user", "User"),
        ("manager", "Manager"),
        ("admin", "Admin"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()
    photo_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.CharField(max_length=255, blank=True, null=True)
    description_long = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "events"


class Registration(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="registrations"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")
        db_table = "registrations"


class Feedback(models.Model):
    STATUS_CHOICES = [
        ("в ожидании", "В ожидании"),
        ("рассмотрено", "Рассмотрено"),
    ]

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="в ожидании"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"

    class Meta:
        db_table = "feedback"
