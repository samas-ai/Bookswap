from rest_framework import serializers
from user.models import Book, User, Trade, Trade

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'full_name')

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'published_date', 'isbn', 'owner')


class TradeSerializer(serializers.ModelSerializer):
    proposer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    proposer_book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    receiver_book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Trade
        fields = ('id', 'proposer', 'receiver', 'proposer_book', 'receiver_book', 'status', 'created_at', 'updated_at')
        read_only_fields = ('status', 'created_at', 'updated_at')

    def validate(self, data):
        """
        Check that the proposer is the owner of the proposer_book
        and the receiver is the owner of the receiver_book.
        """
        if data['proposer_book'].owner != data['proposer']:
            raise serializers.ValidationError("Você só pode propor trocas com livros que você possui.")
        if data['receiver_book'].owner != data['receiver']:
            raise serializers.ValidationError("O livro do destinatário não pertence a ele.")
        if data['proposer'] == data['receiver']:
            raise serializers.ValidationError("Você não pode trocar livros com você mesmo.")
        return data