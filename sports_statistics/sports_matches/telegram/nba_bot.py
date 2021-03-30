import json
import requests
import telebot
from telebot import types
from keyboa import keyboa_maker

TEAM_NBA = [
    'Los Angeles Lakers', 'Los Angeles Clippers', 'San Antonio Spurs', 'Memphis Grizzlies',
    'Philadelphia 76ers', 'Brooklyn Nets', 'Toronto Raptors', 'Boston Celtics', 'New York Knicks',
    'Milwaukee Bucks', 'Indiana Pacers', 'Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons',
    'Charlotte Hornets', 'Miami Heat', 'Atlanta Hawks', 'Orlando Magic', 'Washington Wizards',
    'Portland Trail Blazers', 'Utah Jazz', 'Denver Nuggets', 'Oklahoma City Thunder', 'Minnesota Timberwolves',
    'Phoenix Suns', 'Golden State Warriors', 'Sacramento Kings', 'Dallas Mavericks', 'New Orleans Pelicans',
    'Houston Rockets'
]

MSG_GREETING = 'Добро пожаловать в чат-бот который\n\
покажет статистику личных встреч команд NBA 🏀\n\n⬇‍Выбери две команды в меню⬇'

URL_BR = 'https://www.basketball-reference.com'

MSG_URL = 'Еще больше информации о баскетболе можно получить перейдя по ссылке ⬇'

MSG_ALL_GAMES = 'Всего проведено:'

MSG_WIN = 'побед:'

MSG_PERCENT_WIN = 'процент побед:'

teams = []

with open('token.json', 'r') as file:
    bot = telebot.TeleBot(json.load(file)['TOKEN'])


@bot.message_handler(func=lambda m: True)
def start_bot(message):
    user_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_kb.row('start', 'exit')
    if message.text == 'start':
        key = keyboa_maker(items=TEAM_NBA, copy_text_to_callback=True, items_in_row=3)
        bot.send_message(message.from_user.id, reply_markup=key, text=MSG_GREETING)
    if message.text == 'exit':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        url_button = types.InlineKeyboardButton(text="URL", url=URL_BR)
        keyboard.add(url_button)
        bot.send_message(message.from_user.id, MSG_URL, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_walker(call):
    global teams
    if not teams:
        teams.append(call.data)
    else:
        teams.append(call.data)
        sort_teams = sorted(teams)
        req = requests.get(f'http://127.0.0.1:8000/api/all_teams_matches/?team1={sort_teams[0]}&team2={sort_teams[1]}')
        res = json.loads(req.text)
        all_match = res['win_team_one'] + res['win_team_two']
        result = f"{MSG_ALL_GAMES} {all_match} игр\n\n{res['team_one']} {MSG_WIN} {res['win_team_one']}\n\
{MSG_PERCENT_WIN} {int(res['percent_win_team_one'])}%\n\n{res['team_two']} {MSG_WIN} {res['win_team_two']}\n\
{MSG_PERCENT_WIN} {int(res['percent_win_team_two'])}%"
        teams = []
        bot.send_message(call.message.chat.id, result)


bot.polling()
