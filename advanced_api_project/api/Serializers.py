from rest_framework import serializers
from .models import Author, Book
from datetime import date

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year']
    
    def validate(self, attrs):
        current_year = date.today().year
        if attrs.get('publication_year') and attrs['publication_year'] > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return super().validate(attrs)