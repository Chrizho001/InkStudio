import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


# Create your models here.


# Extending the Abstract user class which already comes with a typical user fields to avoid building from scratch
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    


    # Required for AbstractUser: specify fields for username and email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
        ]
        db_table = "users"  # Match your schema's table name

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_image = models.URLField(blank=False)

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bookings")
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="bookings"
    )
    session_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    tattoo_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["artist", "session_date", "start_time"]),
            models.Index(fields=["user"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F("start_time")),
                name="end_time_after_start_time",
            ),
        ]

    def __str__(self):
        return f"Booking {self.id} for {self.user} with {self.artist}"


class ArtistAvailability(models.Model):
    id = models.BigAutoField(primary_key=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="availabilities"
    )
    session_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["artist", "session_date", "start_time"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "session_date", "start_time"],
                name="unique_availability_slot",
            ),
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F("start_time")),
                name="availability_end_time_after_start_time",
            ),
        ]

    def __str__(self):
        return f"Availability for {self.artist} on {self.session_date} at {self.start_time}"


class Gallery(models.Model):
    id = models.BigAutoField(primary_key=True)
    image_url = models.URLField(blank=False)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    style = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["title", "uploaded_at"]),
            models.Index(fields=["style"]),
        ]

    def __str__(self):
        return f"{self.title }"
