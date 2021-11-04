import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
#import mysql.connector as mc
#import pymysql
import psycopg2

#when error, just change the "password" into the password of your own postgresql account


#function that lets you create table into your postgres database in your pc
def create_table():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="5432", host="localhost", port="5432")
    cur = conn.cursor()

    try:
        query = """CREATE TABLE IF NOT EXISTS logs(id varchar not null, name varchar not null, commission real, orderform bool, password varchar);"""
        cur.execute(query)
        conn.commit()
        print("Table created")
    except:
        print("Already Exists")

create_table()

#Load UI
class AddWin(QWidget):
    def __init__(self):
        super(AddWin, self).__init__()
        uic.loadUi("add.ui", self)

        self.addbtn.clicked.connect(self.addData)
        self.cancelbtn.clicked.connect(self.close)

    def addData(self):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="5432", host="localhost", port="5432")
        cur = conn.cursor()
        try:
            cur.execute('''INSERT INTO logs(id, name, commission)
                                      VALUES (%s, %s, %s)''',
                        (self.idtxt.text(),
                         self.nametxt.text(),
                         self.comitxt.text())
                        )
            conn.commit()
            cur.close()
            QMessageBox.information(self, "Congratulations", "Data Inserted Successfully")
            #print("Added Values")
        except Exception as e:
            print("Exception: ", e)

class SalespersonWin(QWidget):
    def __init__(self):
        super(SalespersonWin, self).__init__()
        uic.loadUi("view.ui", self)
        self.loadData()
        self.addbtn.clicked.connect(self.window2)
        self.refreshbtn.clicked.connect(self.loadData)

    def window2(self):
        self.addWin = AddWin()
        self.addWin.show()

    def loadData(self):
        try:
            conn = psycopg2.connect(dbname="postgres", user="postgres", password="5432", host="localhost", port="5432")
            cur = conn.cursor()
            cur.execute("SELECT * FROM logs")
            result = cur.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                print(row_number)
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    # print(column_number)
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print("Error")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main.ui", self)
        self.show()
        self.actionSalesperson.triggered.connect(self.saleWindow)

    def saleWindow(self):
        self.salespersonWindow = SalespersonWin()
        self.salespersonWindow.show()



app = QApplication(sys.argv)
design = MainWindow()

app.exec_()
