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
                                                                                                     13))
    for user in users:
        print(users[user])


class User:
    def __init__(self, user_id, first_name, username, real_last_name, real_first_name, real_middle_name):  # last_name
        self.__user_id = user_id
        self.__first_name = first_name
        self.__username = username
        # self.__last_name = last_name
        # ========================================
        self.__real_last_name = real_last_name
        self.__real_first_name = real_first_name
        self.__real_middle_name = real_middle_name

    def __str__(self):
        fst = lambda stroka, dlina: f"{stroka: <{dlina}}|" if stroka is not None else " " * dlina + "|"
        user_str = fst(self.__user_id, 10) + fst(self.__first_name, 10) + fst(self.__username, 18) + \
                   fst(self.__real_last_name, 11) + fst(self.__real_first_name, 9) + fst(self.__real_middle_name, 13)
        return user_str

    def get_name(self):
        return self.__real_first_name
