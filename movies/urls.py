from django.urls import path
from .views import MovieListView, MovieDetailView, SessionListView, SeatMapView

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('<int:movie_id>/sessions/', SessionListView.as_view(), name='session_list'),
    path('sessions/<int:session_id>/seats/', SeatMapView.as_view(), name='seat_map'),
]