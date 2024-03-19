from tkinter import Tk, Canvas
from Sidja.game import Game
from Sidja.constants import X_SIZE, Y_SIZE, CELL_SIZE

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from Authorization import autorization
from Authorization import register
from Authorization import login
from Authorization.cypher import *

WIDTH, HEIGHT = 1000, 800
ROWS, COLS = 8, 10
SQUARE_SIZE = WIDTH//COLS

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
global input_log, input_pass, xor

app = QApplication(sys.argv)

def main():
    global main_window
    global main_ui
    main_window = QMainWindow()
    main_ui = autorization.Ui_MainWindow()
    main_ui.setupUi(main_window)
    main_window.show()
    main_ui.pushButton.clicked.connect(open_auth)
    main_ui.pushButton_2.clicked.connect(open_reg)

def open_auth():
    global auth_window
    global auth_ui
    main_window.close()
    auth_window = QMainWindow()
    auth_ui = login.Ui_authorization()
    auth_ui.setupUi(auth_window)
    auth_window.show()
    auth_ui.exitlog.clicked.connect(exit_click_auth)
    auth_ui.loginbtn.clicked.connect(handle_auth)

def open_reg():
    global reg_window
    global reg_ui
    main_window.close()
    reg_window = QMainWindow()
    reg_ui = register.Ui_registration()
    reg_ui.setupUi(reg_window)
    reg_window.show()
    reg_ui.exitreg.clicked.connect(exit_click_reg)
    reg_ui.regbtn.clicked.connect(handle_reg)

from pathlib import Path

USER_DATA_PATH = Path('users.txt')  # Путь к файлу с данными пользователей

def handle_reg():
    user_login = reg_ui.new_login.text()
    user_password = reg_ui.new_pass.text()
    user_data = {"log": user_login, "pas": user_password}
    user_encrypted = vigenere_encrypt(str(user_data), key)

    if len(user_login) > 16:
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Ошибка")
        msgBox.setText("Длина логина превысила 16 символов")
        msgBox.exec()
    elif len(user_login) == 0:
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Ошибка")
        msgBox.setText("Ничего не введено")
        msgBox.exec()
    else:
        # Открыть файл на чтение (режим 'r')
        with USER_DATA_PATH.open('r', encoding='utf-8') as file:
            existing_users = file.readlines()

        if user_encrypted + '\n' in existing_users:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Ошибка")
            msgBox.setText("Такой аккаунт уже зарегистрирован")
            msgBox.exec()
        else:
            with USER_DATA_PATH.open('a', encoding='utf-8') as file:
                file.write(user_encrypted + '\n')
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Успешная регистрация")
            msgBox.setText("Вы успешно зарегистрированы!")
            msgBox.exec()
            reg_window.close()
            main()

def handle_auth():
    user_login = auth_ui.input_login.text()
    user_password = auth_ui.input_password.text()
    user_data = {"log": user_login, "pas": user_password}
    user_encrypted = vigenere_encrypt(str(user_data), key)

    with USER_DATA_PATH.open('r', encoding='utf-8') as file:
        existing_users = file.readlines()

    if user_encrypted + '\n' in existing_users:
        main_window.close()
        auth_window.close()
        run_tkinter_app()
    else:
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Ошибка")
        msgBox.setText("Вы ввели неправильный логин или пароль")
        msgBox.exec()


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

def exit_click_reg():
    reg_window.close()
    main_window.show()

def exit_click_auth():
    auth_window.close()
    main_window.show()

main()

app.exec()

if __name__ == '__main__':
    main()
