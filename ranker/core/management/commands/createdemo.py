import random
import datetime

from django.core.cache import caches
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from ranker.core.models import Event, Player, Match

DEMO_FIRST_NAMES = [
    'Edward', 'Jason', 'William', 'Thomas', 'Donald', 'Brian', 'Jeff',
    'Mary', 'Jennifer', 'Lisa', 'Sandra', 'Michelle',
    'Patricia', 'Maria', 'Nancy', 'Donna', 'Laura', 'Linda', 'Susan',
    'Karen', 'Carol', 'Sarah', 'Barbara', 'Margaret',
    'Betty', 'Ruth', 'Kimberly', 'Elizabeth', 'Dorothy', 'Helen',
    'Sharon', 'Deborah'
]

DEMO_LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller',
    'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas',
    'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia',
    'Martinez', 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Lee',
    'Walker', 'Hall', 'Allen', 'Young', 'Hernandez', 'King',
    'Wright', 'Lopez', 'Hill', 'Scott', 'Green', 'Adams', 'Baker', 'Gonzalez',
    'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner',
    'Phillips', 'Campbell', 'Parker', 'Evans', 'Edwards', 'Collins',
    'Stewart', 'Sanchez', 'Morris', 'Rogers', 'Reed', 'Cook',
    'Morgan', 'Bell', 'Murphy', 'Bailey', 'Rivera', 'Cooper', 'Richardson',
    'Cox', 'Howard', 'Ward', 'Torres', 'Peterson', 'Gray', 'Ramirez',
    'James', 'Watson', 'Brooks', 'Kelly', 'Sanders', 'Price',
    'Bennett', 'Wood', 'Barnes', 'Ross', 'Henderson', 'Coleman',
    'Jenkins', 'Perry', 'Powell', 'Long', 'Patterson', 'Hughes', 'Flores',
    'Washington', 'Butler', 'Simmons', 'Foster', 'Gonzales',
    'Bryant', 'Alexander', 'Russell', 'Griffin', 'Diaz', 'Hayes'
]

DEMO_N_PLAYERS = 50
DEMO_USERNAME_PREFIX = 'demo_'
DEMO_BASE_DATE = datetime.date(1970, 1, 1)
DEMO_MAX_DAYS = 10000
DEMO_CITIES = ['Gotham', 'Metropolis', 'Emerald City', 'Christmas Town']
DEMO_HANDS = ['L', 'R']
DEMO_EQUIPMENT = ["Atemi 100", "TB ALC", "Petr Korbel Japan", "Some Pimpled Bat"]
DEMO_N_PLAY_DAYS = 60
DEMO_MATCHES_PER_DAY = 20

PLAYER_FIELDS = [f.name for f in Player._meta.fields if f.name != 'id']


class Command(BaseCommand):
    help = 'Creates some demo content for app'

    def handle(self, *args, **options):
        print('Creates demo content.')

        random.seed(42)

        with transaction.atomic():
            events = self.create_events()
            players = self.create_players()
            self.create_matches(events, players)

        self.clear_cache('leaderboard')

        print('Done.')

    def create_events(self,):
        """Create demo events"""
        print(f'Creating events...')

        events = {
            'regular': {
                'name': 'Regular Office Battles',
                'short_name': 'Office Games',
                'address': 'Office',
                'coefficient': 0.6
            },
            'special': {
                'name': 'Friday Tournament',
                'short_name': 'Friday Clash',
                'address': 'Office',
                'coefficient': 1.0
            }
        }

        result = {}

        for name, meta in events.items():
            result[name] = Event.objects.create(**meta)

        return result

    def create_players(self):
        """Create some random players"""
        print('Creating random players...')

        players = []

        for _ in range(DEMO_N_PLAYERS):

            first_name = random.choice(DEMO_FIRST_NAMES)
            last_name = random.choice(DEMO_LAST_NAMES)
            username = f'{DEMO_USERNAME_PREFIX}{first_name.lower()}{last_name.lower()}'

            date_of_birth = DEMO_BASE_DATE + datetime.timedelta(
                days=random.randint(0, DEMO_MAX_DAYS)
            )

            city = random.choice(DEMO_CITIES)
            hand = random.choice(DEMO_HANDS)
            equipment = random.choice(DEMO_EQUIPMENT)
            rating = Player.INITIAL_RATING_SCORE

            player = [
                first_name, last_name, username, date_of_birth,
                city, hand, equipment, rating
            ]

            if not Player.objects.filter(username=username).exists():
                p = Player(**dict(zip(PLAYER_FIELDS, player)))
                p.save()

                players.append(p)

        return players

    def create_matches(self, events, players):
        """Create some random match results for the past two months"""
        print('Creating random matches...')

        start_date = timezone.now().date() - datetime.timedelta(days=DEMO_N_PLAY_DAYS)
        players = list(Player.objects.all())

        for day in range(DEMO_N_PLAY_DAYS):
            play_day = start_date + datetime.timedelta(days=day)

            if play_day.strftime('%A') == 'Friday':
                event = events['special']
            else:
                event = events['regular']

            for n in range(DEMO_MATCHES_PER_DAY):
                winner, loser = random.sample(players, k=2)

                # last two matches of day are 3rd place and finals
                if n + 2 == DEMO_MATCHES_PER_DAY:
                    phase = 3
                elif n + 1 == DEMO_MATCHES_PER_DAY:
                    phase = 1
                else:
                    phase = None

                match = Match(
                    event=event,
                    event_date=play_day,
                    event_phase=phase,
                    winner=winner,
                    loser=loser,
                    winner_score=1,
                    loser_score=0
                )
                match.save()

    def clear_cache(self, cache_name):
        """Clear LB cache"""
        print('Clearing cache...')

        try:
            lb_cache = caches[cache_name]
        except Exception:
            lb_cache = None

        if lb_cache is not None:
            lb_cache.clear()
