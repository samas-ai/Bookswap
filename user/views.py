from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_authenticated_view(request):
    """
    View de teste para verificar a autenticação JWT.
    """
    return Response({"message": "Você está autenticado!"})