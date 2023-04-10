# import settings as st
from User import *
import time


async def print_help(bot, users, mci, mt):
    await bot.send_message(mci, "Список команд: \n"
                                "===== Для Личных сообщений =====\n"
                                "/start - начать взаимодействие с ботом\n"
                                "/help - показывает список команд\n"
                                "/add_me - Позволяет записать ваши ФИО в БД\n"
                                "/who_am_I - Выводит данные о вас\n"
                                "/time - текущее время\n"
                                "/add_date - добавить свой ДР[TBA]\n"
                                "===== Для чата ФИФ 2.2 =====\n"
                                "/rasp - выводит расписание на всю неделю[TBA]\n"
                                "/today - выводит расписание на сегодня[TBA]\n"
                                "/tommorow - выводит расписание на завтра[TBA]\n"
                                "/say_my_name - Выводит ваши ФИО[TBA]\n"
                                "============ Админские команды ==============\n"
                                "/print_all - выводит всю базу в консоль\n")


async def add_me(bot, users, mci, mt):
    gfm = users[mci].get_fio_mode()
    fio = users[mci].get_full_name()
    if gfm == 3:
        await bot.send_message(mci, f"Я вас уже знаю, вы - {fio}")
    else:
        await bot.send_message(mci, f"Введите ФИО (полностью):")
        users[mci].set_fio_mode(1)


async def who_am_i(bot, users, mci, mt):
    gfm = users[mci].get_fio_mode()
    fio = users[mci].get_full_name()
    if gfm < 2:
        await bot.send_message(mci, "Я вас ещё не знаю, вы можете записать ФИО, воспользовавшись командой /add_me")
    else:
        await bot.send_message(mci, "Вы - " + fio)
        if gfm == 2:
            await bot.send_message(mci, "Если хотите изменить ФИО, введите /add_me")


async def get_time(bot, users, mci, mt):
    tm = time.strftime("%H:%M:%S")
    await bot.send_message(mci, f"{tm}")


pm_commands = ["/help", "/add_me", "/who_am_i", "/time"]
pm_func = [print_help, add_me, who_am_i, get_time]


def find_command(message):
    command = ""
    diff = 0
    if message["entities"] is not None:
        ent = message["entities"]
        for x in ent:
            if x["type"] == "bot_command":
                start = x["offset"] - diff
                end = start + x["length"]
                command = message.text[start:end]
                # await bot.send_message(mci, mt[start:end])
                break
            elif x["type"] == "custom_emoji":
                diff += 1
    return command.lower()


async def write_new_name(bot, users, mci, mt):
    if users[mci].set_full_name(bot, mci, mt):
        save_users(users)
        await bot.send_message(mci, "Данные успешно записаны")
    else:
        await bot.send_message(mci, "Неправильно, попробуй ещё раз")


async def pm_chat(bot, users, message):
    mci = message.chat.id
    mt = message.text
    gfm = users[mci].get_fio_mode()

    command = find_command(message)
    print(command)

    if gfm == 1:
        await write_new_name(bot, users, mci, mt)
        return

    for i in range(len(pm_commands)):
        if command == pm_commands[i]:
            await pm_func[i](bot, users, mci, mt)
            return

    await bot.send_message(mci, "Выполняю " + mt)


async def admin_commands(users, mt):
    if mt == "/print_all":
        print_all(users)

    pass


async def fif_commands(bot, users, mci, mt):
    pass


async def bunker_commands(bot, users, mci, mt):
    pass
