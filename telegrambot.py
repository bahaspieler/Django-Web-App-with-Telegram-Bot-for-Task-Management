import telebot
import requests
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from tabulate import tabulate
import pandas as pd
import time


bot = telebot.TeleBot('Put Your API Token here')

def Button(message):
    r = requests.get('http://127.0.0.1:8000/api/button')
    data = json.loads(r.content)
    key = ReplyKeyboardMarkup(True, False)
    text = 'Hello {}'.format(message.from_user.first_name,'!!')
    for i in range(len(data['list'])):
        button = KeyboardButton(data['list'][i]['name'])
        key.add(button)
    bot.send_message(message.from_user.id, text, reply_markup=key)

@bot.message_handler(commands=['start'])
def start(message):
    Button(message)

# @bot.message_handler(content_types='text')
# def Send_Message(message):
#     link = 'http://127.0.0.1:8000/api/catag'
#     text = {"text": message.text}
#     print(text)
#     r= requests.post(link, data=json.dumps(text))
#     bot.send_message(message.from_user.id, "Catagory is set")


@bot.message_handler(content_types='text')
def Send_Message(message):
    link = 'http://127.0.0.1:8000/api/text'
    text = {"text": message.text}
    print(text)
    r = requests.post(link, data=json.dumps(text))
    data = json.loads(r.text)
    if data['code'] == 401:
        bot.send_message(message.from_user.id, "Data can't be fetched or use the buttons' name at the beginning of search item [i.e. site CXMRD1]")
    elif data['text']=="Please enter the correct value":
        bot.send_message(message.from_user.id, "Please enter the correct value")
    elif data['text']== []:
        bot.send_message(message.from_user.id, "The entry doesn't exist")



    else:
        dic = data['text']
        # dic_final = []
        for a in dic:
            dic_tuple = list(a.items())
            dic_list = [list(ele) for ele in dic_tuple]
            # dic_final.append(dic_list)
            status = tabulate(dic_list, showindex=False)
            status1 = "<pre>{}</pre>".format(status)
            # dic_final.append(status)
            bot.send_message(message.from_user.id, status1, parse_mode='HTML')


bot.polling()


# while True:
#
#     try:
#         bot.polling()
#     except Exception:
#         time.sleep(5)