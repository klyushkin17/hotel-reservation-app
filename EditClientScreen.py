import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class EditClientScreen(QWidget):
    def __init__(self, conn, client_id, client_name, client_surname, client_phonenumber, client_email, AdminMainWindow):
        super().__init__()
        self.conn = conn
        self.AdminMainWindow = AdminMainWindow
        self.clientId = client_id
        self.clientName = client_name
        self.clientSurname = client_surname
        self.clientPhonenumber = client_phonenumber
        self.clientEmail = client_email

        self.setWindowTitle('Редактирование записи')
        self.setFixedSize(400, 350)
        
        self.name_label = QLabel('Имя*:')
        self.name_input = QLineEdit()
        self.name_input.setText(client_name)
        
        self.lastname_label = QLabel('Фамилия*:')
        self.lastname_input = QLineEdit()
        self.lastname_input.setText(client_surname)
        
        self.phone_label = QLabel('Номер телефона*:')
        self.phone_input = QLineEdit()
        self.phone_input.setText(client_phonenumber)
        
        self.email_label = QLabel('Почта:')
        self.email_input = QLineEdit()
        self.phone_input.setText(client_email)
        
        self.submit_button = QPushButton('Сохранить изменения')
        self.submit_button.clicked.connect(self.onUpdateButtonClicked)
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
        
    def onUpdateButtonClicked(self):
        name = self.name_input.text()
        lastname = self.lastname_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        if (not phone.isdigit()) and ('@' not in email) and email:
            QMessageBox.warning(self, 'Ошибка', 'Некорректные данные: номер телефона и/или почта')
        else:
            if not phone.isdigit():
                QMessageBox.warning(self, 'Ошибка', 'Некорректно введен номер телефона')
            else:
                if ('@' not in email) and email:
                    QMessageBox.warning(self, 'Ошибка', 'Некорректно введен адрес электронной почты')
                else:
                    if name and lastname and phone:
                        try:
                            with self.conn as conn:
                                with conn.cursor() as cursor:
                                    cursor.execute("SELECT update_client(%s, %s, %s, %s, %s)", (self.clientId, lastname, name, phone, email))
                                    conn.commit()
                                    self.AdminMainWindow.enableAdminMainWindow()
                                    self.close()
                                    QMessageBox.information(self, 'Успех', f'Данные клиента обновлены!')
                        except Exception as e:
                            QMessageBox.warning(self, 'Ошибка', f'Ошибка при обновлении данных клиента: {str(e)}')
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните обязательные поля!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    registration_form = EditClientScreen()
    registration_form.show()
    sys.exit(app.exec_())