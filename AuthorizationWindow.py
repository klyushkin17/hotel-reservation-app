import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from UserMainWindow import UserMainWindow

class AuthorizationWindow(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.setWindowTitle('Авторизация')
        self.setFixedSize(300, 150)
        
        self.phone_label = QLabel('Номер телефона:')
        self.phone_input = QLineEdit()
        
        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.login)
        
        layout = QVBoxLayout()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.login_button)
        
        self.setLayout(layout)
        
    def login(self):
        phone_number = self.phone_input.text()

        if phone_number:
            try:
                with self.conn as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("CALL check_client_by_phonenumber(%s, %s)", (phone_number, None))
                        out_client_id = 0
                        for record in cursor.fetchall():
                            out_client_id = record[0]  
                        conn.commit()
                        print(out_client_id)
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Ошибка при авторизации пользователя')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите номер телефона')
        
        if (out_client_id != None):
            QMessageBox.information(self, 'Успех', f'Добро пожаловать!')
            self.user_main_window = UserMainWindow(self.conn, out_client_id)
            self.user_main_window.show()
            self.close()
        else:
            QMessageBox.information(self, 'Ошибка', 'Пользоватль с таким номером не существует')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth_window = AuthorizationWindow()
    auth_window.show()
    sys.exit(app.exec_())