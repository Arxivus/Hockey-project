import telebot
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webProject.settings')
django.setup()
from django.contrib.auth.models import User
from django.db import transaction

token = ''

bot = telebot.TeleBot(token)
  
@bot.message_handler(commands = ['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Привет! Я бот веб-сайта проведения турниров академии "Спартаковец"\n\nУ меня есть пара полезных команд в меню!\nВот ID чата со мной: {chat_id}')
 
  
@bot.message_handler(commands = ['chat_id'])
def get_chat_ID(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Держи твой чат-ID: {chat_id}')
    
@bot.message_handler(commands = ['change_password'])
@transaction.atomic
def change_password(message):
    chat_id = message.chat.id
    name = message.from_user.username
    user = User.objects.get(username=name)
    if user:
        message = bot.send_message(chat_id, f'{name}, введите новый пароль в своем следующем сообщении \n\nОн не должен быть простым (как qwerty123)\n\nДля надежности используйте заглавные буквы, цифры, спец. символы\n\nЧтобы отменить смену пароля введите "отменить"')
        bot.register_next_step_handler(message, get_new_password)
    else:
        message = bot.send_message(chat_id, f'Пользователь под вашим именем ({name}) не найден на сайте') 

def get_new_password(message):
    chat_id = message.chat.id
    new_password = message.text
    
    if len(new_password) < 8:
        bot.send_message(chat_id, "Пароль слишком короткий! Нужно минимум 8 символов!")
        bot.register_next_step_handler(message, get_new_password)
    
    elif new_password.isdigit():
        bot.send_message(chat_id, "Пароль не может состоять из одних цифр!")
        bot.register_next_step_handler(message, get_new_password)
        
    elif new_password == 'отменить':
        bot.send_message(chat_id, "Изменение отменено\nЧтобы изменить пароль введите соответствующую команду снова")
    
    else:
        try:
            name = message.from_user.username
            user = User.objects.get(username=name)
            user.set_password(new_password)
            user.save()
            bot.send_message(chat_id, 'Новый пароль установлен!')
        except Exception as e:
            print(e)
            bot.send_message(chat_id, 'Не удалось установить пароль. Проверьте пароль или попробуйте еще раз позже')
    
    
bot.polling(none_stop=True)

        
