import requests
from bs4 import BeautifulSoup

from django.core.management import BaseCommand

from sports_matches.models import MatchResults
from datetime import datetime

DATE_START_APP = datetime.strptime('Feb 15, 2021', '%b %d, %Y').date()

DATE_CHANGES = datetime.strptime('Oct 31, 2000', '%b %d, %Y').date()

START_SEASON_76 = datetime.strptime('Oct 23, 1975', '%b %d, %Y').date()
FINISH_SEASON_76 = datetime.strptime('Jun 6, 1976', '%b %d, %Y').date()

START_SEASON_83 = datetime.strptime('Oct 29, 1982', '%b %d, %Y').date()
FINISH_SEASON_83 = datetime.strptime('May 31, 1983', '%b %d, %Y').date()

START_SEASONS_85_86 = datetime.strptime('Oct 25, 1985', '%b %d, %Y').date()
FINISH_SEASON_86_87 = datetime.strptime('Jun 14, 1987', '%b %d, %Y').date()

DATE_NOW = datetime.now().date()


class Command(BaseCommand):
    help = 'Добавление в базу данных результатов матчей НБА с сезона 68/69 г. + обновление последних результатов'

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
                try:
                    date = data[0].get_text(strip=True)[5::]
                    date = datetime.strptime(date, '%b %d, %Y').date()
                except Exception:
                    date = ''
                if date >= DATE_NOW:
                    break
                if START_SEASON_83 <= date <= FINISH_SEASON_83 or date > DATE_CHANGES or START_SEASONS_85_86 <= \
                        date <= FINISH_SEASON_86_87 or START_SEASON_76 <= date <= FINISH_SEASON_76:
                    try:
                        team_one = data[3].get_text(strip=True)
                    except Exception:
                        team_one = ''
                    try:
                        score_team_one = int(data[5].get_text(strip=True))
                    except Exception:
                        score_team_one = 0
                    try:
                        team_two = data[6].get_text(strip=True)
                    except Exception:
                        team_two = ''
                    try:
                        score_team_two = int(data[8].get_text(strip=True))
                    except Exception:
                        score_team_two = 0
                    matches.append({'date_match': date, 'team_one': team_one, 'score_team_one': score_team_one,
                                    'score_team_two': score_team_two, 'team_two': team_two})
                elif date < DATE_CHANGES:
                    try:
                        team_one = data[3].get_text(strip=True)
                    except Exception:
                        team_one = ''
                    try:
                        score_team_one = int(data[4].get_text(strip=True))
                    except Exception:
                        score_team_one = 0
                    try:
                        team_two = data[6].get_text(strip=True)
                    except Exception:
                        team_two = ''
                    try:
                        score_team_two = int(data[7].get_text(strip=True))
                    except Exception:
                        score_team_two = 0
                    matches.append({'date_match': date, 'team_one': team_one, 'score_team_one': score_team_one,
                                    'score_team_two': score_team_two, 'team_two': team_two})
            else:
                continue

        return matches

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

    def parse(self):
        for i in range(1969, 2022):
            html = self.get_html(f'https://www.basketball-reference.com/leagues/NBA_{i}_games.html')
            all_links = (self.get_all_links(html))
            for url in all_links:
                html = self.get_html(url)
                self.save_result(self.get_data_page(html))

    def parse_last_matches_updates(self):
        html = self.get_html(f"https://www.basketball-reference.com/leagues/NBA_{DATE_NOW.year}_games\
-{DATE_NOW.strftime('%B').lower()}.html")
        self.save_result(self.get_data_page(html))
