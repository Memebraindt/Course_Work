from User import *
import settings as st

import time


async def pm_help(*args):
    bot = args[0]
    mfi = args[2].from_user.id
    await bot.send_message(mfi, "Список команд: \n"
                                "===== Для Личных сообщений =====\n"
                                "/start - начать взаимодействие с ботом\n"
                                "/help - показывает список команд\n"
                                "/who_am_I - Выводит данные о вас\n"
                                "/add_me - Позволяет записать ваши ФИО в БД\n"
                                "/now - что сейчас?\n"
                                "/time - Текущее время\n"
                                "/date - Текущая дата\n"
                                "/week - Какая неделя?\n"
                                "/today - расписание на сегодня\n"
                                "/tomorrow - расписание на завтра\n")


async def fif_help(*args):
    bot = args[0]
    mci = args[2].chat.id
    await bot.send_message(mci, "Список команд: \n"
                                "===== Для чата ФИФ 2.2 =====\n"
                                "/start\n"
                                "/help\n"
                                "/now - что сейчас?\n"
                                "/week - какая неделя?\n"
                                "/today - выводит расписание на сегодня\n"
                                "/tomorrow - выводит расписание на завтра\n"
                                "/say_my_name - выводит ФИО\n")


async def add_me(*args):
    bot = args[0]
    users = args[1]
    mci = args[2].chat.id
    mfi = args[2].from_user.id
    gfm = users[mfi].get_fio_mode()
    fio = users[mfi].get_full_name()
    if gfm == 3:
        await bot.send_message(mci, f"Я вас уже знаю, вы - {fio}")
    else:
        await bot.send_message(mci, f"Введите ФИО (полностью):")
        users[mfi].set_fio_mode(1)


async def who_am_i(*args):
    bot = args[0]
    users = args[1]
    mfi = args[2].from_user.id
    mci = args[2].chat.id
    gfm = users[mfi].get_fio_mode()
    fio = users[mfi].get_full_name()
    if gfm < 2:
        await bot.send_message(mci, "Я вас ещё не знаю, вы можете записать ФИО, воспользовавшись командой /add_me")
    else:
        await bot.send_message(mci, "Вы - " + fio)
        if gfm == 2 and mci == mfi:
            await bot.send_message(mci, "Если хотите изменить ФИО, введите /add_me")


async def get_time(*args):
    bot = args[0]
    mci = args[2].chat.id
    tm = time.strftime("%H:%M:%S")
    await bot.send_message(mci, f"{tm}")


async def get_date(*args):
    bot = args[0]
    mci = args[2].chat.id
    tm = time.strftime("%d.%m.%Y")
    await bot.send_message(mci, f"{tm}")


def get_day():
    return time.localtime(time.time()).tm_wday


def get_week():
    return ((time.localtime(time.time()).tm_yday - 2) // 7 + 1) % 2


async def get_schedule(*args):
    bot = args[0]
    mci = args[2].chat.id
    command = args[3]
    day = get_day()
    week = get_week()
    if command == "/tomorrow":
        day = (day+1) % 7
        if day == 0:
            week = 1 - week
    await bot.send_message(mci, st.wday[day])
    f = ""
    for key in st.fif_schedule[day].keys():
        stroka = st.fif_schedule[day][key]
        if key is None:
            await bot.send_message(mci, "`Пар нет`", parse_mode="MarkdownV2")
            return
        if not week and len(stroka) == 2:
            stroka = stroka[1]
        else:
            stroka = stroka[0]
        if stroka == "":
            stroka = "Нет пары"
        f += f"`{key}. {stroka}`\n"
    await bot.send_message(mci, f, parse_mode="MarkdownV2")


async def what_is_now(*args):
    bot = args[0]
    mci = args[2].chat.id
    command = args[3]
    day = get_day()
    if command == "/tomorrow":
        day = (day+1) % 7
    week = get_week()
    cur_time = str(time.strftime("%H:%M:%S"))
    para = 0
    if "08:30:00" <= cur_time < "10:05:00":
        para = 1
    elif "10:15:00" <= cur_time < "11:55:00":
        para = 2
    elif "12:15:00" <= cur_time < "13:55:00":
        para = 3
    elif "14:05:00" <= cur_time < "15:45:00":
        para = 4
    elif "15:45:00" <= cur_time <= "23:59:59" or "00:00:00" <= cur_time <= "08:29:59":
        para = 5
        await bot.send_message(mci, f"Отдых")

    if para == 0:
        await bot.send_message(mci, f"Перерыв")
    f = ""
    if 0 < para < 5:
        if para in st.fif_schedule[day].keys():
            stroka = st.fif_schedule[day][para]
        else:
            stroka = ["Пары нет"]

        if not week and len(stroka) == 2:
            stroka = stroka[1]
        else:
            stroka = stroka[0]
        f += f"`{para}. {stroka}`\n"
        await bot.send_message(mci, f, parse_mode="MarkdownV2")


async def send_week(*args):
    bot = args[0]
    mci = args[2].chat.id
    gw = get_week()
    if gw == 1:
        await bot.send_message(mci, "Числитель, верхняя, нечёт")
    else:
        await bot.send_message(mci, "Знаменатель, нижняя, чёт")

rasp_time_ = [["00:00:00", "08:30:00", "10:20:00", "12:20:00", "14:10:00", "16:00:00"],
              ["08:29:59", "10:05:00", "11:55:00", "13:55:00", "15:45:00", "23:59:59"]]

pm_commands = ["/help", "/who_am_i", "/add_me", "/time", "/date", "/today", "/tomorrow", "/week", "/now"]
pm_func = [pm_help, who_am_i, add_me, get_time, get_date, get_schedule, get_schedule, send_week, what_is_now]

fif_commands = ["/help", "/say_my_name", "/today", "/tomorrow", "/week", "/now"]
fif_func = [fif_help, who_am_i, get_schedule, get_schedule, send_week, what_is_now]


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
                pos_dog = command.find("@")
                print(pos_dog)
                if pos_dog != -1:
                    command = command[:pos_dog]
                break
            elif x["type"] == "custom_emoji":
                diff += 1
    return command.lower()


async def write_new_name(bot, users, message):
    mci = message.chat.id
    mt = message.text
    mfi = message.from_user.id
    if users[mfi].set_full_name(mt):
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
        await write_new_name(bot, users, message)
        return

    for i in range(len(pm_commands)):
        if command == pm_commands[i]:
            await pm_func[i](bot, users, message, command)
            return

    # await bot.send_message(mci, "Выполняю " + mt)


async def admin_chat(bot, users, message):
    mt = message.text
    if mt == "/print_all":
        print_all(users)

    pass


async def fif_chat(bot, users, message):
    mci = message.chat.id
    mt = message.text
    command = find_command(message)
    print(command)
    for i in range(len(fif_commands)):
        if command == fif_commands[i]:
            await fif_func[i](bot, users, message, command)
            return
