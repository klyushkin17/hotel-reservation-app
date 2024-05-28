import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from AuthorizationWindow import AuthorizationWindow
from UserMainWindow import UserMainWindow

class RegistrationWindow(QWidget):
    def __init__(self, conn, IS_ADMIN):
        super().__init__()
        self.conn = conn

        self.setWindowTitle('Регистрация')
        self.setFixedSize(300, 400)
        
        self.name_label = QLabel('Имя*:')
        self.name_input = QLineEdit()
        
        self.lastname_label = QLabel('Фамилия*:')
        self.lastname_input = QLineEdit()
        
        self.phone_label = QLabel('Номер телефона*:')
        self.phone_input = QLineEdit()
        
        self.email_label = QLabel('Почта:')
        self.email_input = QLineEdit()
        
        self.auth_label = QLabel('<a href="#">Уже есть аккаунт?</a>')
        self.auth_label.setOpenExternalLinks(False)
        self.auth_label.linkActivated.connect(self.onAuthorizationLinkClicked)
        
        self.submit_button = QPushButton('Зарегистрироваться')
        self.submit_button.clicked.connect(self.onRegistrationButtonClicked)
        
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.lastname_label)
        layout.addWidget(self.lastname_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.auth_label)
        
        self.setLayout(layout)
        
    def onRegistrationButtonClicked(self):
        name = self.name_input.text()
        lastname = self.lastname_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        if (not phone.isdigit()) and ('@' not in email) and email:
            QMessageBox.warning(self, 'Ошибка', 'Некорректно введены номер и почта')
        else:
            if not phone.isdigit():
                QMessageBox.warning(self, 'Ошибка', 'Некорректно введен номер')
            else:
                if ('@' not in email) and email:
                    QMessageBox.warning(self, 'Ошибка', 'Некорректно введена почка')
                else:
                    if name and lastname and phone:
                        try:
                            with self.conn as conn:
                                with conn.cursor() as cursor:
                                    cursor.execute("CALL insert_client_get_last_index_transaction(%s, %s, %s, %s, %s)", (lastname, name, phone, email, None))
                                    out_client_id = 0
                                    for record in cursor.fetchall():
                                        out_client_id = record[0]  
                                    conn.commit()
                                    QMessageBox.information(self, 'Успех', f'Добро пожаловать!')
                        except Exception as e:
                            QMessageBox.warning(self, 'Ошибка', f'Пользователь с таким номером телефона уже существует')
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните обязательные поля!')
        
        self.user_main_window = UserMainWindow(self.conn, out_client_id)
        self.user_main_window.show()
        self.close()
           
    def onAuthorizationLinkClicked(self, url):
        self.close()
        self.auth_window = AuthorizationWindow(self.conn)
        self.auth_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    registration_form = RegistrationWindow()
    registration_form.show()
    sys.exit(app.exec_())