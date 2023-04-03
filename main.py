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


# Хэндлер для обработки команды старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Проверка есть ли пользователь в словаре(dictionary):
    if message.from_user.id not in users:
        # Если пользователя нет, создаём новый объект пользователя и добавляем в словарь.
        user = User(message.from_user.id, message.from_user.first_name,
                    message.from_user.last_name, message.from_user.username)
        users[message.from_user.id] = user
        print(user)
        save_users(users)
    await bot.send_message(message.chat.id, "Приветствую")


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    print(f"{users[message.from_user.id].get_name()}[id{message.from_user.id: >10}] напечатал: {message.text}")
    await bot.send_message(message.chat.id, message.text)
    if message.text == "/print_all":
        print_all(users)


@dp.message_handler(content_types=['photo', 'video', 'sticker', 'document', 'audio', 'animation'])
async def handle_files(message):
    if message.chat.id is not st.admin_id:
        await bot.forward_message(st.admin_id, message.chat.id, message.message_id)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
