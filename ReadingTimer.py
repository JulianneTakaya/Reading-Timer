# Imports
from PyQt6.QtCore import QDate, Qt, QTimer, QTime
from PyQt6.QtWidgets import QApplication, QCheckBox, QDateEdit, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QWidget
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
#
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
#
import numpy as np
from sys import exit

# main class
class ReadingTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.button_click()
        
    # settings
    def settings(self):
        self.setWindowTitle("ReadingTimer")
        self.resize(800,600)

    # init UI
    def initUI(self):

        # date read
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())

        # book title
        self.bookName_box = QLineEdit()
        self.bookName_box.setPlaceholderText("Enter the book title")

        # author name
        self.bookAuthor_box = QLineEdit()
        self.bookAuthor_box.setPlaceholderText("Enter the book author")

        # pages read
        self.pagesRead_box = QLineEdit()
        self.pagesRead_box.setPlaceholderText("Enter the number of pages read")

        # time spent reading
        self.timeSpent_box = QLineEdit()
        self.timeSpent_box.setPlaceholderText("Enter the time spent reading")

        # Timer
        self.time = QTime(0, 0, 0)
        self.time_label = QLabel("00:00:00", self)
        self.timer=QTimer(self)

        #buttons
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")
        self.submit_button = QPushButton("Submit")
        self.clear_button = QPushButton("Clear")
        self.startTimer_button = QPushButton("Start Timer")
        self.stopTimer_button = QPushButton("Stop Timer")
        self.resetTimer_button = QPushButton("Reset Timer")
        self.dark_mode = QCheckBox("Dark Mode")

        #tables
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Title","Author", "Pages", "Time"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Design layout
        # column 1
        self.master_layout = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

        self.sub_row1 = QHBoxLayout()
        self.sub_row2 = QHBoxLayout()
        self.sub_row3 = QHBoxLayout()
        self.sub_row4 = QHBoxLayout()
        self.sub_row5 = QHBoxLayout()
        self.sub_row6 = QHBoxLayout()
        self.sub_row7 = QHBoxLayout()

        self.sub_row1.addWidget(QLabel("Date:"))
        self.sub_row1.addWidget(self.date_box)

        self.sub_row2.addWidget(QLabel("Title:"))
        self.sub_row2.addWidget(self.bookName_box)

        self.sub_row3.addWidget(QLabel("Author:"))
        self.sub_row3.addWidget(self.bookAuthor_box)

        self.sub_row4.addWidget(QLabel("Pages Read:"))
        self.sub_row4.addWidget(self.pagesRead_box)

        self.sub_row5.addWidget(QLabel("Reading Time:"))
        self.sub_row5.addWidget(self.timeSpent_box)

        self.sub_row6.addWidget(self.time_label)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.sub_row7.addWidget(self.startTimer_button)
        self.sub_row7.addWidget(self.stopTimer_button)
        self.sub_row7.addWidget(self.resetTimer_button)

        self.col1.addLayout(self.sub_row1)
        self.col1.addLayout(self.sub_row2)
        self.col1.addLayout(self.sub_row3)
        self.col1.addLayout(self.sub_row4)
        self.col1.addLayout(self.sub_row5)
        self.col1.addLayout(self.sub_row6)
        self.col1.addLayout(self.sub_row7)

        self.col1.addWidget(self.dark_mode)

        btn_row1 = QHBoxLayout()
        btn_row2 = QHBoxLayout()

        btn_row1.addWidget(self.add_button)
        btn_row1.addWidget(self.delete_button)
        btn_row2.addWidget(self.submit_button)
        btn_row2.addWidget(self.clear_button)

        self.col1.addLayout(btn_row1)
        self.col1.addLayout(btn_row2)

        # column 2
        self.col2.addWidget(self.canvas)
        self.col2.addWidget(self.table)

        self.master_layout.addLayout(self.col1, 3)
        self.master_layout.addLayout(self.col2, 7)
        self.setLayout(self.master_layout)

        self.apply_styles()
        self.load_table()

    # Events
    def startTimer(self):
        # update timer every second
        self.timer.start(1000)

    def stopTimer(self):
        self.timer.stop()

    def resetTimer(self):
        self.timer.stop()
        self.time = QTime(0, 0, 0)
        self.time_label.setText(self.formatTime(self.time))

    def updateTimer(self):
        self.time = self.time.addSecs(1)
        self.time_label.setText(self.formatTime(self.time))
        
    def formatTime(self, time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        return f"{hours:02}:{minutes:02}:{seconds:02}"


    def button_click(self):
        self.add_button.clicked.connect(self.add_book)
        self.delete_button.clicked.connect(self.delete_book)
        self.submit_button.clicked.connect(self.calculate_statistics)
        self.dark_mode.stateChanged.connect(self.toggle_dark_mode)
        self.startTimer_button.clicked.connect(self.startTimer)
        self.stopTimer_button.clicked.connect(self.stopTimer)
        self.resetTimer_button.clicked.connect(self.resetTimer)
        self.timer.timeout.connect(self.updateTimer)
        
        self.clear_button.clicked.connect(self.clear)
    
    # load tables
    def load_table(self):
        self.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM reading_log ORDER BY date DESC")
        row = 0
        while query.next():
            id = query.value(0)
            date = query.value(1)
            title = query.value(2)
            author = query.value(3)
            pages = query.value(4)
            time = query.value(5)

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(title))
            self.table.setItem(row, 3, QTableWidgetItem(author))
            self.table.setItem(row, 4, QTableWidgetItem(str(pages)))
            self.table.setItem(row, 5, QTableWidgetItem(str(time)))
            row += 1
            self.table.hideColumn(0)

    #add tables
    def add_book(self):
        date = self.date_box.date().toString("MM-dd-yyyy")
        title = self.bookName_box.text()
        author = self.bookAuthor_box.text()
        pages = self.pagesRead_box.text()
        time = self.timeSpent_box.text()

        query = QSqlQuery(
            """
            INSERT INTO reading_log (date, title, author, pages, time)
            VALUES (?, ?, ?, ?, ?)
            """
            )
        query.addBindValue(date)
        query.addBindValue(title)
        query.addBindValue(author)
        query.addBindValue(pages)
        query.addBindValue(time)
        query.exec()

        self.date_box.setDate(QDate.currentDate())
        self.bookName_box.clear()
        self.bookAuthor_box.clear()
        self.pagesRead_box.clear()
        self.timeSpent_box.clear()
        self.load_table()

    # delete 
    def delete_book(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self,"Please choose a row to delete")
        id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Delete Log", "Are you sure you want to delete this log?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.No:
            return
        query = QSqlQuery()
        query.prepare("DELETE FROM reading_log WHERE id = ?")
        query.addBindValue(id)
        query.exec()

        self.load_table()

    # calculate reading statistics
    def calculate_statistics(self):
        pages = []
        times = []

        query = QSqlQuery("SELECT pages, time FROM reading_log ORDER BY time ASC")
        while query.next():
            page = query.value(0)
            time = query.value(1)
            pages.append(page)
            times.append(time)

        try:
            #avg_page = [(sum(pages) / len(pages)) for page in pages]
            #avg_time = [(sum(times) / len(times)) for time in times]
            #avg_speed = [(sum(pages) / sum(times))]
            min_page = min(pages)
            max_page = max(pages)
            normalized_pages = [(page - min_page) / (max_page - min_page) for page in pages]

            plt.style.use("Solarize_Light2")
            ax = self.figure.subplots()
            ax.scatter(times, pages, c=normalized_pages, cmap='rainbow', label='Pages Read')
            #ax.scatter(avg_time, avg_page, c='red', label='Average Speed', marker='x')
            ax.set_title("Reading Speed", color="#fff")
            ax.set_xlabel("Time Spent Reading (minutes)", color="#fff")
            ax.set_ylabel("Pages Read", color="#fff")
            cbar = ax.figure.colorbar(ax.collections[0], label = 'Average Pages Read')
            cbar.ax.yaxis.label.set_color("#fff")
            cbar.ax.tick_params(colors="#fff")
            ax.tick_params(colors="#fff")
            
            ax.legend()
            self.canvas.draw()
        except Exception as e:
            QMessageBox.warning(self, "Error", "Please enter some data to calculate statistics.")
    
    # css styling
    def apply_styles(self):
        #light mode
        self.setStyleSheet("""
            QWidget{
                background-color: #d3d3ff;
            }
            QLabel, QCheckBox{
                color: #333;
                font-size: 14px;
            }
            QLineEdit, QComboBox, QDateEdit{
                background-color: #e1e1ff;
                color: #333;
                border: 1px solid #444;
                padding: 5px;
            }
            QHeaderView::section{
                color: #333;
            }
            QTableWidget{
                background-color: #d3d3ff;
                color: #333;
                border: 1px solid #444;
                selection-background-color: #ddd;
            }
            QTableWidget::item:selected{
                background-color: #bc96cd;
            }
            QPushButton{
                background-color: #BC96CD;
                color: #333;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover{
                background-color: #8A6F9B;
            }
            """
        )
        figure_color = "#BC96CD"

        self.figure.patch.set_facecolor(figure_color)
        self.canvas.setStyleSheet(f"background-color:{figure_color}")

        #dark mode
        if self.dark_mode.isChecked():
            self.setStyleSheet("""
                QWidget{
                    background-color: #090933;
                }
                QLabel, QCheckBox{
                    color: #faf9f6;
                    font-size: 14px;
                }
                QLineEdit, QComboBox, QDateEdit{
                    background-color: #575799;
                    color: #faf9f6;
                    border: 1px solid #fff;
                    padding: 5px;
                }
                QHeaderView::section{
                    color: #faf9f6;
                }
                QTableWidget{
                    background-color: #090933;
                    color: #faf9f6;
                    border: 1px solid #fff;
                    selection-background-color: #140152;
                }
                QTableWidget::item:selected{
                    background-color: #4048bf;
                }
                QPushButton{
                    background-color: #5058af;
                    color: #faf9f6;
                    border: none;
                    padding: 8px 16px;
                    font-size: 14px;
                }
                QPushButton:hover{
                    background-color: #4048bf;
                }
                """
            )
            figure_color = "#04052e"
            self.figure.patch.set_facecolor(figure_color)
            self.canvas.setStyleSheet(f"background-color:{figure_color}")

    # dark mode
    def toggle_dark_mode(self):
        self.apply_styles()

    # reset
    def clear(self):
        self.date_box.setDate(QDate.currentDate())
        self.bookName_box.clear()
        self.bookAuthor_box.clear()
        self.pagesRead_box.clear()
        self.timeSpent_box.clear()
        self.resetTimer()
        self.figure.clear()
        self.canvas.draw()

# initilize database
def createDB():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("reading_timer.db")
    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
            "Unable to establish a database connection.\n"
            "This example needs SQLite support. Please read "
            "the Qt SQL driver documentation for information how "
            "to build it.\n\n"
            "Click Cancel to exit.", QMessageBox.StandardButton.Cancel)
        return False
    query = QSqlQuery()
    query.exec(
        """
        CREATE TABLE IF NOT EXISTS reading_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            title TEXT,
            author TEXT,
            pages REAL,
            time REAL
        )
        """
    )
    return True

if __name__ == "__main__":
    app = QApplication([])
    createDB()
    main = ReadingTimer()
    main.show()
    app.exec()
