from rest_framework import generics, permissions
from .models import Movie, Session, Seat
from .serializers import MovieSerializer, SessionSerializer, SeatSerializer


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all().order_by('title')
    serializer_class = MovieSerializer
    permission_classes = (permissions.AllowAny,)


class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (permissions.AllowAny,)


class SessionListView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Session.objects.filter(movie_id=movie_id).order_by('datetime')


class SeatMapView(generics.ListAPIView):
    serializer_class = SeatSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        session = Session.objects.get(id=session_id)
        return Seat.objects.filter(room=session.room).order_by('row', 'column')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['session_id'] = self.kwargs['session_id']
        return context