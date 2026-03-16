from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from movies.models import Movie, Room, Seat, Session


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        Movie.objects.all().delete()
        Room.objects.all().delete()

        movies = [
            Movie.objects.create(
                title='Inception',
                description='A thief who steals corporate secrets through dream-sharing technology.',
                duration_minutes=148,
                genre='Sci-Fi',
                poster_url='https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg'
            ),
            Movie.objects.create(
                title='The Dark Knight',
                description='Batman raises the stakes in his war on crime.',
                duration_minutes=152,
                genre='Action',
                poster_url='https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg'
            ),
            Movie.objects.create(
                title='Interstellar',
                description='A team of explorers travel through a wormhole in space.',
                duration_minutes=169,
                genre='Sci-Fi',
                poster_url='https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg'
            ),
            Movie.objects.create(
                title='Parasite',
                description='Greed and class discrimination threaten the newly formed symbiotic relationship.',
                duration_minutes=132,
                genre='Drama',
                poster_url='https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg'
            ),
        ]

        rooms = []
        for i in range(1, 4):
            room = Room.objects.create(
                name=f'Sala {i}',
                rows=6,
                columns=8
            )
            rooms.append(room)

            for row in 'ABCDEF':
                for col in range(1, 9):
                    Seat.objects.create(room=room, row=row, column=col)

        now = timezone.now()
        for i, movie in enumerate(movies):
            room = rooms[i % len(rooms)]
            for day in range(3):
                for hour in [14, 17, 20]:
                    Session.objects.create(
                        movie=movie,
                        room=room,
                        datetime=now + timedelta(days=day, hours=hour)
                    )

        self.stdout.write(self.style.SUCCESS(
            f'Done! Created {len(movies)} movies, {len(rooms)} rooms, and sessions.'
        ))