from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.http import JsonResponse

from users.views.auth_view import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    CustomTokenBlacklistView,
)

def api_root(request):
    return JsonResponse({
        'message': 'Welcome to Severstal-test API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'health': '/api/health/',
        }
    })

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'severstal-test-api'
    })

urlpatterns = [
    # ---------- API документация ----------
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/health/', health_check, name='health-check'),

    # ---------- Auth (JWT) ----------
    path('token/jwt/', CustomTokenObtainPairView.as_view(), name='auth-jwt-create'),
    path('token/jwt/refresh/', CustomTokenRefreshView.as_view(), name='auth-jwt-refresh'),
    path('token/jwt/verify/', CustomTokenVerifyView.as_view(), name='auth-jwt-verify'),
    path('token/jwt/blacklist/', CustomTokenBlacklistView.as_view(), name='auth-jwt-blacklist'),

    # ---------- app urls ----------
    path('api/v1/', include([
        path('', include('users.urls')),
    ])),

]