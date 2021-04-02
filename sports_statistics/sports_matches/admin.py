from django.contrib import admin

from sports_matches.models import MatchResults, StatsWinAllTeamNBA, TeamsNBA

admin.site.register(MatchResults)
admin.site.register(StatsWinAllTeamNBA)
admin.site.register(TeamsNBA)