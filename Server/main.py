from configs import TELEGRAM_API_KEY, MAIN_USER_ID
import telebot
from Server.twm import TellWithMe as TWM
from telebot import util, types

twm = TWM()
bot = telebot.TeleBot(TELEGRAM_API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == MAIN_USER_ID:
        bot.send_message(message.chat.id, 'Start command do nothing, just say hello')
    else:
        bot.send_message(message.chat.id, 'You are not authorized to use this bot.')

@bot.message_handler(commands=["poweroff"])
def sendCommand(message: types.Message):
    if message.from_user.id == MAIN_USER_ID:
        rawCommand = util.extract_arguments(message.text)
        computerName = rawCommand.split("/")[0]
        command = rawCommand.split("")[1]
        for address, data in twm.twmcd.items():
            if data["name"] == computerName:
                twm.send(twm.compileCommand("IC", {"command": command}), address, "IC", f"Listen {data['name']}! I want to you do {command}")
                bot.send_message(message.chat.id, f"Command {command} sent to {data['name']}")
    else:
        bot.send_message(message.chat.id, 'You are not authorized to use this bot.')