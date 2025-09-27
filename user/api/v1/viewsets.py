from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from user.models import User, Book, Trade
from user.api.v1.serializers import BookSerializer, UserSerializer, TradeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

    def get_queryset(self):
        
        queryset = self.queryset
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(models.Q(proposer=user) | models.Q(receiver=user))
        return queryset

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        trade = self.get_object()
        if trade.receiver != request.user:
            return Response({'status': 'Apenas o destinatário pode aceitar a troca.'}, status=status.HTTP_403_FORBIDDEN)
        if trade.status != 'pending':
            return Response({'status': f'A troca não pode ser aceita pois está com o status "{trade.get_status_display()}".'}, status=status.HTTP_400_BAD_REQUEST)

        # Swap books
        proposer_book = trade.proposer_book
        receiver_book = trade.receiver_book
        proposer_book.owner, receiver_book.owner = receiver_book.owner, proposer_book.owner
        proposer_book.save()
        receiver_book.save()

        trade.status = 'accepted'
        trade.save()
        return Response({'status': 'Troca aceita e livros trocados.'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        trade = self.get_object()
        if trade.receiver != request.user:
            return Response({'status': 'Apenas o destinatário pode rejeitar a troca.'}, status=status.HTTP_403_FORBIDDEN)
        if trade.status != 'pending':
            return Response({'status': f'A troca não pode ser rejeitada pois está com o status "{trade.get_status_display()}".'}, status=status.HTTP_400_BAD_REQUEST)

        trade.status = 'rejected'
        trade.save()
        return Response({'status': 'Troca rejeitada.'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        trade = self.get_object()
        if trade.proposer != request.user:
            return Response({'status': 'Apenas o proponente pode cancelar a troca.'}, status=status.HTTP_403_FORBIDDEN)
        if trade.status != 'pending':
            return Response({'status': f'A troca não pode ser cancelada pois está com o status "{trade.get_status_display()}".'}, status=status.HTTP_400_BAD_REQUEST)

        trade.status = 'cancelled'
        trade.save()
        return Response({'status': 'Troca cancelada.'})