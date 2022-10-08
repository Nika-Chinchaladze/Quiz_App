import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QFrame, QRadioButton
from PyQt5 import uic
from Visualize import BatMan
from data import question_data


class IronMan(QMainWindow):
    def __init__(self):
        super(IronMan, self).__init__()
        uic.loadUi("play.ui", self)
        # extra variables:
        self.score = 0
        self.ask_index = 0
        self.question_bank = question_data
        self.information = []

        # define content:
        self.section_label = self.findChild(QLabel, "section_label")
        self.ask_label = self.findChild(QLabel, "ask_label")
        self.answer_label = self.findChild(QLabel, "answer_label")
        self.see_label = self.findChild(QLabel, "see_label")
        self.next_button = self.findChild(QPushButton, "next_button")
        self.stac_button = self.findChild(QPushButton, "stac_button")
        self.check_button = self.findChild(QPushButton, "check_button")
        self.frame_1 = self.findChild(QFrame, "frame_1")
        self.frame_2 = self.findChild(QFrame, "frame_2")
        self.t_button = self.findChild(QRadioButton, "t_button")
        self.f_button = self.findChild(QRadioButton, "f_button")
        self.stac_button.setEnabled(False)


        # call defined methods:
        self.next_button.clicked.connect(self.next_try)
        self.check_button.clicked.connect(self.check_answer)
        self.stac_button.clicked.connect(self.check_statistics)

        self.show()

# ----------------------------- logic ------------------------------- #
    def next_try(self):
        try:
            self.ask_label.setText(f" Q.{self.ask_index+1}  {self.question_bank[self.ask_index]['text']}")
            self.answer_label.setText("")
            self.t_button.setChecked(False)
            self.f_button.setChecked(False)
            self.check_button.setEnabled(True)
            self.check_button.setStyleSheet("background-color: rgb(255, 255, 255)")
        except IndexError:
            self.next_button.setEnabled(False)
            self.stac_button.setEnabled(True)
            if self.score <= 4:
                self.answer_label.setText(f"You have Bad results, Try Again!")
            elif self.score >= 5 and self.score <= 8:
                self.answer_label.setText(f"Good Job, You have Good results!")
            else:
                self.answer_label.setText(f"Congratulations, You have Excellent results!")
        # actions:
        self.next_button.setEnabled(False)
        self.next_button.setStyleSheet("background-color: rgb(189, 189, 189)")
        self.answer_label.setStyleSheet("background-color: rgb(85, 0, 255);")
    
    def check_answer(self):
        correct_answer = self.question_bank[self.ask_index]['answer']
        try:
            # first conditional:
            if self.t_button.isChecked():
                guess = "True"
            elif self.f_button.isChecked():
                guess = "False"
            # second conditional:
            if guess == correct_answer:
                self.score += 1
                self.answer_label.setText("Good Job, Your answer is Correct!")
                self.answer_label.setStyleSheet("background-color: rgb(51, 153, 75);")
            else:
                self.answer_label.setText("Unfortunately, Your answer is Wrong!")
                self.answer_label.setStyleSheet("background-color: rgb(85, 0, 255);")
            # actions:
            self.check_button.setEnabled(False)
            self.check_button.setStyleSheet("background-color: rgb(254, 254, 254)")
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet("background-color: rgb(244, 127, 50)")
            self.see_label.setText(f"{self.score} / {self.ask_index + 1}")
            self.ask_index += 1
        except UnboundLocalError:
            pass
    
    def check_statistics(self):
        Name = self.information[0]
        Surname = self.information[1]
        Category = self.information[2]
        conn = sqlite3.connect("results.db")
        curr = conn.cursor()
        curr.execute(f'''INSERT INTO students(first_name, last_name, score, category) VALUES('{Name}', '{Surname}', {self.score}, '{Category}');''')
        conn.commit()
        conn.close()
        self.go_next_page()
    
    def go_next_page(self):
        self.window_show = QMainWindow()
        self.bat = BatMan()
        self.close()

# ------------------------------ end -------------------------------- #

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    iron = IronMan()
    sys.exit(app.exec_())
