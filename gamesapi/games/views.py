from django.shortcuts import render
from django.contrib.auth.models import User

from django_filters.rest_framework import FilterSet
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter

from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.throttling import ScopedRateThrottle

from games.models import Game
from games.models import GameCategory
from games.models import Player
from games.models import PlayerScore
from games.serializers import GameSerializer
from games.serializers import GameCategorySerializer
from games.serializers import UserSerializer
from games.serializers import PlayerSerializer
from games.serializers import PlayerScoreSerializer
from games.permissions import IsOwnerOrReadOnly


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly)
    filter_fields = (
        'name',
        'game_category',
        'release_date',
        'played',)
    search_fields = (
        '^name',)
    ordering_fields = (
        'name',
        'release_date',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly)

class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)
    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name',)

class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)

class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'
    filter_fields = (
        'name',
        'gender',
        )
    search_fields = (
        '^name',
        )
    ordering_fields = (
        'name',
        )

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'

class PlayerScoreFilter(FilterSet):
    min_score = NumberFilter(
        field_name='score', lookup_expr='gte')
    max_score = NumberFilter(
        field_name='score', lookup_expr='lte')
    from_score_date = DateTimeFilter(
        field_name='score_date', lookup_expr='gte')
    to_score_date = DateTimeFilter(
        field_name='score_date', lookup_expr='lte')
    player_name = AllValuesFilter(
        field_name='player__name')
    game_name = AllValuesFilter(
        field_name='game__name')

    class Meta:
        model = PlayerScore
        fields = (
            'score',
            'from_score_date',
            'to_score_date',
            'min_score',
            'max_score',
            'player_name',
            'game_name',
            )

class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'
    filter_class = PlayerScoreFilter
    ordering_fields = (
        'score',
        'score_date',
        )

class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'games': reverse(GameList.name, request=request),
            'game-categories': reverse(GameCategoryList.name, request=request),
            'users': reverse(UserList.name, request=request),
            })
