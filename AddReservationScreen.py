import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QDateEdit
from PyQt5.QtCore import QDate

class AddReservationScreen(QWidget):
    def __init__(self, conn, AdminMainWindow):
        super().__init__()
        self.conn = conn
        self.AdminMainWindow = AdminMainWindow

        self.setWindowTitle('Добавление бронирования')
        self.setFixedSize(400, 350)
 
        self.client_label = QLabel('Клиент*:')
        self.client_combobox = QComboBox(self)
        
        self.room_label = QLabel('Комната*:')
        self.room_combobox = QComboBox(self)
     
        self.check_in_date_label = QLabel('Дата заселения*:')
        self.check_in_date_edit = QDateEdit()
        self.check_in_date_edit.setCalendarPopup(True)
        self.check_in_date_edit.setDateRange(QDate.currentDate(), QDate(2100, 12, 31))
        
        self.check_out_date_label = QLabel('Дата выселения')
        self.check_out_date_edit = QDateEdit()
        self.check_out_date_edit.setCalendarPopup(True)
        self.check_out_date_edit.setDateRange(QDate.currentDate(), QDate(2100, 12, 31))

        
        self.submit_button = QPushButton('Добавить')
        self.submit_button.clicked.connect(self.onRegistrationButtonClicked)
        self.submit_button.setFixedHeight(40)
        
        layout = QVBoxLayout()
        layout.addWidget(self.client_label)
        layout.addWidget(self.client_combobox)
        layout.addWidget(self.room_label)
        layout.addWidget(self.room_combobox)
        layout.addWidget(self.check_in_date_label)
        layout.addWidget(self.check_in_date_edit)
        layout.addWidget(self.check_out_date_label)
        layout.addWidget(self.check_out_date_edit)
        layout.addWidget(self.submit_button)
        
        self.setLayout(layout)

        self.populate_client_combobox()
        self.populate_room_combobox()

    def closeEvent(self, event):
        self.AdminMainWindow.enableAdminMainWindow()
        event.accept()

    def populate_client_combobox(self):
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT clientid, surname, name, phonenumber FROM client")
                clients = cursor.fetchall()
                for client in clients:
                    self.client_combobox.addItem(f"{client[1]} {client[2]} ({client[3]})", userData=client[0])

    def populate_room_combobox(self):
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT roomid, room FROM room")
                rooms = cursor.fetchall()
                for room in rooms:
                    self.room_combobox.addItem(f"{room[1]}", userData=room[0])
        
    def onRegistrationButtonClicked(self):
        room_name = self.room_combobox.currentText()
        room_id = self.room_combobox.currentData()
        client_id = self.client_combobox.currentData()
        checkin_date = self.check_in_date_edit.date().toPyDate()
        checkout_date = self.check_out_date_edit.date().toPyDate()

        if checkin_date <= checkout_date:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT check_room_availability(%s, %s, %s)", (room_name, checkin_date, checkout_date))
                    result = cursor.fetchone()[0]

                    if result == 'YES':
                        cursor.execute("SELECT add_reservation(%s, %s, %s, %s, %s)", (client_id, room_id, QDate.currentDate().toPyDate(), checkin_date, checkout_date))
                        conn.commit()
                        self.AdminMainWindow.enableAdminMainWindow()
                        QMessageBox.information(self, 'Успех', f'Данные успешно добавлены')
                        self.close()
                    else:
                        QMessageBox.critical(self, 'Error', 'Номер на эти даты уже забронирован')
        else:
            QMessageBox.critical(self, 'Error', 'Некорректно введена дата')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    registration_form = AddReservationScreen()
    registration_form.show()
    sys.exit(app.exec_())