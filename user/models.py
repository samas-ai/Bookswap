from django.db import models
from django.contrib.auth.models import AbstractUser
from core.base_model import BaseModel
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):  # type: ignore[override]
        return self.username

class Book(BaseModel):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class Trade(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('accepted', 'Aceita'),
        ('rejected', 'Rejeitada'),
        ('cancelled', 'Cancelada'),
    )

    proposer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proposed_trades')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_trades')
    proposer_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='trades_as_proposer_book')
    receiver_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='trades_as_receiver_book')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Troca de {self.proposer_book.title} por {self.receiver_book.title} entre {self.proposer.username} e {self.receiver.username}"

    class Meta:
        verbose_name = 'Troca'
        verbose_name_plural = 'Trocas'
