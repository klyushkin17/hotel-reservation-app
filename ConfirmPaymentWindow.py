import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class ConfirmPaymentWindow(QWidget):
    def __init__(self, conn, clientId, roomId, checkinDate, checkoutDate):
        super().__init__()
        self.initUI()
        self.conn = conn
        self.clientId = clientId

    def initUI(self):
        self.setWindowTitle('Подтверждение оплаты')
        self.setFixedSize(500, 300)

        card_number_label = QLabel('Номер карты:')
        self.card_number_input = QLineEdit()

        card_code_label = QLabel('Код:')
        self.card_code_input = QLineEdit()

        start_year_label = QLabel('Год старта обслуживания:')
        self.start_year_input = QLineEdit()

        end_year_label = QLabel('Год окончания обслуживания:')
        self.end_year_input = QLineEdit()

        confirm_button = QPushButton('Оплатить')
        confirm_button.clicked.connect(self.confirmPayment)
        confirm_button.setFixedHeight(50)
        

        layout = QVBoxLayout()
        layout.addWidget(card_number_label)
        layout.addWidget(self.card_number_input)
        layout.addWidget(card_code_label)
        layout.addWidget(self.card_code_input)
        layout.addWidget(start_year_label)
        layout.addWidget(self.start_year_input)
        layout.addWidget(end_year_label)
        layout.addWidget(self.end_year_input)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def confirmPayment(self):
        card_number = self.card_number_input.text()
        card_code = self.card_code_input.text()
        start_year = self.start_year_input.text()
        end_year = self.end_year_input.text()

        print(f'Processing payment with Card Number: {card_number}, Code: {card_code}, Start Year: {start_year}, End Year: {end_year}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConfirmPaymentWindow()
    window.show()
    sys.exit(app.exec_())