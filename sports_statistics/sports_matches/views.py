from django.http import JsonResponse
from django.shortcuts import render
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

        res = self.queryset.get(team_one=team_one, team_two=team_two, date_match=date)

        return JsonResponse({'match_date': res.date_match, 'team_one': res.team_one, 'team_two': res.team_two,
                             'score_team-one': res.score_one, 'score_team_two': res.score_two
                             }, safe=False)


class StatsWinAllTeamNBAViewSet(ModelViewSet):
    queryset = StatsWinAllTeamNBA.objects.all()
    serializer_class = StatsWinAllTeamNBASerializer

    def list(self, request, *args, **kwargs):
        team_one = request.query_params.get('team1')
        team_two = request.query_params.get('team2')
        teams = team_one, team_two
        sort_team = sorted(teams)

        result = self.queryset.get(team_one=sort_team[0], team_two=sort_team[1])
        return JsonResponse({'team_one': result.team_one, 'win_team_one': result.win_team_one,
                             'percent_win_team_one': result.win_percent_team_one, 'team_two': result.team_two,
                             'win_team_two': result.win_team_two,
                             'percent_win_team_two': result.win_percent_team_two}, safe=False)
