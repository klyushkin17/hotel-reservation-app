import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from AddClientScreen import AddClientScreen
from EditClientScreen import EditClientScreen
from AddRoomScreen import AddRooomScreen
from EditRoomScreen import EditRoomScreen
from AddReservationScreen import AddReservationScreen

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
        refresh_client_table_btn = QPushButton()
        refresh_client_table_btn.setIcon(QIcon('resourses/refresh_icon.png'))
        add_client_btn.setFixedHeight(40)
        edit_client_btn.setFixedHeight(40)
        delete_client_btn.setFixedHeight(40)
        refresh_client_table_btn.setFixedHeight(40)
        button_layout.addWidget(add_client_btn)
        button_layout.addWidget(edit_client_btn)
        button_layout.addWidget(delete_client_btn)
        button_layout.addWidget(refresh_client_table_btn)

        tab1_layout.addLayout(button_layout)
        tab1.setLayout(tab1_layout)
        tab_widget.addTab(tab1, "Клиенты")

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
        refresh_room_table_btn = QPushButton()
        refresh_room_table_btn.setIcon(QIcon('resourses/refresh_icon.png'))
        add_room_btn.setFixedHeight(40)
        edit_room_btn.setFixedHeight(40)
        delete_room_btn.setFixedHeight(40)
        refresh_room_table_btn.setFixedHeight(40)
        button_layout_1.addWidget(add_room_btn)
        button_layout_1.addWidget(edit_room_btn)
        button_layout_1.addWidget(delete_room_btn)
        button_layout_1.addWidget(refresh_room_table_btn)

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
        refresh_reservation_table_btn = QPushButton()
        refresh_reservation_table_btn.setIcon(QIcon('resourses/refresh_icon.png'))
        add_reservation_btn.setFixedHeight(40)
        edit_reservation_btn.setFixedHeight(40)
        delete_reservation_btn.setFixedHeight(40)
        refresh_reservation_table_btn.setFixedHeight(40)
        button_layout_2.addWidget(add_reservation_btn)
        button_layout_2.addWidget(edit_reservation_btn)
        button_layout_2.addWidget(delete_reservation_btn)
        button_layout_2.addWidget(refresh_reservation_table_btn)


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
        refresh_payment_table_btn = QPushButton()
        refresh_payment_table_btn.setIcon(QIcon('resourses/refresh_icon.png'))
        add_payment_btn.setFixedHeight(40)
        edit_payment_btn.setFixedHeight(40)
        delete_payment_btn.setFixedHeight(40)
        refresh_payment_table_btn.setFixedHeight(40)
        button_layout_3.addWidget(add_payment_btn)
        button_layout_3.addWidget(edit_payment_btn)
        button_layout_3.addWidget(delete_payment_btn)
        button_layout_3.addWidget(refresh_payment_table_btn)

        tab4_layout.addLayout(button_layout_3)
        tab4.setLayout(tab4_layout)
        tab_widget.addTab(tab4, "Оплата")

        self.setCentralWidget(tab_widget)

        add_client_btn.clicked.connect(lambda: self.add_row(self.client_table))
        edit_client_btn.clicked.connect(lambda: self.edit_row(self.client_table))
        delete_client_btn.clicked.connect(lambda: self.delete_row(self.client_table))

        add_room_btn.clicked.connect(lambda: self.add_row(self.room_table))
        edit_room_btn.clicked.connect(lambda: self.edit_row(self.room_table))
        delete_room_btn.clicked.connect(lambda: self.delete_row(self.room_table))

        add_reservation_btn.clicked.connect(lambda: self.add_row(self.reservation_table))
        edit_reservation_btn.clicked.connect(lambda: self.edit_row(self.reservation_table))
        delete_reservation_btn.clicked.connect(lambda: self.delete_row(self.reservation_table))

        add_payment_btn.clicked.connect(lambda: self.add_row(self.payment_table))
        edit_payment_btn.clicked.connect(lambda: self.edit_row(self.payment_table))
        delete_payment_btn.clicked.connect(lambda: self.delete_row(self.payment_table))

        refresh_client_table_btn.clicked.connect(self.refresh_tables)
        refresh_room_table_btn.clicked.connect(self.refresh_tables)
        refresh_reservation_table_btn.clicked.connect(self.refresh_tables)
        refresh_payment_table_btn.clicked.connect(self.refresh_tables)

        self.display_data(self.client_table, "SELECT * FROM client ORDER BY clientid")
        self.display_data(self.room_table, "SELECT * FROM room ORDER BY roomid")
        self.display_data(self.reservation_table, "SELECT * FROM get_reservation_details()")
        self.display_data(self.payment_table, "SELECT * FROM payment ORDER BY paymentid")
    

    def refresh_tables(self):
        self.display_data(self.client_table, "SELECT * FROM client ORDER BY clientid")
        self.display_data(self.room_table, "SELECT * FROM room ORDER BY roomid")
        self.display_data(self.reservation_table, "SELECT * FROM get_reservation_details()")
        self.display_data(self.payment_table, "SELECT * FROM payment ORDER BY paymentid")

    def disableAdminMainWindow(self):
        self.setDisabled(True)

    def enableAdminMainWindow(self):
        self.setEnabled(True)

    def add_row(self, table_widget):
        if (table_widget == self.client_table):
            self.add_client_screen = AddClientScreen(self.conn, self)
            self.add_client_screen.show()
            self.setDisabled(True)
        elif (table_widget == self.room_table):
            self.add_room_screen = AddRooomScreen(self.conn, self)
            self.add_room_screen.show()
            self.setDisabled(True)
        elif (table_widget == self.reservation_table):
            self.add_reservation_screen = AddReservationScreen(self.conn, self)
            self.add_reservation_screen.show()
            self.setDisabled(True)
     
    def edit_row(self, table_widget):
        if (table_widget == self.client_table):
            selected_row = table_widget.currentRow()
            if selected_row != -1: 
                client_id = table_widget.item(selected_row, 0).text()
                client_surname = table_widget.item(selected_row, 1).text()
                client_name = table_widget.item(selected_row, 2).text()
                client_phonenumber = table_widget.item(selected_row, 3).text()
                client_email = table_widget.item(selected_row, 4).text()

                self.edit_client_screen = EditClientScreen(self.conn, client_id, client_name, client_surname, client_phonenumber, client_email, self)
                self.edit_client_screen.show()
                self.setDisabled(True)

        elif (table_widget == self.room_table):
            selected_row = table_widget.currentRow()
            if selected_row != -1: 
                room_id = table_widget.item(selected_row, 0).text()
                room = table_widget.item(selected_row, 1).text()
                capacity = table_widget.item(selected_row, 2).text()
                payment = table_widget.item(selected_row, 3).text()

                self.edit_room_screen = EditRoomScreen(self.conn, room_id, room, capacity, payment, self)
                self.edit_room_screen.show()
                self.setDisabled(True)
        
    def delete_row(self, table_widget):
        if (table_widget == self.client_table):
            selected_row = table_widget.currentRow()
            if selected_row != -1:
                client_id = table_widget.item(selected_row, 0).text()
                try:
                    with self.conn as conn:
                        with conn.cursor() as cursor:
                            cursor.execute("SELECT delete_client(%s)", (client_id))
                            conn.commit()
                            QMessageBox.information(self, 'Успех', f'Клиент удален!')
                except Exception as e:
                    QMessageBox.warning(self, 'Ошибка', f'Не удалось удалить клиента: ')
                self.refresh_tables() 
        elif (table_widget == self.room_table):
            selected_row = table_widget.currentRow()
            if selected_row != -1:
                room_id = table_widget.item(selected_row, 0).text()
                try:
                    with self.conn as conn:
                        with conn.cursor() as cursor:
                            cursor.execute("SELECT delete_room(%s)", (room_id))
                            conn.commit()
                            QMessageBox.information(self, 'Успех', f'Номер удален!')
                except Exception as e:
                    QMessageBox.warning(self, 'Ошибка', f'Не удалось удалить номер: ')
                self.refresh_tables() 

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