# import settings as st
from User import *


async def pm_chat(bot, users, mci, mt):
    FIO = users[mci].get_full_name()
    gfm = users[mci].get_fio_mode()
    if gfm == 1:
        users[mci].set_full_name(mt)
        users[mci].set_fio_mode(2)
        save_users(users)
        await bot.send_message(mci, "Хорошо, записал")
    elif mt[:5] == "/help":
        await bot.send_message(mci, "Список команд: \n"
                                    "/rasp - выводит расписание на всю неделю\n"
                                    "/today - выводит расписание на сегодня\n"
                                    "/tommorow - выводит расписание на завтра\n"
                                    "/add_me - Позволяет записать ваши ФИО в БД\n"
                                    "/who_am_I или /кто_я - Выводит данные о вас\n"
                                    "/print_all - админская команда, выводит всю базу в консоль\n"
                                    "/help - показывает список команд \n")
    elif mt[:7] == "/add_me":
        if gfm == 3:
            await bot.send_message(mci, f"Я вас уже знаю, вы - {FIO}")
        else:
            await bot.send_message(mci, f"Введите ФИО:")
            users[mci].set_fio_mode(1)
    elif mt[:9] == "/who_am_i" or mt[:4] == "/кто":
        if gfm < 2:
            await bot.send_message(mci, "Я вас ещё не знаю, вы можете записать ФИО воспользовавшись командой /add_me")
        else:
            await bot.send_message(mci, "Вы - " + FIO)
            if gfm == 2:
                await bot.send_message(mci,
                                       "Если хотите изменить ФИО, введите /add_me")
    else:
        await bot.send_message(mci, "Выполняю " + mt)


async def admin_commands(users, mt):
    if mt == "/print_all":
        print_all(users)

    pass


async def fif_commands():

    pass


async def bunker_commands():

    pass
