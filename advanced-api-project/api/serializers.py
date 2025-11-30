from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date']

    def validate(self, attrs):
        if 'published_date' in attrs:
            if attrs['published_date'] > datetime.date.today():
                raise serializers.ValidationError("Publication date cannot be in the future.")
        return super().validate(attrs)
