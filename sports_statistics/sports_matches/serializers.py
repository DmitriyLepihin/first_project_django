from rest_framework.serializers import ModelSerializer

from sports_matches.models import MatchResults, StatsWinAllTeamNBA


class MatchResultsSerializer(ModelSerializer):
    class Meta:
        model = MatchResults
        fields = '__all__'


class StatsWinAllTeamNBASerializer(ModelSerializer):
    class Meta:
        model = StatsWinAllTeamNBA
        fields = '__all__'
