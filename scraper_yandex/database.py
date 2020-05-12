import re

import mysql.connector
from idna import unicode


class Database:
    def myresult(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="images"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT ie_name FROM table_name")
        myresult = mycursor.fetchall()

        for x in myresult:
            for y in x:
                print(y)
        print(len(myresult))

        return myresult

#  Пример подключения в другом классе или файле
# class Start(Database):
#     mass = Database()
#     mass.myresult()
