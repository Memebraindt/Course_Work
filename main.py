# import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import settings as st
from User import *

# bot -- экземпляр класса Бот
bot = Bot(token=st.token)
dp = Dispatcher(bot)


# Создаём словарь и сохраняем в него пользователей из файла
# users = {}
users = load_users()
print(users)
print_all(users)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if message.from_user.id not in users.keys():
        user = User(str(message.from_user.id), message.from_user.first_name,
                    message.from_user.username,  # message.from_user.last_name,
                    " " * 11, " " * 9, " " * 13)
        users[message.from_user.id] = user
        save_users(users)
    # else:
    #     Check_and_update()
    await bot.send_message(message.chat.id, "Приветствую")
    await bot.send_message(message.chat.id, "Возможные команды: /help /print_all")


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    print(message)
    mfi = int(message.from_user.id)
    mt = message.text
    mci = message.chat.id
    # print(f"{users[mfi].get_name()}[id{mfi: >10}] напечатал: \n{mt}")
    if mt == "/print_all":
        print_all(users)
    else:
        await bot.send_message(mci, mt)


@dp.message_handler(content_types=['photo', 'video', 'sticker', 'document', 'audio', 'animation'])
async def handle_files(message):
    if message.chat.id is not st.admin_id:
        await bot.forward_message(st.admin_id, message.chat.id, message.message_id)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
