from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post, Comment

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # L'auteur est automatiquement défini dans la vue
        fields = ['title', 'content', 'tags']  # Étape 2: Ajout du champ 'tags' au formulaire

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

