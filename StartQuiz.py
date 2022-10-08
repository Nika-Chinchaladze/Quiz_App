from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QComboBox
from PyQt5 import uic
from GameQuiz import IronMan
from data import question_data


class SpiderMan(QMainWindow):
    def __init__(self):
        super(SpiderMan, self).__init__()
        uic.loadUi("register.ui", self)

        # define content:
        self.head_label = self.findChild(QLabel, "head_label")
        self.name_line = self.findChild(QLineEdit, "name_line")
        self.sur_line = self.findChild(QLineEdit, "sur_line")
        self.box = self.findChild(QComboBox, "box")
        self.start_button = self.findChild(QPushButton, "start_button")
        self.name_line.setPlaceholderText("Name")
        self.sur_line.setPlaceholderText("Surname")

        # call defined methods:
        self.start_button.clicked.connect(self.begin_quiz)


        self.show()

# ----------------------------- logic ------------------------------- #
    def begin_quiz(self):
        self.window_iron = QMainWindow()
        self.iron = IronMan()
        self.write_first()
        self.remember()
        self.close()
    
    def write_first(self):
        self.iron.ask_label.setText(f" Q.1  {question_data[0]['text']}")
        self.iron.next_button.setEnabled(False)
        self.iron.next_button.setStyleSheet("background-color: rgb(189, 189, 189)")
        self.iron.check_button.setStyleSheet("background-color: rgb(255, 255, 255)")
    
    def remember(self):
        First_name = self.name_line.text()
        Last_name = self.sur_line.text()
        Category = self.box.currentText()
        self.iron.section_label.setText(f"{Category}'s Section")
        self.iron.information = [First_name, Last_name, Category]
        

# ------------------------------ end -------------------------------- #

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    spider = SpiderMan()
    sys.exit(app.exec_())
