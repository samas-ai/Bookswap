from django.db import models
from core.base_model import BaseModel

class User(BaseModel):
    # Campos base de usúario
    username = models.CharField(max_length=18, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=150, blank=True, null=True)

    # flags de permissão
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Book(BaseModel):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class Trade(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('accepted', 'Aceita'),
        ('rejected', 'Rejeitada'),
        ('cancelled', 'Cancelada'),
    )

    proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposed_trades')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_trades')
    proposer_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='trades_as_proposer_book')
    receiver_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='trades_as_receiver_book')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Troca de {self.proposer_book.title} por {self.receiver_book.title} entre {self.proposer.username} e {self.receiver.username}"

    class Meta:
        verbose_name = 'Troca'
        verbose_name_plural = 'Trocas'
