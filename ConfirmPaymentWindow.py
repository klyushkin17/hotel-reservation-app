import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from datetime import datetime
from UserMainWindow import UserMainWindow


class ConfirmPaymentWindow(QWidget):
    def __init__(self, conn, clientId, roomId, checkinDate, checkoutDate, totalPrice, userMainWindow):
        super().__init__()
        self.initUI()
        self.conn = conn
        self.clientId = clientId
        self.roomId = roomId
        self.checkinDate = checkinDate
        self.checkoutDate = checkoutDate
        self.totalPrice = totalPrice
        self.userMainWindow = userMainWindow

    def initUI(self):
        self.setWindowTitle('Подтверждение оплаты')
        self.setFixedSize(500, 300)

        card_number_label = QLabel('Номер карты:')
        self.card_number_input = QLineEdit()

        card_code_label = QLabel('Код:')
        self.card_code_input = QLineEdit()

        end_month_label = QLabel('Месяц конца обслуживания:')
        self.end_month_input = QLineEdit()

        end_year_label = QLabel('Год окончания обслуживания:')
        self.end_year_input = QLineEdit()

        confirm_button = QPushButton('Оплатить')
        confirm_button.clicked.connect(self.confirmPayment)
        confirm_button.setFixedHeight(50)

        self.card_number_input.setValidator(QRegExpValidator(QRegExp("\d{0,16}")))
        self.card_code_input.setValidator(QIntValidator())
        self.end_month_input.setValidator(QIntValidator())
        self.end_year_input.setValidator(QIntValidator())

        self.card_number_input.setMaxLength(16)
        self.card_code_input.setMaxLength(3)
        self.end_month_input.setMaxLength(2)
        self.end_year_input.setMaxLength(4)
        

        layout = QVBoxLayout()
        layout.addWidget(card_number_label)
        layout.addWidget(self.card_number_input)
        layout.addWidget(card_code_label)
        layout.addWidget(self.card_code_input)
        layout.addWidget(end_month_label)
        layout.addWidget(self.end_month_input)
        layout.addWidget(end_year_label)
        layout.addWidget(self.end_year_input)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def confirmPayment(self):
        card_number = self.card_number_input.text()
        card_code = self.card_code_input.text()
        end_month = self.end_month_input.text()
        end_year = self.end_year_input.text()

        if card_number and card_code and end_month and end_year:

            if (int(end_month) < 13) and (len(end_year) == 4):
                current_date = datetime.now().date()
                expiry_date = datetime(int(end_year), int(end_month), 1).date()
                if expiry_date > current_date:
                    try:
                        with self.conn as conn:
                            with conn.cursor() as cursor:
                                cursor.execute("SELECT add_reservation(%s, %s, %s, %s, %s)", (self.clientId, self.roomId, datetime.now().date(), self.checkinDate.toString("yyyy-MM-dd"), self.checkoutDate.toString("yyyy-MM-dd")))
                                cursor.execute("SELECT MAX(reservationid) FROM reservation;")
                                reservation_id = cursor.fetchone()[0]
                                cursor.execute("SELECT add_payment(%s, %s, %s, %s, %s, %s, %s)", ('Card', str(card_number), str(card_code), str(end_month), str(end_year), reservation_id, str(self.totalPrice)))
                                conn.commit()
                                QMessageBox.information(self, 'Успех', 'Мы забронировали для вас номер')
                    except Exception as e:
                        QMessageBox.warning(self, 'Ошибка', f'Упс, произошла ошибка при подтверждении платежа')
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Срок действия карты истек')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Дата введена некорректно')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните обязательные поля!')
        
        self.userMainWindow.unlockUserMainWindow()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConfirmPaymentWindow()
    window.show()
    sys.exit(app.exec_())