from django.contrib import admin
from .models import Book
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'id')

    list_filter = ('author', 'publication_year')

    search_fields = ('title', 'author')

    list_display_links = ('title', 'author')

admin.site.register(Book, BookAdmin)