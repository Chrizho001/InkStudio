from django.shortcuts import render
from rest_framework import generics
from .models import Artist, Gallery, Booking
from .serializers import ArtistSerializer, GallerySerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class ArtistListView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ArtistsDetailView(generics.RetrieveAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    lookup_field = "id"


class GalleryListView(generics.ListAPIView):
    queryset = Gallery.objects.all().order_by("-uploaded_at")
    serializer_class = GallerySerializer


class GalleryDetailView(generics.RetrieveAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    lookup_field = "slug"


class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Booking.objects.select_related("user", "artist")
            .filter(user=self.request.user)
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Pass the logged-in user as context
        context["user"] = self.request.user
        return context
