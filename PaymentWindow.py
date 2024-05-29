from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QGridLayout, QWidget, QApplication
from PyQt5.QtCore import Qt
from ConfirmPaymentWindow import ConfirmPaymentWindow

class PaymentWindow(QWidget):
    def __init__(self, room_id, room, capacity, price, checkin_date, checkout_date, conn, clientId, userMainWindow):
        super().__init__()

        self.conn = conn
        self.clientId = clientId
        self.roomId = room_id
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date
        self.userMainWindow = userMainWindow

        layout = QGridLayout() 
        self.setWindowTitle("Оплата")
        self.setFixedSize(600, 400)
        self.setLayout(layout)

        total_days = checkin_date.daysTo(checkout_date)
        self.total_price = int(price) * total_days

        room_label = QLabel(f"Номер комнаты: {room}")
        capacity_label = QLabel(f"Вместимость: {capacity}")
        price_label = QLabel(f"Цена: {price} рублей")
        checkin_label = QLabel(f"Дата въезда: {checkin_date.toString('yyyy-MM-dd')}")
        checkout_label = QLabel(f"Дата выезда: {checkout_date.toString('yyyy-MM-dd')}")
        total_price_label = QLabel(f"ИТОГО: {self.total_price} рублей")

        room_label.setStyleSheet('font-size: 16pt;')
        capacity_label.setStyleSheet('font-size: 16pt;')
        price_label.setStyleSheet('font-size: 16pt;')
        checkin_label.setStyleSheet('font-size: 16pt;')
        checkout_label.setStyleSheet('font-size: 16pt;')
        total_price_label.setStyleSheet('font-size: 16pt;')

        layout.addWidget(room_label, 0, 0)
        layout.addWidget(capacity_label, 1, 0)
        layout.addWidget(price_label, 2, 0)
        layout.addWidget(checkin_label, 3, 0)
        layout.addWidget(checkout_label, 4, 0)
        layout.addWidget(total_price_label, 3, 1)

        self.pay_button = QPushButton('Оплатить', self)
        self.pay_button.clicked.connect(self.onPayButtonClicked)
        self.pay_button.setFixedHeight(50)
        layout.addWidget(self.pay_button, 4, 1)  

    def onPayButtonClicked(self):
        self.confirm_payment_window = ConfirmPaymentWindow(self.conn, self.clientId, self.roomId, self.checkin_date, self.checkout_date, self.total_price, self.userMainWindow)
        self.confirm_payment_window.show()
        self.close()
        self.userMainWindow.lockUserMainWindow()
    
    def closeEvent(self, event):
        self.userMainWindow.unlockUserMainWindow()
        event.accept()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = PaymentWindow()
    window.show()
    sys.exit(app.exec_())