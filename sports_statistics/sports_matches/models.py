from django.db import models


class MatchResults(models.Model):
    type_sport = models.CharField(max_length=150, null=True)
    league = models.CharField(max_length=150, null=True)
    team_one = models.CharField(max_length=350, null=True)
    team_two = models.CharField(max_length=350, null=True)
    score_one = models.IntegerField()
    score_two = models.IntegerField()
    date_match = models.DateField(null=True, blank=True)
    date_match = models.DateField()
    match_details = models.JSONField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.type_sport} - league {self.league}: {self.team_one} {self.score_one}:\
{self.score_two} {self.team_two}"
