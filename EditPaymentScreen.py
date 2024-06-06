import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QLineEdit, QPushButton, QMessageBox, QLabel
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from datetime import datetime

class EditPaymentScreen(QWidget):
    def __init__(self, conn, AdminMainWindow, payment_id, payment_type, card_number, card_code, mounth, year, total_price, reservation_id):
        super().__init__()
        self.conn = conn
        self.AdminMainWindow = AdminMainWindow
        self.paymentId = payment_id
        self.paymentType = payment_type
        self.cardNumber = card_number
        self.cardCode = card_code
        self.mounth = mounth
        self.year = year
        self.totalPrice = total_price
        self.reservationId = reservation_id

        self.setWindowTitle("Редактирование")
        self.setFixedSize(400, 350)

        layout = QVBoxLayout()

        self.radio_button = QRadioButton("Оплата наличными")
        if self.paymentType == 'Cash':
            self.radio_button.setChecked(True)
        else:
            self.radio_button.setChecked(False)

        self.card_number_label = QLabel("Номер карты:")
        layout.addWidget(self.card_number_label)
        self.card_number_edit = QLineEdit()
        self.card_number_edit.setPlaceholderText("Номер карты")
        if self.paymentType != 'Cash':
            self.card_number_edit.setText(card_number)
        layout.addWidget(self.card_number_edit)

        self.card_code_label = QLabel("Код карты:")
        layout.addWidget(self.card_code_label)
        self.card_code_edit = QLineEdit()
        self.card_code_edit.setPlaceholderText("Код карты")
        if self.paymentType != 'Cash':
            self.card_code_edit.setText(card_code)
        layout.addWidget(self.card_code_edit)

        self.expire_month_label = QLabel("Месяц конца обслуживания:")
        layout.addWidget(self.expire_month_label)
        self.expire_month_edit = QLineEdit()
        self.expire_month_edit.setPlaceholderText("Месяц конца обслуживания")
        if self.paymentType != 'Cash':
            self.expire_month_edit.setText(mounth)
        layout.addWidget(self.expire_month_edit)

        self.expire_year_label = QLabel("Год конца обслуживания:")
        layout.addWidget(self.expire_year_label)
        self.expire_year_edit = QLineEdit()
        self.expire_year_edit.setPlaceholderText("Год конца обслуживания")
        if self.paymentType != 'Cash':
            self.expire_year_edit.setText(year)
        layout.addWidget(self.expire_year_edit)

        self.amount_label = QLabel("Сумма:")
        layout.addWidget(self.amount_label)
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Сумма")
        self.amount_edit.setText(total_price)
        layout.addWidget(self.amount_edit)

        self.toggle_inputs()
        self.radio_button.toggled.connect(self.toggle_inputs)
        layout.addWidget(self.radio_button)

        self.card_number_edit.setValidator(QRegExpValidator(QRegExp("\d{0,16}")))
        self.card_code_edit.setValidator(QIntValidator())
        self.expire_month_edit.setValidator(QIntValidator())
        self.expire_year_edit.setValidator(QIntValidator())
        self.amount_edit.setValidator(QIntValidator())

        self.card_number_edit.setMaxLength(16)
        self.card_code_edit.setMaxLength(3)
        self.expire_month_edit.setMaxLength(2)
        self.expire_year_edit.setMaxLength(4)

        self.add_button = QPushButton("Сохранить изменения")
        layout.addWidget(self.add_button)
        self.add_button.setFixedHeight(40)
        self.add_button.clicked.connect(self.confirmEditing)

        self.setLayout(layout)

    def toggle_inputs(self):
        is_enabled = not self.radio_button.isChecked()
        self.card_number_edit.setEnabled(is_enabled)
        self.card_code_edit.setEnabled(is_enabled)
        self.expire_month_edit.setEnabled(is_enabled)
        self.expire_year_edit.setEnabled(is_enabled)
    
    def closeEvent(self, event):
        self.AdminMainWindow.enableAdminMainWindow()
        event.accept()

    def confirmEditing(self):
        card_number = self.card_number_edit.text()
        card_code = self.card_code_edit.text()
        end_month = self.expire_month_edit.text()
        end_year = self.expire_year_edit.text()
        total_price = self.amount_edit.text()
        reservation_id = self.reservationId
        payment_id = self.paymentId

        if self.reservationId:
            reservation_id = self.reservationId
        else:
            reservation_id = None

        if not self.radio_button.isChecked() and card_number and card_code and end_month and end_year and total_price:
            if (int(end_month) < 13) and (len(end_year) == 4):
                current_date = datetime.now().date()
                expiry_date = datetime(int(end_year), int(end_month), 1).date()
                if expiry_date > current_date:
                    try:
                        with self.conn as conn:
                            with conn.cursor() as cursor:
                                cursor.execute("SELECT update_payment(%s, %s, %s, %s, %s, %s, %s, %s)", (payment_id, 'Card', str(card_number), str(card_code), str(end_month), str(end_year), None, total_price))
                                conn.commit()
                                self.AdminMainWindow.enableAdminMainWindow()
                                QMessageBox.information(self, 'Успех', 'Изменения сохранены')
                                self.close()
                    except Exception as e:
                        QMessageBox.warning(self, 'Ошибка', f'Ошибка при добавлении платежа')
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Срок действия карты истек')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Дата введена некорректно')
        else:
            if self.radio_button.isChecked() and total_price:
                try:
                    with self.conn as conn:
                        with conn.cursor() as cursor:
                            cursor.execute("SELECT update_payment(%s, %s, %s, %s, %s, %s, %s, %s)", (payment_id, 'Cash', None, None, None, None, None, total_price))
                            conn.commit()
                            self.AdminMainWindow.enableAdminMainWindow()
                            QMessageBox.information(self, 'Успех', 'Изменения сохранены')
                            self.close()
                except Exception as e:
                    QMessageBox.warning(self, 'Ошибка', f'Ошибка при добавлении платежа')

            else:
                QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все поля!')
        
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    add_payment_screen = EditPaymentScreen()
    add_payment_screen.show()
    sys.exit(app.exec_())