from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ranker.core.models import (
    Player, Event, RatingHistory
)
from ranker.core.serializers import (
    PlayerSerializer,
    EventSerializer,
    RatingHistorySerializer,
    MatchHistorySerializer
)
from ranker.core.utils import data

N_LAST_MATCHES = 10
N_PLAYERS = 5
N_DAYS_STATS_MAIN = 7
LB_CACHE_MINUTES = 1


class LeaderBoard(APIView):
    """
    Get data for leaderboard. Data is cached for LB_CACHE_MINUTES
    minutes. Set it to 0 if you dont need any caching
    """
    @method_decorator(cache_page(LB_CACHE_MINUTES * 60, cache='leaderboard', key_prefix=''))
    def get(self, request):
        leaders = data.get_leaders(n_players=N_PLAYERS, rating_trend_days=N_DAYS_STATS_MAIN)
        changes = data.get_changes_in_time(n_players=N_PLAYERS, n_days=N_DAYS_STATS_MAIN)
        maxes = data.get_maxes()
        totals = data.get_totals()

        return Response({
            'leaders': leaders,
            'weekly': changes,
            'maxes': maxes,
            'totals': totals
        })


class PlayerList(APIView):
    """
    List of all players
    """
    def get(self, request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)


class PlayerDetail(APIView):
    """
    Player data
    """
    def get(self, request, player_id):
        try:
            player = Player.objects.get(pk=player_id)
            serializer = PlayerSerializer(player)
            response = Response(serializer.data)
        except Player.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
        return response


class PlayerRatingHistory(APIView):
    """
    Player history rating for charts
    """
    def get(self, request, player_id):
        history = RatingHistory.objects.filter(player_id=player_id).order_by('date')
        serializer = RatingHistorySerializer(history, many=True)
        return Response(serializer.data)


class PlayerMatchHistory(APIView):
    """
    Player match history
    """
    def get(self, request, player_id):
        summary = data.get_last_matches(player_id, N_LAST_MATCHES)
        serializer = MatchHistorySerializer(summary, many=True)
        return Response(serializer.data)


class PlayerStats(APIView):
    """
    Simple player statistics
    """
    def get(self, request, player_id):
        stats = data.get_player_stats(player_id)
        return Response(stats)


class EventList(APIView):
    """
    List of all events
    """
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventDetail(APIView):
    """
    Detailed event information
    """
    def get(self, response, event_id):
        try:
            event_details = data.get_event_details(event_id)
            response = Response(event_details)
        except Event.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
        return response
