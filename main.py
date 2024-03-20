from tkinter import Tk, Canvas, Button, Entry, Label, messagebox
from Sidja.game import Game
from Sidja.constants import X_SIZE, Y_SIZE, CELL_SIZE
from Authorization.cypher import vigenere_encrypt
from pathlib import Path

USER_DATA_PATH = Path('users.txt')  # Путь к файлу с данными пользователей
key = "key"

def main():
    main_window = Tk()
    main_window.title('Сиджа')

    def open_auth():
        main_window.destroy()
        auth_window = Tk()
        auth_window.title('Авторизация')

        def handle_auth():
            user_login = input_login.get()
            user_password = input_password.get()
            user_data = {"log": user_login, "pas": user_password}
            user_encrypted = vigenere_encrypt(str(user_data), key)

            with USER_DATA_PATH.open('r', encoding='utf-8') as file:
                existing_users = file.readlines()

            if user_encrypted + '\n' in existing_users:
                auth_window.destroy()
                run_tkinter_app()
            else:
                messagebox.showerror("Ошибка", "Вы ввели неправильный логин или пароль")

        label_login = Label(auth_window, text="Введите логин:")
        label_login.pack()
        input_login = Entry(auth_window)
        input_login.pack()
        label_password = Label(auth_window, text="Введите пароль:")
        label_password.pack()
        input_password = Entry(auth_window, show="*")
        input_password.pack()
        login_btn = Button(auth_window, text="OK", command=handle_auth)
        login_btn.pack()

        auth_window.mainloop()

    def open_reg():
        main_window.destroy()
        reg_window = Tk()
        reg_window.title('Регистрация')

        def handle_reg():
            user_login = new_login.get()
            user_password = new_pass.get()
            user_data = {"log": user_login, "pas": user_password}
            user_encrypted = vigenere_encrypt(str(user_data), key)

            if len(user_login) > 16:
                messagebox.showerror("Ошибка", "Длина логина превысила 16 символов")
            elif len(user_login) == 0:
                messagebox.showerror("Ошибка", "Ничего не введено")
            else:
                with USER_DATA_PATH.open('r', encoding='utf-8') as file:
                    existing_users = file.readlines()

                if user_encrypted + '\n' in existing_users:
                    messagebox.showerror("Ошибка", "Такой аккаунт уже зарегистрирован")
                else:
                    with USER_DATA_PATH.open('a', encoding='utf-8') as file:
                        file.write(user_encrypted + '\n')
                    messagebox.showinfo("Успешная регистрация", "Вы успешно зарегистрированы!")
                    reg_window.destroy()
                    main()

        label_login = Label(reg_window, text="Введите логин:")
        label_login.pack()
        new_login = Entry(reg_window)
        new_login.pack()
        label_password = Label(reg_window, text="Введите пароль:")
        label_password.pack()
        new_pass = Entry(reg_window, show="*")
        new_pass.pack()
        reg_btn = Button(reg_window, text="OK", command=handle_reg)
        reg_btn.pack()

        reg_window.mainloop()

    auth_btn = Button(main_window, text="Авторизация", command=open_auth)
    auth_btn.pack(pady=10)
    reg_btn = Button(main_window, text="Регистрация", command=open_reg)
    reg_btn.pack(pady=10)

    main_window.mainloop()

def run_tkinter_app():
    tk_window = Tk()
    tk_window.title('Сиджа')
    tk_window.resizable(0, 0)

    canvas = Canvas(tk_window, width=CELL_SIZE * X_SIZE, height=CELL_SIZE * Y_SIZE)
    canvas.pack()

    game = Game(canvas, X_SIZE, Y_SIZE)
    canvas.bind("<Motion>", game.mouse_move)
    canvas.bind("<Button-1>", game.mouse_down)

    tk_window.mainloop()

if __name__ == '__main__':
    main()
