from django.db import models


class MatchResults(models.Model):
    type_sport = models.CharField(max_length=150, null=True)
    league = models.CharField(max_length=150, null=True)
    team_one = models.CharField(max_length=350, null=True)
    team_two = models.CharField(max_length=350, null=True)
    score_one = models.IntegerField()
    score_two = models.IntegerField()
    date_match = models.DateField(null=True, blank=True)
    match_details = models.JSONField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.type_sport} - league {self.league}: {self.team_one} {self.score_one}:\
{self.score_two} {self.team_two}"


class StatsWinAllTeamNBA(models.Model):
    team_one = models.CharField(max_length=350, null=True)
    team_two = models.CharField(max_length=350, null=True)
    win_team_one = models.IntegerField(default=0)
    win_team_two = models.IntegerField(default=0)
    win_percent_team_one = models.FloatField(default=0)
    win_percent_team_two = models.FloatField(default=0)
    win_team_one_guest = models.IntegerField(default=0)
    win_team_one_home = models.IntegerField(default=0)
    win_team_two_guest = models.IntegerField(default=0)
    win_team_two_home = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team_one} - WIN {self.win_team_one} : {self.win_team_two} WIN - {self.team_two}"
