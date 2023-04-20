# import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import settings as st
import commands as cm
from User import *

# bot -- экземпляр класса Бот
bot = Bot(token=st.token)
dp = Dispatcher(bot)


# Создаём словарь и сохраняем в него пользователей из файла
# users = {}
users = load_users()
print(users)


async def default(*args):
    message = args[2]
    print("default - ", args)
    await bot.forward_message(st.admin_id, message.chat.id, message.message_id)
    await bot.send_message(st.admin_id, str(message))

chats = {"admin": cm.admin_chat,
         "FIF2.2": cm.fif_chat,
         "PM": cm.pm_chat,
         "default": default}


def add_new_update_old(mf):
    if mf.id not in users.keys():
        user = User(mf.id, mf.first_name,
                    mf.username,  # mf.last_name,
                    " " * 11, " " * 9, " " * 13, 0)
        users[mf.id] = user
        save_users(users)
    else:
        users[mf.id].update_data(mf)
        save_users(users)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    mf = message.from_user
    mci = message.chat.id
    add_new_update_old(mf)
    await bot.send_message(mci, "Привет!\nЧтобы увидеть возможные команды попробуйте /help")


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    mci = message.chat.id
    mf = message.from_user
    add_new_update_old(mf)
    key = "default"
    if str(mci) == str(st.admin_id):
        key = "admin"
    elif str(mci) == str(st.fif_chat_id):
        key = "FIF2.2"
    elif int(mci) == int(mf.id):
        key = "PM"

    await chats[key](bot, users, message)

    # print(message)
    # print(f"{users[mfi].get_name()}[id{mfi: >10}] напечатал: \n{mt}")


@dp.message_handler(content_types=['photo', 'video', 'sticker', 'document', 'audio', 'animation'])
async def handle_files(message):
    add_new_update_old(message.from_user)
    if message.chat.id is not st.admin_id:
        await bot.forward_message(st.admin_id, message.chat.id, message.message_id)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
