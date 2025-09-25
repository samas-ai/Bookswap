from rest_framework import serializers
from user.models import Book, User, Trade

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

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