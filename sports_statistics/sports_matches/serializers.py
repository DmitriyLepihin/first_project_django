from rest_framework.serializers import ModelSerializer

from sports_matches.models import MatchResults


class MatchResultsSerializer(ModelSerializer):
    class Meta:
        model = MatchResults
        fields = '__all__'
