import telebot
from config import TOKEN
from utils import keys
from extensions import ConversionException, ExchConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n \
<имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversionException('Неправильное количество параметров.')
        quote, base, amount = values
        total_base = ExchConverter.get_price(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Не удалось обработать команду проверьте правильность параметров ввода\n { e }')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n { e }')
    else:
        text = f'Цена { amount } { quote.lower() } в { base.lower() } - { round(float(total_base), 2) }'
        bot.send_message(message.chat.id, text)


bot.polling()
