import requests
from bs4 import BeautifulSoup

from django.core.management import BaseCommand

from sports_matches.models import MatchResults
from datetime import datetime

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
 Chrome/88.0.4324.150 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,\
application/signed-exchange;v=b3;q=0.9'}


def get_html(url):
    res = requests.get(url, headers=HEADERS)
    return res.text


def get_all_links(html):
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


def get_data_page(html):
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
        else:
            continue
    return matches


def save_result(items):
    g = 0
    for info in items:
        match_res = MatchResults(type_sport='Basketball',
                                 league='NBA',
                                 date_match=info['date_match'],
                                 team_one=info['team_one'],
                                 team_two=info['team_two'],
                                 score_one=info['score_team_one'],
                                 score_two=info['score_team_two'],
                                 ).save()
        g += 1
        print(f'done {g}')


def parse():
    for i in range(2002, 2021):
        html = get_html(f'https://www.basketball-reference.com/leagues/NBA_{i}_games.html')
        all_links = (get_all_links(html))
        for url in all_links:
            html = get_html(url)
            save_result(get_data_page(html))


class Command(BaseCommand):
    help = 'Добавление в базу данных результатов матчей НБА с 2002 г.'

    def handle(self, *args, **options):
        parse()
