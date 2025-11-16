from django  import forms
from .models import Book

class ExempleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn_number', 'pages', 'cover', 'language'] 
