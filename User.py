import pickle


def save_users(users):
    with open("users.pkl", "wb") as file:
        pickle.dump(users, file)


def load_users():
    with open("users.pkl", "rb") as file:
        return pickle.load(file)


def print_all(user_ids):
    print("____Id____|___Name___|____Username____|____Last__Name____|")
    for id_i in user_ids:
        print(user_ids[id_i])


class User:
    def __init__(self, user_id, first_name, last_name, username):
        self.__user_id = user_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__username = username

    def __str__(self):
        user_str = f"{self.__user_id: >10}|{self.__first_name: >10}|"
        if self.__username is not None:
            user_str += f"{self.__username: >16}|"
        if self.__last_name is not None:
            user_str += f"{self.__last_name: >16}|"
        return user_str

    def get_name(self):
        return self.__first_name
