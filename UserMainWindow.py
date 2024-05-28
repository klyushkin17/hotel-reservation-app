from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QLabel, QMainWindow, QTableWidgetItem, QTableWidget, QHBoxLayout, QDateEdit, QAbstractItemView, QHeaderView, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
from ConnectionManager import ConnectionManager
from PaymentWindow import PaymentWindow
from datetime import datetime

class UserMainWindow(QWidget):
    def __init__(self, conn, clientId):
        super().__init__()
        self.conn = conn
        self.clientId = clientId
        self.ultimateCheckinDate = ''
        self.ultimateCheckoutDate = ''
        
        layout = QVBoxLayout()
        self.setWindowTitle("Бронирование номеров")
        self.setFixedSize(900, 600)
        self.setLayout(layout)
        
        date_layout = QHBoxLayout()
        
        checkin_label = QLabel("Дата въезда:")
        self.checkin_date = QDateEdit()
        date_layout.addWidget(checkin_label)
        date_layout.addWidget(self.checkin_date)
        
        checkout_label = QLabel("Дата выезда:")
        self.checkout_date = QDateEdit()
        date_layout.addWidget(checkout_label)
        date_layout.addWidget(self.checkout_date)

        self.search_button = QPushButton('Найти', self)
        date_layout.addWidget(self.search_button)
           
        layout.addLayout(date_layout)
        
        self.table_widget = QTableWidget()
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)  
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
    
        layout.addWidget(self.table_widget)

        self.reserve_button = QPushButton('Забронировать', self)
        self.reserve_button.setFixedHeight(50)
        layout.addWidget(self.reserve_button)

        self.search_button.clicked.connect(self.onSearchButtonClicked)
        self.reserve_button.clicked.connect(self.onReserveButtonClicked)

    def onReserveButtonClicked(self):
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            return

        room_id = self.table_widget.item(selected_row, 0).text()
        room = self.table_widget.item(selected_row, 1).text()
        capacity = self.table_widget.item(selected_row, 2).text()
        price = self.table_widget.item(selected_row, 3).text()

        checkin_date = QDate.fromString(self.ultimateCheckinDate, "yyyy-MM-dd")
        checkout_date = QDate.fromString(self.ultimateCheckoutDate, "yyyy-MM-dd")

        self.payment_window = PaymentWindow(room_id, room, capacity, price, checkin_date, checkout_date, self.conn, self.clientId, self)
        self.setDisabled(True)
        self.payment_window.show()
    
    def unlockUserMainWindow(self):
        self.setEnabled(True)
            

    def onSearchButtonClicked(self):
        checkin_date = self.checkin_date.date().toString("yyyy-MM-dd")
        checkout_date = self.checkout_date.date().toString("yyyy-MM-dd")
        current_date = datetime.now().strftime("%Y-%m-%d")

        print(type(checkin_date))

        if (checkin_date >= checkout_date) or (checkin_date < current_date):  
            QMessageBox.warning(self, "Ошибка", "Некорректно выбраны даты")
        else:
            self.ultimateCheckinDate = checkin_date
            self.ultimateCheckoutDate = checkout_date
            with self.conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                    SELECT * FROM get_available_rooms_query(%s, %s);
                    """, (checkin_date, checkout_date))
                    rows = cursor.fetchall()
                    
                    self.table_widget.setRowCount(len(rows))
                    self.table_widget.setColumnCount(len(rows[0]))

                    column_labels = ['ID комнаты','Комната', 'Вместимость', 'Цена']  
                    self.table_widget.setHorizontalHeaderLabels(column_labels)
                    
                    for i, row in enumerate(rows):
                        for j, value in enumerate(row):
                            item = QTableWidgetItem(str(value))
                            item.setFont(QFont("Arial", 10)) 
                            self.table_widget.setItem(i, j, item)
                    self.table_widget.setColumnHidden(0, True)        
                        
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = UserMainWindow(conn=None, IS_ADMIN=False)
    window.show()
    sys.exit(app.exec_())