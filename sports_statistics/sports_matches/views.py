from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from sports_matches.models import MatchResults
from sports_matches.serializers import MatchResultsSerializer


class MatchResultsViewSet(ModelViewSet):
    queryset = MatchResults.objects.all()
    serializer_class = MatchResultsSerializer

    def list(self, request):
        return JsonResponse(list(self.queryset.values()), safe=False)
