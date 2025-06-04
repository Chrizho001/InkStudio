from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, time, timedelta
from tattoo_shop.models import User, Booking

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class BookingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="client@example.com",
            password="password",
            first_name="Client",
            last_name="User"
        )

    def test_create_valid_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            session_date=date.today(),
            start_time=time(10, 0),
            end_time=time(11, 0),
            tattoo_description="A cool dragon tattoo"
        )
        self.assertEqual(booking.status, "pending")
        self.assertEqual(booking.user.email, "client@example.com")
        self.assertEqual(str(booking), f"Booking {booking.id} for {self.user}")

    def test_booking_end_time_must_be_after_start_time(self):
        booking = Booking(
            user=self.user,
            session_date=date.today(),
            start_time=time(12, 0),
            end_time=time(11, 0),
            tattoo_description="Invalid time booking"
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()  # This triggers model validation including constraints

    def test_status_choices(self):
        for status, _ in Booking.STATUS_CHOICES:
            booking = Booking(
                user=self.user,
                session_date=date.today(),
                start_time=time(9, 0),
                end_time=time(10, 0),
                status=status
            )
            booking.full_clean()  # Should not raise

    def test_end_time_can_be_blank(self):
        booking = Booking.objects.create(
            user=self.user,
            session_date=date.today(),
            start_time=time(9, 0),
            tattoo_description="No end time yet"
        )
        self.assertIsNone(booking.end_time)
