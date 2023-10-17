import telebot

# Создаем экземпляр бота
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Словарь для хранения зарегистрированных пользователей
users = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in users:
        bot.send_message(chat_id, "Добро пожаловать! Пожалуйста, зарегистрируйтесь.")
        bot.send_message(chat_id, "Введите ваше имя:")
        bot.register_next_step_handler(message, process_name_step)
    else:
        bot.send_message(chat_id, "Вы уже зарегистрированы!")

# Обработчик следующего шага - ввод имени
def process_name_step(message):
    chat_id = message.chat.id
    name = message.text
    users[chat_id] = {'name': name, 'posts': []}
    bot.send_message(chat_id, f"Регистрация прошла успешно, {name}!")

# Обработчик команды /post
@bot.message_handler(commands=['post'])
def post(message):
    chat_id = message.chat.id
    if chat_id in users:
        bot.send_message(chat_id, "Введите ваше сообщение:")
        bot.register_next_step_handler(message, process_post_step)
    else:
        bot.send_message(chat_id, "Сначала зарегистрируйтесь!")

# Обработчик следующего шага - ввод сообщения
def process_post_step(message):
    chat_id = message.chat.id
    post_message = message.text
    users[chat_id]['posts'].append(post_message)
    bot.send_message(chat_id, "Сообщение сохранено!")

# Обработчик команды /view_posts
@bot.message_handler(commands=['view_posts'])
def view_posts(message):
    chat_id = message.chat.id
    if chat_id in users:
        posts = users[chat_id]['posts']
        if posts:
            bot.send_message(chat_id, "Ваши посты:")
            for post in posts:
                bot.send_message(chat_id, post)
        else:
            bot.send_message(chat_id, "У вас пока нет постов!")
    else:
        bot.send_message(chat_id, "Сначала зарегистрируйтесь!")

# Запуск бота
bot.run()