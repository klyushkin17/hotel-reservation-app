from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QLabel, QMainWindow, QTableWidgetItem, QTableWidget, QHBoxLayout, QDateEdit, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QFont
from ConnectionManager import ConnectionManager
from PaymentWindow import PaymentWindow

class UserMainWindow(QWidget):
    def __init__(self, conn, clientId):
    
        super().__init__()
        self.conn = conn
        
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

        self.search_button.clicked.connect(self.onSearchBottonClicked)
        self.reserve_button.clicked.connect(self.onReserveButtonClicked)

    def onReserveButtonClicked(self):
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            return

        room_id = self.table_widget.item(selected_row, 0).text()
        room = self.table_widget.item(selected_row, 1).text()
        capacity = self.table_widget.item(selected_row, 2).text()
        price = self.table_widget.item(selected_row, 3).text()

        checkin_date = self.checkin_date.date()
        checkout_date = self.checkout_date.date()

        self.payment_window = PaymentWindow(room_id, room, capacity, price, checkin_date, checkout_date, self.conn)
            

    def onSearchBottonClicked(self):
        checkin_date = self.checkin_date.date().toString("yyyy-MM-dd")
        checkout_date = self.checkout_date.date().toString("yyyy-MM-dd")
        
        with self.conn as conn:
            with conn.cursor() as cursor:
                sql_query = f"""
                SELECT roomid, room, capacity, price
                FROM room
                WHERE roomid NOT IN (
                    SELECT roomid
                    FROM reservation
                    WHERE ('{checkout_date}' <= departure AND '{checkout_date}' >= checkindate) OR ('{checkin_date}' <= departure AND '{checkin_date}' >= checkindate)
                );
                """
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                
                self.table_widget.setRowCount(len(rows))
                self.table_widget.setColumnCount(len(rows[0]))

                column_labels = ['Номер комнаты', 'Вместимость', 'Цена']  
                self.table_widget.setHorizontalHeaderLabels(column_labels)
                
                for i, row in enumerate(rows):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        item.setFont(QFont("Arial", 10)) 
                        self.table_widget.setItem(i, j, item)
                        
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = UserMainWindow(conn=None, IS_ADMIN=False)
    window.show()
    sys.exit(app.exec_())