import requests
from bs4 import BeautifulSoup

from django.core.management import BaseCommand

from sports_matches.models import MatchResults, StatsWinAllTeamNBA
from datetime import datetime, timedelta

DATE_START_APP = datetime.strptime('Feb 15, 2021', '%b %d, %Y').date()

DATE_CHANGES = datetime.strptime('Oct 31, 2000', '%b %d, %Y').date()

START_SEASON_76 = datetime.strptime('Oct 23, 1975', '%b %d, %Y').date()
FINISH_SEASON_76 = datetime.strptime('Jun 6, 1976', '%b %d, %Y').date()

START_SEASON_83 = datetime.strptime('Oct 29, 1982', '%b %d, %Y').date()
FINISH_SEASON_83 = datetime.strptime('May 31, 1983', '%b %d, %Y').date()

START_SEASONS_85_86 = datetime.strptime('Oct 25, 1985', '%b %d, %Y').date()
FINISH_SEASON_86_87 = datetime.strptime('Jun 14, 1987', '%b %d, %Y').date()

DATE_NOW = datetime.now().date()
CHECK_DATE = DATE_NOW - timedelta(1)

YEAR_START = 1981
YEAR_FINISH = 2022

URL_BR = 'https://www.basketball-reference.com/leagues/NBA_'


class Command(BaseCommand):
    help = 'Added 80/81 NBA season results to database + updated latest results. Counting victories in personal\
 meetings of teams.'
    teams_nba = {
        'New Jersey Nets': 'Brooklyn Nets',
        'Charlotte Bobcats': 'Charlotte Hornets',
        'Vancouver Grizzlies': 'Memphis Grizzlies',
        'New Orleans Hornets': 'New Orleans Pelicans',
        'New Orleans/Oklahoma City Hornets': 'New Orleans Pelicans',
        'Seattle SuperSonics': 'Oklahoma City Thunder',
        'Washington Bullets': 'Washington Wizards',
        'Kansas City Kings': 'Sacramento Kings',
        'San Diego Clippers': 'Los Angeles Clippers'
    }

    def handle(self, *args, **options):
        if DATE_NOW > DATE_START_APP:
            self.parse_last_matches_updates()
        else:
            self.parse()

    def get_html(self, url):
        res = requests.get(url)
        return res.text

    def get_all_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', class_='filter')
        links = []
        for div in divs:
            for a in div:
                try:
                    a.find('a').get('href')
                    link = 'https://www.basketball-reference.com' + a.find('a').get('href')
                    links.append(link)
                except Exception:
                    continue

        return links

    def get_data_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('tr')
        matches = []
        for info in items[1::]:
            data = info.find_all()
            if len(data) > 1:
                date = self.check_data(data, 0)
                if date >= DATE_NOW:
                    break
                if START_SEASON_83 <= date <= FINISH_SEASON_83 or date > DATE_CHANGES or START_SEASONS_85_86 <= \
                        date <= FINISH_SEASON_86_87 or START_SEASON_76 <= date <= FINISH_SEASON_76:
                    team_one = self.check_data(data, 3)
                    score_team_one = int(self.check_data(data, 5))
                    team_two = self.check_data(data, 6)
                    score_team_two = int(self.check_data(data, 8))
                    matches.append({'date_match': date, 'team_one': team_one, 'score_team_one': score_team_one,
                                    'score_team_two': score_team_two, 'team_two': team_two})
                elif date < DATE_CHANGES:
                    team_one = self.check_data(data, 3)
                    score_team_one = int(self.check_data(data, 4))
                    team_two = self.check_data(data, 6)
                    score_team_two = int(self.check_data(data, 7))
                    matches.append({'date_match': date, 'team_one': team_one, 'score_team_one': score_team_one,
                                    'score_team_two': score_team_two, 'team_two': team_two})
            else:
                continue
        return matches

    def check_data(self, data, index):
        values = None
        if index == 0:
            try:
                values = data[index].get_text(strip=True)[5::]
                values = datetime.strptime(values, '%b %d, %Y').date()
            except Exception:
                values = ''
        else:
            try:
                values = data[index].get_text(strip=True)
                if self.teams_nba.get(values):
                    values = self.teams_nba.get(values)
                else:
                    raise ValueError
            except(Exception, ValueError):
                pass
        return values

    def save_result(self, items):
        for info in items:
            match_res = MatchResults.objects.filter(date_match=info['date_match'],
                                                    team_one=info['team_one'],
                                                    team_two=info['team_two'],
                                                    score_one=info['score_team_one'],
                                                    score_two=info['score_team_two'])

            if match_res:
                continue
            else:
                match_res = MatchResults(type_sport='Basketball',
                                         league='NBA',
                                         date_match=info['date_match'],
                                         team_one=info['team_one'],
                                         team_two=info['team_two'],
                                         score_one=info['score_team_one'],
                                         score_two=info['score_team_two'],
                                         ).save()
        self.save_stat_matches(items)

    def save_stat_matches(self, items):
        for info in items:
            if info['date_match'] == CHECK_DATE:
                teams = info['team_one'], info['team_two']
                sort_teams = sorted(teams)
                if sort_teams[0] != teams[0]:
                    if StatsWinAllTeamNBA.objects.filter(team_one=sort_teams[0], team_two=sort_teams[1]).exists():
                        match_stat = StatsWinAllTeamNBA.objects.filter(team_one=sort_teams[0], team_two=sort_teams[1])
                        if info['score_team_one'] > info['score_team_two']:
                            match_stat[0].win_team_two += 1
                            match_stat[0].win_team_two_home += 1
                            all_match = match_stat[0].win_team_two + match_stat[0].win_team_one
                            match_stat[0].win_percent_team_one = match_stat[0].win_team_one / all_match * 100
                            match_stat[0].win_percent_team_two = match_stat[0].win_team_two / all_match * 100
                            match_stat.save()
                        else:
                            match_stat[0].win_team_one += 1
                            match_stat[0].win_team_one_guest += 1
                            all_match = match_stat[0].win_team_two + match_stat[0].win_team_one
                            match_stat[0].win_percent_team_one = match_stat[0].win_team_one / all_match * 100
                            match_stat[0].win_percent_team_two = match_stat[0].win_team_two / all_match * 100
                            match_stat.save()
                    else:
                        if info['score_team_one'] > info['score_team_two']:
                            match_stat = StatsWinAllTeamNBA(team_one=sort_teams[0], team_two=sort_teams[1],
                                                            win_team_two=1, win_team_two_home=1).save()
                        else:
                            match_stat = StatsWinAllTeamNBA(team_one=sort_teams[0], team_two=sort_teams[1],
                                                            win_team_one=1, win_team_one_guest=1).save()
                else:
                    if StatsWinAllTeamNBA.objects.filter(team_one=sort_teams[0], team_two=sort_teams[1]).exists():
                        match_stat = StatsWinAllTeamNBA.objects.filter(team_one=sort_teams[0], team_two=sort_teams[1])
                        if info['score_team_one'] > info['score_team_two']:
                            match_stat[0].win_team_one += 1
                            match_stat[0].win_team_one_home += 1
                            all_match = match_stat[0].win_team_two + match_stat[0].win_team_one
                            match_stat[0].win_percent_team_one = match_stat[0].win_team_one / all_match * 100
                            match_stat[0].win_percent_team_two = match_stat[0].win_team_two / all_match * 100
                            match_stat.save()
                        else:
                            match_stat[0].win_team_two += 1
                            match_stat[0].win_team_two_guest += 1
                            all_match = match_stat[0].win_team_two + match_stat[0].win_team_one
                            match_stat[0].win_percent_team_one = match_stat[0].win_team_one / all_match * 100
                            match_stat[0].win_percent_team_two = match_stat[0].win_team_two / all_match * 100
                            match_stat.save()
                    else:
                        if info['score_team_one'] > info['score_team_two']:
                            match_stat = StatsWinAllTeamNBA(team_one=info['team_one'], team_two=info['team_two'],
                                                            win_team_one=1, win_team_one_home=1).save()
                        else:
                            match_stat = StatsWinAllTeamNBA(team_one=info['team_one'], team_two=info['team_two'],
                                                            win_team_two=1, win_team_two_guest=1).save()
            else:
                continue

    def parse(self):
        for i in range(YEAR_START, YEAR_FINISH):
            html = self.get_html(f'{URL_BR + str(i)}_games.html')
            all_links = (self.get_all_links(html))
            for url in all_links:
                html = self.get_html(url)
                self.save_result(self.get_data_page(html))

    def parse_last_matches_updates(self):
        html = self.get_html(f"{URL_BR}{DATE_NOW.year}_games-{DATE_NOW.strftime('%B').lower()}.html")
        self.save_result(self.get_data_page(html))
