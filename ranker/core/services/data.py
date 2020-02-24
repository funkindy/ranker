import datetime

import pandas as pd

from django.db.models import IntegerField, CharField, F, Value
from django.db.models.functions import Concat, Cast
from django.utils import timezone
from django.utils.translation import gettext as _

from ranker.core.models import Player, Match, RatingHistory

VALUE_WIN = 1
VALUE_LOSE = 0


def get_last_matches(*, player_id: int, n_matches: int) -> Match:

    wins = Match.objects.filter(winner_id=player_id).values(
        'id', 'event_date', 'delta',
        event_short_name=F('event__short_name'),
        opponent_name=Concat('loser__first_name', Value(' '), 'loser__last_name'),
        rating=F('winner_rating'),
        opponent_rating=F('loser_rating'),
        result=Value(VALUE_WIN, IntegerField()),
        score=Concat(
            Cast('winner_score', CharField()),
            Value(' - '),
            Cast('loser_score', CharField())
        )
    )

    losses = Match.objects.filter(loser_id=player_id).values(
        'id', 'event_date', 'delta',
        event_short_name=F('event__short_name'),
        opponent_name=Concat('winner__first_name', Value(' '), 'winner__last_name'),
        rating=F('loser_rating'),
        opponent_rating=F('winner_rating'),
        result=Value(VALUE_LOSE, IntegerField()),
        score=Concat(
            Cast('loser_score', CharField()),
            Value(' - '),
            Cast('winner_score', CharField())
        )
    )
    summary = wins.union(losses).order_by('-id')[:n_matches]
    return summary


def get_player_stats(*, player_id: int) -> dict:

    stats = {}

    wins = Match.objects.filter(winner_id=player_id)
    losses = Match.objects.filter(loser_id=player_id)

    best_rating = (
        RatingHistory
        .objects
        .filter(player_id=player_id)
        .order_by('-rating')
        .values('rating', 'date')
        .first()
    )

    stats['win_count'] = wins.count()
    stats['lose_count'] = losses.count()
    stats['total_games'] = stats['win_count'] + stats['lose_count']
    stats['best_rating'] = best_rating

    # TODO: best/worst opponent, events frequency,
    # achievemets (medal places) and more

    return stats


def get_changes_in_time(*, n_players: int = 5, n_days: int = 7, fmt: str = "%Y-%m-%d") -> dict:
    """
    POSTGRESQL ONLY: Raw query to get rating deltas in time back vs current.
    default is one week.

    For other backends there are more convinient ORM ways to get this

    returns n_players best and n_players worst deltas

    TODO: put this to ORM level
    """
    up_to_date = (timezone.now() - timezone.timedelta(days=n_days)).strftime(fmt)

    qs = RatingHistory.objects.raw(
        f"""
            SELECT
                p1.id,
                p1.player_id,
                p3.last_name || ' ' || p3.first_name as full_name,
                p3.rating - p1.rating as rating_delta
            FROM ratinghistory p1, (
                SELECT player_id, MAX(date) AS max_date
                FROM ratinghistory
                WHERE  date <= '{up_to_date}'::date
                GROUP BY player_id
            ) AS p2, player as p3
            WHERE p1.date <= '{up_to_date}'::date
            AND p1.player_id = p2.player_id
            AND p1.player_id = p3.id
            AND p1.date = p2.max_date
            ORDER BY rating_delta DESC
        """
    )

    items = [
        {
            'id': i.player_id,
            'name': i.full_name,
            'value': i.rating_delta
        }
        for i in qs
    ]

    return {
        'best': items[:n_players],
        'worst': reversed(items[-n_players:])
    }


def get_leaders(*, n_players: int = 5, rating_trend_days: int = 7) -> list:
    """
    TODO: put this to ORM level (PostgreSQL Window Functions)
    """
    leaders = Player.objects.order_by('-rating')[:n_players]

    leaders_ratings = (
        RatingHistory
        .objects
        .filter(player_id__in=leaders)
        .order_by('player_id', '-date')
        .values()
    )

    result = []

    if leaders_ratings:
        latest_leader_ratings = (
            pd.DataFrame(leaders_ratings)
            .groupby('player_id')['rating']
            .apply(lambda x: list(x.head(rating_trend_days))[::-1])
            .to_dict()
        )

        # Combining Users with their latest ratings
        for leader in leaders:

            leader_dict = {
                'id': leader.id,
                'name': leader.full_name,
                'rating': leader.rating,
                'city': leader.city,
                'rating_trend': latest_leader_ratings.get(leader.id, [])
            }

            result.append(leader_dict)

    return result


def get_maxes() -> dict:

    if not Match.objects.exists():
        return dict()

    matches = pd.DataFrame(Match.objects.values('winner_id', 'loser_id'))
    ratings = pd.DataFrame(Player.objects.values('id', 'rating'))

    wins = matches.groupby('winner_id').size()
    losses = matches.groupby('loser_id').size()
    ratings = ratings.set_index('id')['rating'] - Player.INITIAL_RATING_SCORE
    total = wins + losses

    metrics = [
        ('games', wins + losses),
        ('winrate', wins / total),
        ('efficiency', ratings / total)
    ]

    result = {}

    for metric, data in metrics:
        idx = data.idxmax()
        result[metric] = [{
            'id': idx,
            'name': Player.objects.get(pk=idx).full_name,
            'value': data[idx]
        }]

    return result


def get_totals() -> list:

    players = Player.objects.count()
    matches = Match.objects.count()

    totals = [
        {'id': 'players', 'name': _('Total Matches'), 'value': matches},
        {'id': 'matches', 'name': _('Total Players'), 'value': players}
    ]

    return totals


def get_event_details(*, event_id: int, days: int = 365, n_events: int = 5) -> dict:

    all_matches = (
        Match.objects
        .select_related('winner')
        .select_related('loser')
        .filter(event_id=event_id)
    )

    start_date = timezone.now() - datetime.timedelta(days=days)

    matches = (
        all_matches
        .filter(event_date__gte=start_date)
        .order_by('-event_date', 'id')
    )

    # Get recent events, their stats and winners
    places = {}

    for match in matches:

        if match.event_phase is None:
            continue

        places.setdefault(match.event_date, [])

        places[match.event_date].append({
            'id': match.winner_id,
            'place': match.event_phase,
            'name': match.winner.full_name,
            'rating': match.winner_rating
        })

        if match.event_phase < 3:  # We dont need loser of third place match in the leaderboard
            places[match.event_date].append({
                'id': match.loser_id,
                'place': match.event_phase + 1,  # +1 as it lost
                'name': match.loser.full_name,
                'rating': match.loser_rating
            })

    # Sorting by place
    for date, meta in places.items():
        places[date] = sorted(meta, key=lambda k: k['place'])

    # Getting only last n_events events
    # +1 for the last place player (as he loses all the matches)
    recent_events = (
        pd.DataFrame(matches.values())
        .groupby('event_date')
        .agg(
            players_count=('winner_id', lambda x: x.nunique() + 1),
            avg_rating=('winner_rating', 'mean')
        )
        .sort_index(ascending=False)
        .head(n_events)
    )
    recent_events['places'] = recent_events.index.map(places)

    # Overall event statistics
    total_events = all_matches.values('event_date').distinct().count()
    avg_rating = recent_events.avg_rating.mean()
    avg_players = recent_events.players_count.mean()

    return {
        'event_id': event_id,
        'total_events': total_events,
        'avg_rating': avg_rating,
        'avg_players': avg_players,
        'recent': recent_events.reset_index().to_dict(orient='records')
    }
