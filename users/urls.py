from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.user_register),
    path('<int:pk>/', views.user_detail),
    path('friend/', views.friend_view),
    path('history/', views.history_view),
]
