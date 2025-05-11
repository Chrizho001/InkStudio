from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ink_studio/', include('tattoo_shop.urls')),
    path('auth/', include('djoser.urls')),  # Djoser endpoints
    path('auth/', include('djoser.urls.jwt')),  # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT
]