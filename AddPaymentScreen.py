import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QLineEdit, QPushButton, QMessageBox, QLabel
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from datetime import datetime

class AddPaymentScreen(QWidget):
    def __init__(self, conn, AdminMainWindow):
        super().__init__()
        self.conn = conn
        self.AdminMainWindow = AdminMainWindow

        self.setWindowTitle("Добавление оплаты")
        self.setFixedSize(400, 350)

        layout = QVBoxLayout()

        self.radio_button = QRadioButton("Оплата наличными")

        self.card_number_label = QLabel("Номер карты:")
        self.card_number_edit = QLineEdit()
        self.card_number_edit.setPlaceholderText("Номер карты")
        layout.addWidget(self.card_number_label)
        layout.addWidget(self.card_number_edit)

        self.card_code_label = QLabel("Код карты:")
        self.card_code_edit = QLineEdit()
        self.card_code_edit.setPlaceholderText("Код карты")
        layout.addWidget(self.card_code_label)
        layout.addWidget(self.card_code_edit)

        self.expire_month_label = QLabel("Месяц конца обслуживания:")
        self.expire_month_edit = QLineEdit()
        self.expire_month_edit.setPlaceholderText("Месяц конца обслуживания")
        layout.addWidget(self.expire_month_label)
        layout.addWidget(self.expire_month_edit)

        self.expire_year_label = QLabel("Год конца обслуживания:")
        self.expire_year_edit = QLineEdit()
        self.expire_year_edit.setPlaceholderText("Год конца обслуживания")
        layout.addWidget(self.expire_year_label)
        layout.addWidget(self.expire_year_edit)

        self.amount_label = QLabel("Сумма:")
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Сумма")
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_edit)

        self.card_number_edit.setValidator(QRegExpValidator(QRegExp("\d{0,16}")))
        self.card_code_edit.setValidator(QIntValidator())
        self.expire_month_edit.setValidator(QIntValidator())
        self.expire_year_edit.setValidator(QIntValidator())
        self.amount_edit.setValidator(QIntValidator())

        self.card_number_edit.setMaxLength(16)
        self.card_code_edit.setMaxLength(3)
        self.expire_month_edit.setMaxLength(2)
        self.expire_year_edit.setMaxLength(4)

        self.radio_button.toggled.connect(self.toggle_inputs)
        layout.addWidget(self.radio_button)

        self.add_button = QPushButton("Добавить")
        layout.addWidget(self.add_button)
        self.add_button.setFixedHeight(40)
        self.add_button.clicked.connect(self.confirmAdding)

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

    def confirmAdding(self):
        card_number = self.card_number_edit.text()
        card_code = self.card_code_edit.text()
        end_month = self.expire_month_edit.text()
        end_year = self.expire_year_edit.text()
        total_price = self.amount_edit.text()

        if not self.radio_button.isChecked() and card_number and card_code and end_month and end_year and total_price:
            if (int(end_month) < 13) and (len(end_year) == 4):
                current_date = datetime.now().date()
                expiry_date = datetime(int(end_year), int(end_month), 1).date()
                if expiry_date > current_date:
                    try:
                        with self.conn as conn:
                            with conn.cursor() as cursor:
                                cursor.execute("SELECT add_payment(%s, %s, %s, %s, %s, %s, %s)", ('Card', str(card_number), str(card_code), str(end_month), str(end_year), None, total_price))
                                conn.commit()
                                self.AdminMainWindow.enableAdminMainWindow()
                                QMessageBox.information(self, 'Успех', 'Оплата добавлена')
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
                            cursor.execute("SELECT add_payment(%s, %s, %s, %s, %s, %s, %s)", ('Cash', None, None, None, None, None, total_price))
                            conn.commit()
                            self.AdminMainWindow.enableAdminMainWindow()
                            QMessageBox.information(self, 'Успех', 'Оплата добавлена')
                            self.close()
                except Exception as e:
                    QMessageBox.warning(self, 'Ошибка', f'Ошибка при добавлении платежа {str(e)}')

            else:
                QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все поля!')
        
        self.close

if __name__ == '__main__':
    app = QApplication(sys.argv)
    add_payment_screen = AddPaymentScreen()
    add_payment_screen.show()
    sys.exit(app.exec_())