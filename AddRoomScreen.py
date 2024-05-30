import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator

class AddRooomScreen(QWidget):
    def __init__(self, conn, AdminMainWindow):
        super().__init__()
        self.conn = conn
        self.AdminMainWindow = AdminMainWindow

        self.setWindowTitle('Добавление номера')
        self.setFixedSize(400, 350)
        
        self.room_label = QLabel('Номер*:')
        self.room_input = QLineEdit()
        
        self.capacity_label = QLabel('Вместимость*:')
        self.capacity_input = QLineEdit()
        capacity_validator = QRegExpValidator(QRegExp("[0-9]+"))
        self.capacity_input.setValidator(capacity_validator)
        
        self.price_label = QLabel('Цена*:')
        self.price_input = QLineEdit()
        price_validator = QRegExpValidator(QRegExp("[0-9]+"))  
        self.price_input.setValidator(price_validator)
        
        self.submit_button = QPushButton('Добавить')
        self.submit_button.clicked.connect(self.onRegistrationButtonClicked)
        self.submit_button.setFixedHeight(40)
        
        layout = QVBoxLayout()
        layout.addWidget(self.room_label)
        layout.addWidget(self.room_input)
        layout.addWidget(self.capacity_label)
        layout.addWidget(self.capacity_input)
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)
        layout.addWidget(self.submit_button)
        
        self.setLayout(layout)

    def closeEvent(self, event):
        self.AdminMainWindow.enableAdminMainWindow()
        event.accept()
        
    def onRegistrationButtonClicked(self):
        room = self.room_input.text()
        capacity = self.capacity_input.text()
        price = self.price_input.text()

        if room and capacity and price:
            try:
                with self.conn as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT add_room(%s, %s, %s)", (room, capacity, price)) 
                        conn.commit()
                        self.AdminMainWindow.enableAdminMainWindow()
                        self.close()
                        QMessageBox.information(self, 'Успех', f'Номер добавлен!')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Такой номер уже добавлена')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все поля!')
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    registration_form = AddRooomScreen()
    registration_form.show()
    sys.exit(app.exec_())