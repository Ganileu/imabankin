wqimport json
import logging
import os
import re


class Bank:
    def __init__(self):
        self.clients_data = self.load_clients()
        self.current_user = None

    def load_clients(self):
        try:
            with open("clients.json", "r") as file:
                clients = json.load(file)
                return clients
        except FileNotFoundError:
            return {"users": []}
        except Exception as e:
            logging.error(f"Ошибка при загрузке данных: {e}")
            return {"users": []}

    def save_clients(self):
        try:
            with open("clients.json", "w") as file:
                json.dump(self.clients_data, file, indent=2)
        except Exception as e:
            logging.error(f"Ошибка при сохранении данных: {e}")

    def validate_login_password(self, username, password):
        login_pattern = r"^[a-zA-Z0-9_-]{3,20}$"
        password_pattern = r"^[a-zA-Z0-9]{6,20}$"

        if not re.match(login_pattern, username) or not re.match(password_pattern, password):
            logging.error("Неверный логин или пароль")
            print("Неверный логин или пароль")
            return False

        if username.isdigit():
            logging.error("Имя пользователя не может быть числом")
            print("Имя пользователя не может быть числом")
            return False

        return True

    def login_user(self):
        while True:
            try:
                user_login = input("Введите логин: ")
                user_password = input("Введите пароль: ")

                if self.validate_login_password(user_login, user_password):
                    for user in self.clients_data["users"]:
                        if user["username"] == user_login and user["password"] == user_password:
                            print("Вход в систему успешно выполнен")
                            self.current_user = user
                            return True
                    print("Неверный логин или пароль. Попробуйте еще раз")
            except Exception as e:
                logging.error(f"Ошибка при входе в систему: {e}")
                print("Произошла ошибка при входе в систему")

    def signup(self):
        try:
            new_username = input("Введите логин: ")
            new_password = input("Введите пароль (минимум 6 символов): ")

            if self.validate_login_password(new_username, new_password):
                for user in self.clients_data["users"]:
                    if user["username"] == new_username:
                        print("Ошибка: Пользователь с таким логином уже существует.")
                        return False

                new_user = {
                    "username": new_username,
                    "password": new_password,
                    "balance": 0,
                    "transaction_history": []
                }
                self.clients_data["users"].append(new_user)
                self.save_clients()
                transaction = f"Регистрация нового пользователя: {new_username}"
                new_user["transaction_history"].append(transaction)
                print("Регистрация нового пользователя успешно выполнена")
                return True
        except Exception as e:
            logging.error(f"Ошибка при регистрации пользователя: {e}")
            print("Произошла ошибка при регистрации")
            return False

    def deposit(self, amount):
        try:
            if amount < 0:
                logging.warn("Сумма пополнения не может быть отрицательной")
                print("Сумма пополнения не может быть отрицательной")
                return False

            self.current_user["balance"] += amount
            print(f"Счет успешно пополнен. Текущий баланс: {self.current_user['balance']}")
            return True
        except Exception as e:
            logging.error(f"Ошибка при пополнении счета: {e}")
            return False

    def view_balance(self):
        print(f"Текущий баланс счета: {self.current_user['balance']}")

    def view_transaction_history(self):
        print("История транзакций: ")
        for transaction in self.current_user.get("transaction_history", []):
            print(transaction)

    def transfer(self, receiver, amount):
        try:
            if amount < 0:
                logging.warn("Сумма перевода не может быть отрицательной")
                print("Сумма перевода не может быть отрицательной")
                return False

            if self.current_user["balance"] >= amount:
                self.current_user["balance"] -= amount
                receiver["balance"] += amount

                sender_transaction = f"Перевод пользователю {receiver['username']}: -{amount}"
                receiver_transaction = f"Получение перевода от {self.current_user['username']}: +{amount}"

                self.current_user.setdefault("transaction_history", []).append(sender_transaction)
                receiver.setdefault("transaction_history", []).append(receiver_transaction)

                print("Перевод выполнен успешно")
                return True
            else:
                print("Недостаточно средств для перевода")
                return False

        except Exception as e:
            logging.error(f"Ошибка при выполнении перевода: {e}")
            return False

    def logout(self):
        try:
            if self.current_user:
                current_user_index = next(
                    (index for index, user in enumerate(self.clients_data["users"])
                     if user["username"] == self.current_user["username"]), None)
                if current_user_index is not None:
                    self.clients_data["users"][current_user_index] = self.current_user
                    self.save_clients()
                    self.current_user = None
        except Exception as e:
            logging.error(f"Ошибка при выходе из системы: {e}")
