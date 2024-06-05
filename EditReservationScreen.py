import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QDateEdit
from PyQt5.QtCore import QDate

class EditReservationScreen(QWidget):
    def __init__(self, conn, reservation_id, client_data, client_id, room, check_in_date, check_out_date, AdminMainWindow):
        super().__init__()
        self.conn = conn
        self.AdminMainWindow = AdminMainWindow
        self.reservationId = reservation_id
        self.clientData = client_data
        self.clientId = client_id
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.check_in_date = QDate.fromString(check_in_date, "yyyy-MM-dd")
        self.check_out_date = QDate.fromString(check_out_date, "yyyy-MM-dd")

        self.setWindowTitle('Редактирование записиси')
        self.setFixedSize(400, 350)
 
        self.client_label = QLabel('Клиент*:')
        self.client_combobox = QComboBox(self)
        
        self.room_label = QLabel('Комната*:')
        self.room_combobox = QComboBox(self)
     
        self.check_in_date_label = QLabel('Дата заселения*:')
        self.check_in_date_edit = QDateEdit()
        self.check_in_date_edit.setCalendarPopup(True)
        self.check_in_date_edit.setDateRange(QDate.currentDate(), QDate(2100, 12, 31))
        self.check_in_date_edit.setDate(self.check_in_date)
        
        self.check_out_date_label = QLabel('Дата выселения')
        self.check_out_date_edit = QDateEdit()
        self.check_out_date_edit.setCalendarPopup(True)
        self.check_out_date_edit.setDateRange(QDate.currentDate(), QDate(2100, 12, 31))
        self.check_out_date_edit.setDate(self.check_out_date)

        
        self.submit_button = QPushButton('Сохранить')
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
        self.client_combobox.addItem(str(self.clientData), userData=self.clientData)


    def populate_room_combobox(self):
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT roomid, room FROM room")
                rooms = cursor.fetchall()
                for room in rooms:
                    room_name = room[1]
                    room_id = room[0]
                    self.room_combobox.addItem(room_name, userData=room_id)

                    if room_name == self.room:
                        index = self.room_combobox.findText(room_name)
                        if index != -1:
                            self.room_combobox.setCurrentIndex(index)
        
    def onRegistrationButtonClicked(self):
        room_name = self.room_combobox.currentText()
        room_id = self.room_combobox.currentData()
        checkin_date = self.check_in_date_edit.date().toPyDate()
        checkout_date = self.check_out_date_edit.date().toPyDate()

        if checkin_date <= checkout_date:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT check_room_availability_for_updating(%s, %s, %s, %s)", (room_name, checkin_date, checkout_date, self.reservationId))
                    result = cursor.fetchone()[0]

                    if result == 'YES':
                        cursor.execute("SELECT update_reservation(%s, %s, %s, %s, %s, %s)", (self.reservationId, self.clientId, room_id, QDate.currentDate().toPyDate(), checkin_date, checkout_date))
                        conn.commit()
                        self.AdminMainWindow.enableAdminMainWindow()
                        QMessageBox.information(self, 'Успех', f'Данные успешно обновлены')
                        self.close()
                    else:
                        QMessageBox.critical(self, 'Error', 'Номер на эти даты уже забронирован')
        else:
            QMessageBox.critical(self, 'Error', 'Некорректно введена дата')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    registration_form = EditReservationScreen()
    registration_form.show()
    sys.exit(app.exec_())