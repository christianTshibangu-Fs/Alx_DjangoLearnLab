from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home_page, name='home'), # Home page route
    # You can add more blog-related routes here
    path('register/', views.register, name='register'), # Registration route
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'), # Login route
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), # Logout route
    path('profile/', views.profile_view, name='profile'), # User profile route   

]