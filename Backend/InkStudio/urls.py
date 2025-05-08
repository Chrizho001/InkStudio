from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),  # Djoser endpoints
    path('auth/', include('djoser.urls.jwt')),  # JWT endpoints
    path('ink_studio/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get JWT
    path('ink_studio/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT
]