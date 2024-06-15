import logging
from models import Bank

logging.basicConfig(level=logging.INFO,
                    filename='errors.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    bank = Bank()

    while True:
        try:
            if bank.current_user is None:
                print("1. Вход в систему")
                print("2. Регистрация")
                print("3. Выход")
                choice = input("Выберите действие (1|2|3): ")

                if choice == "1":
                    bank.login_user()
                elif choice == "2":
                    bank.signup()
                elif choice == "3":
                    break
                else:
                    logging.warn("Неверный выбор. Попробуйте еще раз.")
            else:
                print("Главное меню:")
                print("1. Пополнение счета")
                print("2. Просмотр баланса")
                print("3. Просмотр история действий")
                print("4. Перевод между счетами")
                print("5. Выход")
                choice = input("Выберите услугу (1|2|3|4|5): ")

                if choice == "1":
                    amount = int(input("Введите сумму для пополнения счета: "))
                    bank.deposit(amount)
                elif choice == "2":
                    bank.view_balance()
                elif choice == "3":
                    bank.view_transaction_history()
                elif choice == "4":
                    transfer_username = input("Введите логин получателя: ")
                    amount = int(input("Введите сумму для перевода: "))
                    bank.transfer(transfer_username, amount)
                elif choice == "5":
                    bank.logout()
                else:
                    logging.warn("Неверный выбор. Попробуйте еще раз.")
        except Exception as e:
            logging.error(f"Общая ошибка: {e}")

    print("До скорого!")

if __name__ == "__main__":
    main()
