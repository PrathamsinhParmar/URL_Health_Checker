from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('urls/add/', views.add_url, name='url_add'),
    path('urls/<int:pk>/edit/', views.edit_url, name='url_edit'),
    path('urls/<int:pk>/delete/', views.delete_url, name='url_delete'),
    path('urls/<int:pk>/', views.url_detail, name='url_detail'),
    path('profile/', views.profile, name='profile'),
    path('accounts/register/', views.register, name='register'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms_of_service, name='terms'),
    path('contact/', views.contact_us, name='contact'),
    path('api-docs/', views.api_docs, name='api_docs'),
    path('integration-guide/', views.integration_guide, name='integration_guide'),
    path('public-status/', views.public_status, name='public_status'),
]
