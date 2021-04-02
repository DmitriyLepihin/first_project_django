# from django.http import JsonResponse
# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from sports_matches.models import MatchResults, StatsWinAllTeamNBA
from sports_matches.serializers import MatchResultsSerializer, StatsWinAllTeamNBASerializer
from datetime import datetime


class MatchResultsViewSet(ModelViewSet):
    queryset = MatchResults.objects.all()
    serializer_class = MatchResultsSerializer

    def list(self, request, *args, **kwargs):
        team_one = request.query_params.get('team1')
        team_two = request.query_params.get('team2')
        date_match = request.query_params.get('date')
        date_list = str(date_match).split('-')
        date = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2])).date()

        res = self.queryset.filter(team_one=team_one, team_two=team_two, date_match=date)
        if res.exists():
            serializer = self.serializer_class(res)
            return Response(data=serializer.data, status=HTTP_200_OK)
        else:
            return Response(data={'detail': 'No match result'}, status=HTTP_404_NOT_FOUND)


class StatsWinAllTeamNBAViewSet(ModelViewSet):
    queryset = StatsWinAllTeamNBA.objects.all()
    serializer_class = StatsWinAllTeamNBASerializer

    def list(self, request, *args, **kwargs):
        team_one = request.query_params.get('team1')
        team_two = request.query_params.get('team2')
        teams = team_one, team_two
        sort_team = sorted(teams)

        result = self.queryset.get(team_one=sort_team[0], team_two=sort_team[1])
        serializer = self.serializer_class(result)
        return Response(data=serializer.data, status=HTTP_200_OK)
