import requests
from bs4 import BeautifulSoup as b
import telebot
import schedule

URL = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2'
token = '5729867659:AAF8B244CiNMQNhd66is5NDYrcXoC5vkYjs'


def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    temperature = soup.find_all('p', class_='today-temp')
    return [c.text for c in temperature]


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def greeting(message):
    bot.send_message(message.chat.id, 'Hello everyone!!!')


@bot.message_handler(commands=['weather'])
def weather_today(message):
    clear_text = parser(URL)
    bot.send_message(message.chat.id, f'today in Kyiv:{clear_text[0]}')

@bot.message_handler(commands=['notifi'])
def notification(message):
    schedule.every().day.at('06:30').do(weather_today, message)


bot.polling()

schedule.every().day.at('06:00').do(parser, URL)
