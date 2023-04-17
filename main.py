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
# print_all(users)


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
    forward_flag = False
    mci = message.chat.id
    mf = message.from_user
    # mt = message.text.lower()
    add_new_update_old(mf)
    is_admin = (str(mci) == str(st.admin_id))
    is_fif_chat = (str(mci) == str(st.fif_chat_id))

    if mci == mf.id:
        await cm.pm_chat(bot, users, message)
        if not is_admin:
            await bot.forward_message(st.admin_id, mci, message.message_id)
            forward_flag = True

    if is_admin:
        await cm.admin_chat(bot, users, message)
        forward_flag = True
    elif is_fif_chat:
        await cm.fif_chat(bot, users, message)
        forward_flag = True

    if not forward_flag:
        await bot.forward_message(st.admin_id, mci, message.message_id)
        await bot.send_message(st.admin_id, str(message))

    # else:
    #     await bot.forward_message(st.admin_id, mci, message.message_id)
    # print(message)
    # print(f"{users[mfi].get_name()}[id{mfi: >10}] напечатал: \n{mt}")


@dp.message_handler(content_types=['photo', 'video', 'sticker', 'document', 'audio', 'animation'])
async def handle_files(message):
    add_new_update_old(message.from_user)
    if message.chat.id is not st.admin_id:
        await bot.forward_message(st.admin_id, message.chat.id, message.message_id)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
