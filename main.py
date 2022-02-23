import telebot
from telebot import types
import psycopg2
from psycopg2 import Error
import datetime

usl0="monday","tuesday","wednesday","thursday","friday","saturday","week","next week"
usl1="monday","tuesday","wednesday","thursday","friday","saturday","week","next week","n недели"


token="5137031889:AAHhy-ynoT_JkEnW3Yv5sMv8lj4lsucfEHQ"
bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    keyboard=types.ReplyKeyboardMarkup()
    keyboard.row("monday","tuesday","wednesday","thursday","friday","saturday","week","next week","n недели")
    bot.send_message(message.chat.id, 'Привет! На какой день хотите узнать расписание?', reply_markup=keyboard)
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Cписок доступных команд: \n /mtusi - ссылка на сайт \n '
                                      'Кнопки с днями недели выводят расписание в этот день \n n недели - какая сейчас неделя')
@bot.message_handler(commands=['mtusi'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ссылка на сайт- https://mtuci.ru/')

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() not in usl1:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')
    if message.text.lower() == "n недели":
        now = datetime.datetime.now()
        ned = datetime.date(now.year, now.month, now.day).isocalendar()[1]
        if ned % 2 == 0:
            nedd = str(ned) + "-четная"
        else:
            nedd = str(ned) + "-нечетная"
        print(nedd)
        bot.send_message(message.chat.id, nedd)

    if message.text.lower() in usl0:
        now = datetime.datetime.now()
        nned = datetime.date(now.year, now.month, now.day).isocalendar()[1]
        if nned % 2 == 0:
            den="SELECT * FROM public."+message.text.lower()
        else:
            den = "SELECT * FROM public.n" + message.text.lower()
        if message.text.lower()=="next week":
            if (nned+1)%2==0:
                den="SELECT * FROM public.week"
            else:
                den="SELECT * FROM public.nweek"

        try:
            connection = psycopg2.connect(user="postgres", password="123321000z", host="localhost", port="5432", database="raspisanie")
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            cursor.execute(den)
            a=cursor.fetchall()
            for i in range (len(a)):
                bot.send_message(message.chat.id,' '.join(a[i]))


        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

bot.polling()