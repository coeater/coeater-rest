from django.urls import path
from match import views

urlpatterns = [
    path('invitation/', views.invitation_view),
    path('invitation/<int:pk>/', views.invitation_detail),
    path('invited/', views.invited_view),
]
