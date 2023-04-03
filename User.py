import pickle


def save_users(users):
    with open("users.pkl", "wb") as file:
        pickle.dump(users, file)


def load_users():
    with open("users.pkl", "rb") as file:
        return pickle.load(file)


def print_all(users):
    s1 = "Id"
    s = f"{s1:_^10}|"
    s1 = "Name"
    s += f"{s1:_>10}|"
    s1 = "Username"
    s += f"{s1:_^18}|"
    s1 = "Last_Name"
    s += f"{s1:_^18}|"
    print(s)
    # print("____Id____|___Name___|_____Username_____|____Last__Name____|")
    for user in users:
        print(users[user])


class User:
    def __init__(self, user_id, first_name, username, last_name, real_first_name, real_middle_name, real_last_name, ):
        self.__user_id = user_id
        self.__first_name = first_name
        self.__username = username
        self.__last_name = last_name
        self.__real_first_name = real_first_name
        self.__real_middle_name = real_middle_name
        self.__real_last_name = real_last_name

    def __str__(self):
        user_str = f"{self.__user_id: >10}|{self.__first_name: >10}|"
        if self.__username is not None:
            user_str += f"{self.__username: >18}|"
        else:
            user_str += " " * 18 + "|"

        if self.__last_name is not None:
            user_str += f"{self.__last_name: >16}|"
        else:
            user_str += " " * 18 + "|"
        # user_str += self.__real_first_name

        return user_str

    def get_name(self):
        return self.__first_name
