from rest_framework.serializers import ModelSerializer

from sports_matches.models import MatchResults, StatsWinAllTeamNBA


class MatchResultsSerializer(ModelSerializer):
    class Meta:
        model = MatchResults
        fields = (
            'team_one',
            'team_two',
            'score_one',
            'score_two',
            'date_match',
        )


class StatsWinAllTeamNBASerializer(ModelSerializer):
    class Meta:
        model = StatsWinAllTeamNBA
        fields = (
            'team_one',
            'win_team_one',
            'win_percent_team_one',
            'team_two',
            'win_team_two',
            'win_percent_team_two',
            'win_team_one_guest',
            'win_team_one_home',
            'win_team_two_guest',
            'win_team_two_home',
        )
