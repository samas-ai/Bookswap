# core/urls.py
from django.contrib import admin
from django.urls import path, include
# Importa as views do Simple JWT para obtenção e renovação de tokens.
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # Rota do admin
    path('admin/', admin.site.urls),

    # Rota para a API v1 do app user
    path('api/v1/', include('user.api.v1.router')),
    
    # Rota teste para autenticação do usuário
    path('api/v1/', include('user.urls')),

    # Rota para obter tokens JWT
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Rota para renovação dos tokens JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
