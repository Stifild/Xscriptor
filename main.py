from configs import TELEGRAM_API_KEY, USER_ID
import telebot
from telebot import util, types

bot = telebot.TeleBot(TELEGRAM_API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Start command do nothing, just say hello')

@bot.message_handler(commands=["poweroff"])
def poweroff(message: types.Message):
    computer_name = util.extract_arguments(message.text)
    current_computer = 
    bot.send_message(message.chat.id, 'Computer is shutting down')