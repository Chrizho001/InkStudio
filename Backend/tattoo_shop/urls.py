from django.urls import path
from tattoo_shop import views

urlpatterns = [
    path("gallery", views.GalleryListView.as_view(), name="Gallery list view"),
    path(
        "gallery/<slug:slug>",
        views.GalleryListView.as_view(),
        name="Gallery detail view",
    ),
    path("artist", views.ArtistListView.as_view(), name="artist list view"),
    path("artist/<str:id>", views.ArtistDetailView.as_view(), name="artist list view"),
    path(
        "booking/",
        views.BookingListCreateView.as_view(),
        name="Booking list and create view",
    ),
]
