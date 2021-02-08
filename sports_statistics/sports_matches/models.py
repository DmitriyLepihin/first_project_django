from django.db import models


class MatchResults(models.Model):
    type_sport = models.CharField(max_length=150, null=True)
    team_one = models.CharField(max_length=350, null=True)
    team_two = models.CharField(max_length=350, null=True)
    score_one = models.IntegerField()
    score_two = models.IntegerField()
    date_match = models.DateField()
    match_details = models.CharField(max_length=800, null=True, blank=True)
