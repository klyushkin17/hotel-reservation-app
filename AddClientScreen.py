import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class AddClientScreen(QWidget):
    def __init__(self, conn, AdminMainWindow):
        super().__init__()
        self.conn = conn
        self.AdminMainWindow = AdminMainWindow

        self.setWindowTitle('Добавление клиента')
        self.setFixedSize(400, 350)
        
        self.name_label = QLabel('Имя*:')
        self.name_input = QLineEdit()
        
        self.lastname_label = QLabel('Фамилия*:')
        self.lastname_input = QLineEdit()
        
        self.phone_label = QLabel('Номер телефона*:')
        self.phone_input = QLineEdit()
        
        self.email_label = QLabel('Почта:')
        self.email_input = QLineEdit()
        
        self.submit_button = QPushButton('Добавить')
        self.submit_button.clicked.connect(self.onRegistrationButtonClicked)
        self.submit_button.setFixedHeight(40)
        
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
        
        self.setLayout(layout)

    def closeEvent(self, event):
        self.AdminMainWindow.enableAdminMainWindow()
        event.accept()
        
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
                    QMessageBox.warning(self, 'Ошибка', 'Некорректно введена почта')
                else:
                    if name and lastname and phone:
                        try:
                            with self.conn as conn:
                                with conn.cursor() as cursor:
                                    cursor.execute("CALL insert_client_get_last_index_transaction(%s, %s, %s, %s, %s)", (lastname, name, phone, email, None)) 
                                    conn.commit()
                                    self.AdminMainWindow.enableAdminMainWindow()
                                    self.close()
                                    QMessageBox.information(self, 'Успех', f'Клиент добавлен!')
                        except Exception as e:
                            QMessageBox.warning(self, 'Ошибка', f'Пользователь с таким номером телефона уже существует')
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните обязательные поля!')
       

if __name__ == '__main__':
    app = QApplication(sys.argv)
    registration_form = AddClientScreen()
    registration_form.show()
    sys.exit(app.exec_())