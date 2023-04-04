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
print_all(users)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    mf = message.from_user
    mfi = int(mf.id)
    if mfi not in users.keys():
        user = User(mfi, mf.first_name,
                    mf.username,  # message.from_user.last_name,
                    " " * 11, " " * 9, " " * 13)
        users[mfi] = user
        save_users(users)
    # else:
    #     Check_and_update()
    await bot.send_message(message.chat.id, "Приветствую")
    await bot.send_message(message.chat.id, "Возможные команды: /help /print_all")


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    mci = message.chat.id
    mfi = int(message.from_user.id)
    mt = message.text
    is_adm_comm = (str(mci) == str(st.admin_id))
    is_bunker_chat = (str(mci) == str(st.bunker_chat_id))
    is_fif_chat = (str(mci) == str(st.fif_chat_id))
    if is_adm_comm:
        await cm.admin_commands(users, mt)
    elif is_fif_chat:
        await cm.fif_commands()
    elif is_bunker_chat:
        await cm.bunker_commands()
    else:
        await bot.forward_message(st.admin_id, mci, message.message_id)
        await bot.send_message(mci, mt)
    print(message)
    # print(f"{users[mfi].get_name()}[id{mfi: >10}] напечатал: \n{mt}")


@dp.message_handler(content_types=['photo', 'video', 'sticker', 'document', 'audio', 'animation'])
async def handle_files(message):
    if message.chat.id is not st.admin_id:
        await bot.forward_message(st.admin_id, message.chat.id, message.message_id)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
