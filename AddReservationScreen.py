import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox

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
        
        self.check_out_date_label = QLabel('Дата выселения')
        
        self.submit_button = QPushButton('Добавить')
        self.submit_button.clicked.connect(self.onRegistrationButtonClicked)
        self.submit_button.setFixedHeight(40)
        
        layout = QVBoxLayout()
        layout.addWidget(self.client_label)
        layout.addWidget(self.client_combobox)
        layout.addWidget(self.room_label)
        layout.addWidget(self.room_combobox)
        layout.addWidget(self.check_in_date_label)
        layout.addWidget(self.check_out_date_label)
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
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    registration_form = AddReservationScreen()
    registration_form.show()
    sys.exit(app.exec_())