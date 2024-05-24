import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QLabel, QMainWindow

from ConnectionManager import ConnectionManager
from UserMainWindow import UserMainWindow
from RegistrationWindow import RegistrationWindow


class ChooseRoleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().__init__()
        self.setWindowTitle('Выбор роли')
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Выберите роль:', self).setFixedWidth(200)  
    

        self.user_radio = QRadioButton('Пользователь', self)
        self.admin_radio = QRadioButton('Администратор', self)

        self.select_button = QPushButton('Выбрать', self)
        self.select_button.clicked.connect(self.onSelectUserButtonClicked)

        layout.addWidget(self.user_radio) 
        layout.addWidget(self.admin_radio)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

    def onSelectUserButtonClicked(self):
        global IS_ADMIN
        if self.user_radio.isChecked():
            connection = ConnectionManager("hoteldatabaseuser")     
            IS_ADMIN = True
            self.form1 = RegistrationWindow(connection, IS_ADMIN)
            self.form1.show()
            self.close()

        elif self.admin_radio.isChecked():
            connection = ConnectionManager("hoteldatabaseadmin")
            IS_ADMIN = False
            #self.form1 = MainWindow(connection, IS_ADMIN)
            self.form1.show()
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ChooseRoleWindow()
    form.show()
    sys.exit(app.exec_())