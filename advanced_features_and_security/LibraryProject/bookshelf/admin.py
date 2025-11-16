from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Book
# Register your models here.

# Définition de l'interface Admin pour le CustomUser
class CustomUserAdmin(UserAdmin):
    # Champs affichés dans la liste des utilisateurs
    list_display = ('email', 'username', 'date_of_birth', 'is_staff', 'is_active')
    
    # Définit les champs pour la modification d'un utilisateur existant
    fieldsets = UserAdmin.fieldsets + (
        (
            'Informations Personnelles Supplémentaires', 
            {'fields': ('date_of_birth', 'profile_photo')}
        ),
    )
    
    # Définit les champs pour la création d'un nouvel utilisateur dans l'Admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Informations Personnelles Supplémentaires', 
            {'fields': ('date_of_birth', 'profile_photo',)}
        ),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)

# Enregistrement du CustomUser avec notre CustomUserAdmin personnalisé
admin.site.register(CustomUser, CustomUserAdmin)

# Définition de l'interface Admin pour le modèle Book
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'id')

    list_filter = ('author', 'publication_year')

    search_fields = ('title', 'author')

    list_display_links = ('title', 'author')

admin.site.register(Book, BookAdmin)