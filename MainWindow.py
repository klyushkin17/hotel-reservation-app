from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QLabel, QMainWindow, QTableWidgetItem, QTableWidget
from ConnectionManager import ConnectionManager

class MainWindow(QWidget):
    def __init__(self, conn: ConnectionManager, IS_ADMIN):
        super().__init__()
        self.conn : ConnectionManager = conn
        self.showMaximized()
        layout = QVBoxLayout()
        self.setWindowTitle("Разряды")
        self.setGeometry(100, 100, 600, 400)
        self.setLayout(layout)
        self.table_widget = QTableWidget()
        self.table_widget.setGeometry(50, 50, 500, 300)

        self.show_data_button = QPushButton("Показать данные")
        self.show_data_button.clicked.connect(self.load_data_from_db)
        layout.addWidget(self.show_data_button)
        layout.addWidget(self.table_widget)

    def load_data_from_db(self):
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM room")  # Убедитесь, что имя таблицы верно
                rows = cursor.fetchall()
                self.table_widget.setRowCount(len(rows))
                self.table_widget.setColumnCount(len(rows[0]))
                for i, row in enumerate(rows):
                    for j, value in enumerate(row):
                        self.table_widget.setItem(i, j, QTableWidgetItem(str(value)))