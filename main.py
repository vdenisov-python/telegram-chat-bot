import telebot
import constants
from datetime import datetime
from exrta_modules import weather, images, numbers


# Создание бота
bot = telebot.TeleBot(constants.token)
bot.last_command = ''

# Лог будет начинаться с информации о боте
print(bot.get_me())


# Вывод данных о входящих и отправленных сообщениях на экран
def log(message, answer):

    print('\t' + '-' * 30)
    print(datetime.now())
    print("> Отправитель: {0} {1}\n> id = {2}\n> Текст: {3}".\
          format(message.from_user.first_name,
                 message.from_user.last_name,
                 message.from_user.id,
                 message.text))
    print("<<<", answer)

########################################################
#                       Команды                        #
########################################################

# Указание, что следующая дальше функция должная быть
#   вызвана, когда боту приходит сообщение нужного типа


@bot.message_handler(commands=['start'])
# Создание кастомной клавиатуры
def handle_start(message):

    user_markup = telebot.types.ReplyKeyboardMarkup\
        (resize_keyboard=True, one_time_keyboard=False)
    user_markup.row('/image', '/weather')
    user_markup.row('/help', '/settings', '/game')
    user_markup.row('/close_keyboard')
    system_info = '<i>Включена основная клавиатура</i>'
    bot.send_message(message.from_user.id, system_info,
                     parse_mode="HTML", reply_markup=user_markup)


@bot.message_handler(commands=['close_keyboard'])
# Сокрытие кастомной клавиатуры
def handle_stop(message):

    hide_markup = telebot.types.ReplyKeyboardRemove()
    system_info = '<i>Клавиатура отключена</i>'
    bot.send_message(message.from_user.id, system_info,
                     parse_mode="HTML", reply_markup=hide_markup)


@bot.message_handler(commands=['help'])
def handle_text(message):

    system_info =\
    '''<i>Мои возможности весьма специфичны.
    Но ты только посмотри... Всё работает !!!</i>'''
    bot.send_message(message.chat.id, system_info, parse_mode='HTML')
    log(message, 'Мои возможности весьма специфичны...')


@bot.message_handler(commands=['settings'])
def handle_settings(message):

    bot.send_message(message.chat.id, 'Настройки пока недоступны :(')
    log(message, 'Настройки пока недоступны :(')


@bot.message_handler(commands=['game'])
def handle_action(message):

    bot.send_message(message.chat.id,
        '''<i>Давай по играем в игру "Тайна чисел".
        Загадай любое число и я скажу интересные факты о нём.</i>''',
        parse_mode="HTML")
    bot.last_command = '/game'
    log(message, 'Давай по играем в игру "Тайна чисел"...')


@bot.message_handler(commands=['image'])
def handle_settings(message):

    cmd_line = message.text.split(' ', 1)
    if len(cmd_line) > 1:
        key_word = cmd_line[1:]
        answer = images.search_by_keyword(key_word)
    else:
        bot.last_command = '/image'
        answer = 'Введите категорию'
    bot.send_message(message.chat.id, answer)
    log(message, answer)


@bot.message_handler(commands=['weather'])
def handle_weather(message):

    cmd_line = message.text.split(' ', 1)
    if len(cmd_line) > 1:
        city = cmd_line[1:]
        answer = weather.weather_in_city(city)
    else:
        bot.last_command = '/weather'
        answer = 'Введите город'
    bot.send_message(message.chat.id, answer)
    log(message, answer)


# Если сообщение с командой не обработается в декераторе для команд,
#   то оно пройдёт условие, как текст (смайлики - это тоже текст).

########################################################
#                         Текст                        #
########################################################

@bot.message_handler(content_types=['text'])
def handle_text(message):

    # Получить id, на который будет отправлен результат обработки запроса
    target_id = message.chat.id
    answer = 'Ошибка при выполнении команды :('

    if bot.last_command == '/image':
        category_of_image = message.text
        answer = images.search_by_keyword(category_of_image)

    if bot.last_command == '/weather':
        name_of_city = message.text
        answer = weather.weather_in_city(name_of_city)

    if bot.last_command == '/game' and message.text.isdigit():
        new_number = int(message.text)
        answer = numbers.interesting_or_not(new_number)

    if bot.last_command != '':

        # Отправить ответное сообщение пользователю
        bot.send_message(target_id, answer, parse_mode='HTML')

        # Записать информацию об обработке запроса
        print("> {} (after command '{}')".format\
                (message.text, bot.last_command), '\n<<< '+answer)

    bot.last_command = ''

########################################################
#                  Новая категория                     #
########################################################

'''
    @bot.message_handler(content_types=['commands'])
    @bot.message_handler(content_types=['document'])
    @bot.message_handler(content_types=['audio'])
    @bot.message_handler(content_types=['photo'])
    @bot.message_handler(content_types=['sticker'])
    ... и т.д.
'''

#######################################################

# Постоянное отправление запросов
bot.polling(none_stop=True, interval=0)
