
from django.urls import path
from .views import test_authenticated_view

# Criei uma URL test para verificar a autenticação do usuário. 
urlpatterns = [
    path('test-auth/', test_authenticated_view, name='test_auth_view'),
]