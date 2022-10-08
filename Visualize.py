from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QComboBox, QFrame, QHBoxLayout
from PyQt5.QtWidgets import QTextEdit, QTableWidget, QTableWidgetItem
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np
import sqlite3


class BatMan(QMainWindow):
    def __init__(self):
        super(BatMan, self).__init__()
        uic.loadUi("show.ui", self)

        # define content:
        self.outcome_label = self.findChild(QLabel, "outcome_label")
        self.x_line = self.findChild(QLineEdit, "x_line")
        self.y_line = self.findChild(QLineEdit, "y_line")
        self.chart_box = self.findChild(QComboBox, "chart_box")
        self.color_box = self.findChild(QComboBox, "color_box")
        self.exec_button = self.findChild(QPushButton, "exec_button")
        self.show_button = self.findChild(QPushButton, "show_button")
        self.close_button = self.findChild(QPushButton, "close_button")
        self.command_frame = self.findChild(QFrame, "command_frame")
        self.down_frame = self.findChild(QFrame, "down_frame")
        self.over_frame = self.findChild(QFrame, "over_frame")
        self.table_widget = self.findChild(QTableWidget, "table_widget")
        self.text_edit = self.findChild(QTextEdit, "text_edit")
        self.x_line.setPlaceholderText("X Label")
        self.y_line.setPlaceholderText("Y Label")

        # chart:
        self.First_layout = QHBoxLayout(self.over_frame)
        self.First_layout.setObjectName("First_layout")
        self.figure = plt.figure()
        self.diagramm = FigureCanvas(self.figure)
        self.First_layout.addWidget(self.diagramm)

        # call defined methods:
        self.close_button.clicked.connect(lambda: self.close())
        self.exec_button.clicked.connect(self.execute_script)
        self.show_button.clicked.connect(self.show_charts)


        self.show()

# ----------------------------- logic ------------------------------- #
    def execute_script(self):
        # execute query:
        sql_script = self.text_edit.toPlainText()
        conn = sqlite3.connect("results.db")
        curr = conn.cursor()
        result_list = []
        try:
            for item in curr.execute(f'''{sql_script}'''):
                result_list.append(list(item))
        except sqlite3.OperationalError:
            pass
        conn.commit()
        conn.close()
        # store output into dataframe:
        result_frame = pd.DataFrame(result_list, columns=["First_Name", "Last_Name", "Score", "Category"])
        RowNumber = len(result_frame.index)
        ColumnNumber = len(result_frame.columns)

        self.table_widget.setColumnCount(ColumnNumber)
        self.table_widget.setRowCount(RowNumber)
        self.table_widget.setHorizontalHeaderLabels(result_frame.columns)

        for rows in range(RowNumber):
            for columns in range(ColumnNumber):
                self.table_widget.setItem(rows, columns, QTableWidgetItem(str(result_frame.iat[rows, columns])))
        
        result_frame.to_csv("answer.csv", index=False)
        self.table_widget.setStyleSheet("background-color: rgb(249, 249, 187);")
    
    def show_charts(self):
        chart_type = self.chart_box.currentText()
        color_type = self.color_box.currentText()
        x_column = self.x_line.text()
        y_column = self.y_line.text()
        self.figure.clear()
        df = pd.read_csv("answer.csv")
        if chart_type == "Bar":
            if (x_column in df.columns) and (y_column in df.columns):
                plt.bar(df[f"{x_column}"], df[f"{y_column}"], color = f"{color_type}")
                plt.grid()
                self.figure.autofmt_xdate()
                self.diagramm.draw()
            else:
                pass
        elif chart_type == "Barh":
            if (x_column in df.columns) and (y_column in df.columns):
                plt.barh(df[f"{x_column}"], df[f"{y_column}"], color = f"{color_type}")
                plt.grid()
                self.figure.autofmt_xdate()
                self.diagramm.draw()
            else:
                pass
        else:
            if (x_column in df.columns) and (y_column in df.columns):
                # define labels:
                my_labels = pd.Series(df[f"{x_column}"]).to_numpy()
                my_labels = np.unique(my_labels)
                # define values:
                amount = df.groupby(df[f"{x_column}"]).sum()
                answer = pd.Series(amount[f"{y_column}"]).to_numpy()
                # visualize:
                plt.pie(answer, labels=my_labels, shadow=True)
                self.diagramm.draw()
            else:
                pass

# ------------------------------ end -------------------------------- #

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    bat = BatMan()
    sys.exit(app.exec_())