from rest_framework import serializers
from .models import Artist, Booking, Gallery
from django.db.models import Q


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "name", "email", "bio", "profile_image"]


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            "id",
            "session_date",
            "start_time",
            "end_time",
            "status",
            "tattoo_description",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def validate(self, data):
        user = self.context.get('user')
        session_date = data["session_date"]
        start_time = data["start_time"]
        end_time = data["end_time"]

        if start_time >= end_time:
            raise serializers.ValidationError("Start time must be before end time.")

        # Check if there already exists a booking at that particular time and date
        overlapping_booking = Booking.objects.filter(
            session_date=session_date,
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).exists()

        if overlapping_booking:
            raise serializers.ValidationError("This time slot has already been taken.")

        # prevent the user from creating double bookings
        user_overlap = Booking.objects.filter(
            user=user,
            session_date=session_date,
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).exists()

        if user_overlap:
            raise serializers.ValidationError(
                "You already have a booking during this time."
            )

        return data


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["id", "image_url", "slug", "title", "description", "style", "uploaded_at"]
        read_only_fields = ['slug', 'uploaded_at']
