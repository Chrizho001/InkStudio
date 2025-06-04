from django.urls import path
from tattoo_shop import views

urlpatterns = [
    path(
        "booking/",
        views.BookingListCreateView.as_view(),
        name="Booking list and create view",
    ),
]
