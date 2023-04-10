import pickle


def save_users(users):
    with open("users.pkl", "wb") as file:
        pickle.dump(users, file)


def load_users():
    with open("users.pkl", "rb") as file:
        return pickle.load(file)


def print_all(users):
    fs = lambda stroka, dlina: f"{stroka:_^{dlina}}|"
    print(fs("Id", 10) + fs("Name", 10) + fs("Username", 18) + fs("Фамилия", 11) + fs("Имя", 9) + fs("Отчество",
                                                                                                     13) + "sf|")
    for user in users:
        print(users[user])


class User:
    def __init__(self, user_id, first_name, username, real_last_name, real_first_name, real_middle_name,
                 set_fio):  # last_name
        self.__user_id = user_id
        self.__first_name = first_name
        self.__username = username
        # self.__last_name = last_name
        # ========================================
        self.__real_last_name = real_last_name
        self.__real_first_name = real_first_name
        self.__real_middle_name = real_middle_name
        self.__set_fio = set_fio
        # 0 - не установлено,
        # 1 - ожидает установки,
        # 2 - установлено, может быть изменено,
        # 3 - установлено, не может быть изменено

    def __str__(self):
        fst = lambda stroka, dlina: f"{stroka: <{dlina}}|" if stroka is not None else " " * dlina + "|"
        user_str = fst(self.__user_id, 10) + fst(self.__first_name, 10) + fst(self.__username, 18) + \
                   fst(self.__real_last_name, 11) + fst(self.__real_first_name, 9) + \
                   fst(self.__real_middle_name, 13) + fst(self.__set_fio, 2)
        return user_str

    def update_data(self, mf):
        self.__username = mf.username
        self.__first_name = mf.first_name

    def get_full_name(self):
        return self.__real_last_name + " " + self.__real_first_name + " " + self.__real_middle_name

    def set_full_name(self, bot, mci, mt):
        lst = mt.split()
        if len(lst) == 3:
            self.__real_last_name = str(lst[0]).capitalize()
            self.__real_first_name = str(lst[1]).capitalize()
            self.__real_middle_name = str(lst[2]).capitalize()
            self.set_fio_mode(2)
            return True
        else:
            return False

    def set_fio_mode(self, mode):
        self.__set_fio = mode

    def get_fio_mode(self):
        return self.__set_fio
