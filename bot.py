import telebot
from telebot import types
from tasks_tree import Tasks_Tree

bot = telebot.TeleBot('6607166211:AAFCnnvZ0aPEc15A1Q8akqrGXgH-nmhLFJM')

user_base = {}
start_nodes = []
task = None
first_time  = True

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Начать!✔', callback_data='start')
    keyboard.row(button)
    bot.send_message(message.chat.id, text='Привет! Готов(-а) начать?', reply_markup=keyboard, parse_mode='html')
    if not message.from_user.id in user_base.keys():
        user_id = message.from_user.id
        user_base[user_id] = Tasks_Tree()



@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    print(call.data)
    if call.data == 'start':
        global start_nodes, first_time
        print(user_base)
        start_nodes = user_base[call.from_user.id].get_current_node_keys()
    if call.from_user.id in user_base.keys():
        print(user_base)
    else:
        if call.data != 'start':
            if call.data == 'back':
                user_base[call.from_user.id].change_current_node('..')
                first_time = True
            else:
                user_base[call.from_user.id].change_current_node(call.data)

        if call.data == 'show':
            solution = user_base[call.from_user.id].get_solution()
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Решение:')
            if solution['image']:
                bot.send_photo(chat_id=call.from_user.id, photo=open(solution['image'], 'rb'), caption=solution['text'])
            else:
                bot.send_message(chat_id=call.from_user.id, text=solution['text'])
            next_btn = types.InlineKeyboardButton(text='Следующая задача⏩', callback_data='cont')
            back_btn = types.InlineKeyboardButton(text='Назад❌', callback_data='back')
            keyboard1 = types.InlineKeyboardMarkup()
            keyboard1.row(next_btn, back_btn)
            bot.send_message(chat_id=call.from_user.id, text='Что дальше?', reply_markup=keyboard1)

        if user_base[call.from_user.id].is_current_node_list() and (call.data == 'cont' or first_time):
            task = user_base[call.from_user.id].get_random_task()
            if task == "congratulations":
                back_btnn = types.InlineKeyboardButton(text='Назад❌', callback_data='back')
                keybrd = types.InlineKeyboardMarkup().row(back_btnn)
                task = user_base[call.from_user.id].get_random_task() 
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='🏆Поздравляем!🏆\n Вы решили все задачи в данном разделе! В ближайших обновлениях мы расширим множество задач, а пока можете заняться другими разделами.', reply_markup=keybrd)
            else:
                first_time = False
                keyboard2 = types.InlineKeyboardMarkup()
                show_sol = types.InlineKeyboardButton(text='Показать решение', callback_data='show')
                keyboard2.add(show_sol)   
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Задача:')      
                if task["image"]:
                    bot.send_photo(chat_id=call.from_user.id, photo=open(task['image'], 'rb'), caption=task["text"])
                else:
                    bot.send_message(chat_id=call.from_user.id, text=task["text"]) 
                bot.send_message(chat_id=call.from_user.id, text='Показать решение?', reply_markup=keyboard2)

        else:
            keyboard = types.InlineKeyboardMarkup()
            for i in user_base[call.from_user.id].get_current_node_keys():
                button = types.InlineKeyboardButton(text=str(i) +  '✏', callback_data=i)
                keyboard.row(button)
            back = types.InlineKeyboardButton('Назад❌', callback_data='back')
            if user_base[call.from_user.id].get_current_node_keys() != start_nodes:
                keyboard.row(back)
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Выбери:', reply_markup=keyboard)


bot.polling(non_stop=True)