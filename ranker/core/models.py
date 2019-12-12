from django.db import models, transaction

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from ranker.core.utils import rating

DEFAULT_COEF = 0.6


class User(AbstractUser):
    phone = models.CharField(
        verbose_name=_('phone number'), max_length=40, null=True, blank=True
    )

    class Meta:
        db_table = 'user'


class Player(models.Model):
    INITIAL_RATING_SCORE = 350
    RIGHT_HAND = 'R'
    LEFT_HAND = 'L'

    MAIN_HAND_CHOICES = [
        (RIGHT_HAND, 'Right'),
        (LEFT_HAND, 'Left')
    ]

    first_name = models.CharField(verbose_name=_('first Name'), max_length=20, null=False)
    last_name = models.CharField(verbose_name=_('last name'), max_length=20, null=False)
    username = models.CharField(verbose_name=_('username'), max_length=20, unique=True)
    date_of_birth = models.DateField(verbose_name=_('date of birth'), null=False)
    city = models.CharField(verbose_name=_('city'), max_length=20, null=False)
    hand = models.CharField(max_length=1, choices=MAIN_HAND_CHOICES, default=RIGHT_HAND)
    equipment = models.TextField(verbose_name=_('equipment'))
    rating = models.FloatField(null=False, default=INITIAL_RATING_SCORE)

    @property
    def full_name(self):
        return '{0} {1}'.format(self.last_name, self.first_name)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'player'
        verbose_name = _('player')
        verbose_name_plural = _('players')


class Event(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=255, null=False)
    short_name = models.CharField(verbose_name=_('short name'), max_length=30, null=False)
    address = models.CharField(verbose_name=_('address'), max_length=255, null=False)
    coefficient = models.FloatField(
        verbose_name=_('rating coefficient'), null=False, default=DEFAULT_COEF
    )

    def __str__(self):
        return '{0}, {1}: {2}'.format(
            self.name,
            _('coef'),
            self.coefficient
        )

    class Meta:
        db_table = 'event'
        verbose_name = _('event')
        verbose_name_plural = _('events')


class Match(models.Model):
    event = models.ForeignKey(
        'Event',
        verbose_name=_('event'),
        null=False,
        on_delete=models.CASCADE
    )
    event_date = models.DateField(verbose_name=_('event date'), null=False)
    winner = models.ForeignKey(
        'Player',
        db_index=True,
        verbose_name=_('winner'),
        null=False,
        on_delete=models.CASCADE,
        related_name='winner'
    )
    loser = models.ForeignKey(
        'Player',
        db_index=True,
        verbose_name=_('loser'),
        null=False,
        on_delete=models.CASCADE,
        related_name='loser'
    )
    winner_score = models.PositiveSmallIntegerField(
        verbose_name=_('winner score'), null=False
    )
    loser_score = models.PositiveSmallIntegerField(
        verbose_name=_('loser score'), null=False
    )
    winner_rating = models.FloatField(verbose_name=_('winner rating'))
    loser_rating = models.FloatField(verbose_name=_('loser rating'))
    delta = models.FloatField(verbose_name=_('rating delta'))

    is_technical = models.BooleanField(
        verbose_name=_('technical result'), null=False, default=False
    )

    def save(self, *args, **kwargs):
        with transaction.atomic():

            # Get new rating values and delta
            new_winner_rating, new_loser_rating, delta = rating.calculate_new_rating(
                self.winner.rating, self.loser.rating, self.event.coefficient
            )

            # Updating cache fields for match statistics and save match
            self.winner_rating = self.winner.rating
            self.loser_rating = self.loser.rating
            self.delta = delta

            super().save(*args, **kwargs)

            # Updating actual ratings and history to date for each player
            self.winner.rating = new_winner_rating
            self.winner.save()

            self.loser.rating = new_loser_rating
            self.loser.save()

            RatingHistory.objects.update_or_create(
                player=self.winner,
                date=self.event_date,
                defaults={
                    'rating': self.winner.rating
                }
            )

            RatingHistory.objects.update_or_create(
                player=self.loser,
                date=self.event_date,
                defaults={
                    'rating': self.loser.rating
                }
            )

    def __str__(self):
        return '{0}: {1}, {2} vs {3}, {4}-{5}'.format(
            self.event.name, self.event_date, self.winner,
            self.loser, self.winner_score, self.loser_score
        )

    class Meta:
        db_table = 'match'
        verbose_name = _('match result')
        verbose_name_plural = _('match results')


class RatingHistory(models.Model):
    player = models.ForeignKey(
        'Player',
        db_index=True,
        verbose_name=_('player'),
        null=False,
        on_delete=models.CASCADE
    )
    date = models.DateField(db_index=True, verbose_name=_('date'), null=False)
    rating = models.FloatField(null=False)

    def __str__(self):
        return "{0} {1}".format(self.player.full_name, self.date)

    class Meta:
        db_table = 'ratinghistory'
        verbose_name = _('rating history')
        verbose_name_plural = _('rating history')
