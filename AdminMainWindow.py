import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
import sqlite3

class AdminMainWindow(QMainWindow):
    def __init__(self, conn, isAdmin):
        super().__init__()
        self.conn = conn
        self.setWindowTitle("Кабинет администратора")
        self.setFixedSize(900, 600)

        tab_widget = QTabWidget()
        
        #Client
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        self.client_table = QTableWidget()
        self.client_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.client_table.setSelectionMode(QAbstractItemView.SingleSelection)  
        self.client_table.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.client_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        tab1_layout.addWidget(self.client_table)

        button_layout = QHBoxLayout()
        add_client_btn = QPushButton("Добавить")
        edit_client_btn = QPushButton("Редактировать")
        delete_client_btn = QPushButton("Удалить")
        add_client_btn.setFixedHeight(40)
        edit_client_btn.setFixedHeight(40)
        delete_client_btn.setFixedHeight(40)
        button_layout.addWidget(add_client_btn)
        button_layout.addWidget(edit_client_btn)
        button_layout.addWidget(delete_client_btn)

        tab1_layout.addLayout(button_layout)
        tab1.setLayout(tab1_layout)
        tab_widget.addTab(tab1, "Клиенты")

        add_client_btn.clicked.connect(self.add_row)

        #Room
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        self.room_table = QTableWidget()
        self.room_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.room_table.setSelectionMode(QAbstractItemView.SingleSelection)  
        self.room_table.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.room_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        tab2_layout.addWidget(self.room_table)

        button_layout_1 = QHBoxLayout()
        add_room_btn = QPushButton("Добавить")
        edit_room_btn = QPushButton("Редактировать")
        delete_room_btn = QPushButton("Удалить")
        add_room_btn.setFixedHeight(40)
        edit_room_btn.setFixedHeight(40)
        delete_room_btn.setFixedHeight(40)
        button_layout_1.addWidget(add_room_btn)
        button_layout_1.addWidget(edit_room_btn)
        button_layout_1.addWidget(delete_room_btn)

        tab2_layout.addLayout(button_layout_1)
        tab2.setLayout(tab2_layout)
        tab_widget.addTab(tab2, "Номера")

        #Reservation
        tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        self.reservation_table = QTableWidget()
        self.reservation_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.reservation_table.setSelectionMode(QAbstractItemView.SingleSelection)  
        self.reservation_table.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.reservation_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        tab3_layout.addWidget(self.reservation_table)

        button_layout_2 = QHBoxLayout()
        add_reservation_btn = QPushButton("Добавить")
        edit_reservation_btn = QPushButton("Редактировать")
        delete_reservation_btn = QPushButton("Удалить")
        add_reservation_btn.setFixedHeight(40)
        edit_reservation_btn.setFixedHeight(40)
        delete_reservation_btn.setFixedHeight(40)
        button_layout_2.addWidget(add_reservation_btn)
        button_layout_2.addWidget(edit_reservation_btn)
        button_layout_2.addWidget(delete_reservation_btn)

        tab3_layout.addLayout(button_layout_2)
        tab3.setLayout(tab3_layout)
        tab_widget.addTab(tab3, "Бронь")

        #Payment
        tab4 = QWidget()
        tab4_layout = QVBoxLayout()
        self.payment_table = QTableWidget()
        self.payment_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.payment_table.setSelectionMode(QAbstractItemView.SingleSelection)  
        self.payment_table.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.payment_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        tab4_layout.addWidget(self.payment_table)

        button_layout_3 = QHBoxLayout()
        add_payment_btn = QPushButton("Добавить")
        edit_payment_btn = QPushButton("Редактировать")
        delete_payment_btn = QPushButton("Удалить")
        add_payment_btn.setFixedHeight(40)
        edit_payment_btn.setFixedHeight(40)
        delete_payment_btn.setFixedHeight(40)
        button_layout_3.addWidget(add_payment_btn)
        button_layout_3.addWidget(edit_payment_btn)
        button_layout_3.addWidget(delete_payment_btn)

        tab4_layout.addLayout(button_layout_3)
        tab4.setLayout(tab4_layout)
        tab_widget.addTab(tab4, "Оплата")

        self.setCentralWidget(tab_widget)

        # Отобразить данные из базы данных в таблицах
        self.display_data(self.client_table, "SELECT * FROM client")
        self.display_data(self.room_table, "SELECT * FROM room")
        self.display_data(self.reservation_table, "SELECT * FROM reservation")
        self.display_data(self.payment_table, "SELECT * FROM payment")

    
    def add_row(self, table_widget):
        pass
        
    def edit_row(self, table_widget):
        pass
        
    def delete_row(self, table_widget):
        pass

    def display_data(self, table_widget, query):
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                
                table_widget.setRowCount(len(rows))
                table_widget.setColumnCount(len(rows[0]))
                
                if (table_widget == self.client_table):
                    column_labels = ['ID клиента','Фамилия', 'Имя', 'Номер телефона', 'Почта']  
                elif (table_widget == self.room_table):
                    column_labels = ['ID комнаты','Комната', 'Вместимость', 'Цена']  
                elif (table_widget == self.reservation_table):
                    column_labels = ['ID брони','Клиент', 'Комната', 'Дата бронированя', 'Дата заселения', 'Дата выселения']  
                else:
                    column_labels = ['ID оплаты','Тип оплаты', 'Номер карты', 'Код карты', 'Месяц конца обс.', 'Год конца обс.', 'Номер брони', 'Сумма']  
                table_widget.setHorizontalHeaderLabels(column_labels)
                
                for i, row in enumerate(rows):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        item.setFont(QFont("Arial", 10)) 
                        table_widget.setItem(i, j, item)
                table_widget.setColumnHidden(0, True)     

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminMainWindow(conn=None, isAdmin=False)
    window.show()
    sys.exit(app.exec_())