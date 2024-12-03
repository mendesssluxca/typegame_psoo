from django.urls import path
from .views import save_score, get_leaderboard

urlpatterns = [
    path('save_score/', save_score, name='save_score'),
    path('get_leaderboard/', get_leaderboard, name='get_leaderboard'),
]
