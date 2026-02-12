from django.shortcuts import render
from rest_framework import generics
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated
from .utils import booking_confirmation
from rest_framework.throttling import ScopedRateThrottle

# Create your views here.


class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = "bookings"

    def get_queryset(self):
        return (
            Booking.objects.select_related("user")
            .filter(user=self.request.user)
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        user = self.request.user
        user_email = self.request.user.email
        booking_confirmation(user, user_email, booking)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Pass the logged-in user as context
        context["user"] = self.request.user
        return context
