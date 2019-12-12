
from rest_framework import serializers

from ranker.core.models import Player, Match, RatingHistory


class PlayerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    rating = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    class Meta:
        model = Player
        fields = '__all__'


class RatingHistorySerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    class Meta:
        model = RatingHistory
        exclude = ['id', 'player']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class MatchHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    event_date = serializers.DateField()
    delta = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    event_short_name = serializers.CharField(max_length=30)
    opponent_name = serializers.CharField(max_length=80)
    rating = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    opponent_rating = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    score = serializers.CharField(max_length=5)
    result = serializers.IntegerField()
