from django.urls import path

from ranker.core import views

urlpatterns = [
    path('players/all', views.PlayerList.as_view()),
    path('players/leaderboard', views.LeaderBoard.as_view()),
    path('player/details/<int:player_id>', views.PlayerDetail.as_view()),
    path('player/stats/<int:player_id>', views.PlayerStats.as_view()),
    path('history/rating/<int:player_id>', views.PlayerRatingHistory.as_view()),
    path('history/match/<int:player_id>', views.PlayerMatchHistory.as_view())
]
