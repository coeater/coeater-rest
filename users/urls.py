from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.user_register),
    path('<int:pk>/', views.user_detail),
    path('<int:pk>/friend/', views.user_friend),
    path('<int:pk>/history/', views.user_history),
    path('friend/', views.friend_view),
    path('history/', views.history_view),
]
