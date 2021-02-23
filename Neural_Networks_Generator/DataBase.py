# (c) Kosolapov Denis 2021
# License GPLv2
import mysql.connector

class MySQL:
    def __init__(self, host, user, passwd):
        try:
            self.MYSQL = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd
            )
        except mysql.connector.Error:
            print('failed to connect to MySQL, check the entered parameters')

    def showDatabases(self):
        my_cursor = self.MYSQL.cursor()
        my_cursor.execute('SHOW DATABASES')
        mass = []
        for x in my_cursor:
            for y in x:
                mass.append(y)
        mass.sort()
        return mass


    def userDatabases(self):
        all_bases_list = self.showDatabases()
        system_bases_list = ['information_schema', 'mysql', 'performance_schema', 'sys']
        user_bases = list(set(all_bases_list) - set(system_bases_list))
        user_bases.sort()
        return user_bases

    @staticmethod
    def systemDatabases():
        system_bases_list = ['information_schema', 'mysql', 'performance_schema', 'sys']
        return system_bases_list


class DataBase:
    # create a database and connect to it
    def __init__(self, host, user, passwd, database):
        try:
            self.base = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
            )
            my_cursor = self.base.cursor()
            my_cursor.execute('CREATE DATABASE ' + database)
        except mysql.connector.Error:
            # print('database ' + database + ' exist')
            pass
        self.connectDataBase(host, user, passwd, database)

    # connect to database
    def connectDataBase(self, host, user, passwd, database):
        try:
            self.base = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
            )
        except mysql.connector.Error:
            print('database ' + database + ' not found')

    def dropDatabase(self, database_list):
        for i in database_list:
            try:
                my_cursor = self.base.cursor()
                my_cursor.execute('DROP DATABASE ' + i)
            except mysql.connector.Error:
                print('the database does not exist')

    def dropTable(self, drop_list):
        for i in drop_list:
            try:
                my_cursor = self.base.cursor()
                my_cursor.execute('DROP TABLE ' + i)
            except mysql.connector.Error:
                print('table unavailable')

    def dropColumn(self, table_name, column_list):
        for i in column_list:
            try:
                my_cursor = self.base.cursor()
                my_cursor.execute('ALTER TABLE ' + table_name + ' DROP COLUMN ' + i)
            except mysql.connector.Error:
                print('cannot delete column')

    def dropRow(self, table_name, column_name, what_to_delete):
        my_cursor = self.base.cursor()
        sql = "DELETE FROM " + table_name + " WHERE " + column_name + " =" + "\'" + what_to_delete + "\'"
        my_cursor.execute(sql)
        self.base.commit()

    def createTable(self, list_tables_create):
        for i in list_tables_create:
            try:
                my_cursor = self.base.cursor()
                my_cursor.execute('CREATE TABLE ' + i + '(id INT AUTO_INCREMENT PRIMARY KEY)')
            except mysql.connector.Error:
                print('unable to create table')

    # for save the neural network weights
    def createTable_weights(self, table_name, columns):
        my_cursor = self.base.cursor()
        my_cursor.execute("CREATE TABLE " + table_name + '(' + columns + ')')


    def addColumn(self, table_name, columns):
        try:
            for column_name, data_type in columns.items():
                my_cursor = self.base.cursor()
                my_cursor.execute('ALTER TABLE ' + table_name + ' ADD COLUMN ' + column_name + ' ' + data_type)
        except mysql.connector.Error:
            print('cannot add column')

    def select_column(self, table_name, column_name):
        try:
            mass = []
            my_cursor = self.base.cursor()
            my_cursor.execute('SELECT ' + column_name + ' FROM ' + table_name)
            my_result = my_cursor.fetchall()
            for x in my_result:
                for y in x:
                    mass.append(y)
            return mass
        except mysql.connector.Error:
            print('cannot select data')

    def select_row(self, table_name):
        try:
            my_cursor = self.base.cursor()
            my_cursor.execute('SELECT *' + ' FROM ' + table_name)
            my_result = my_cursor.fetchall()
            val = []
            for i in my_result:
                i = list(i)
                val.append(i)
            return val
        except mysql.connector.Error:
            print('cannot select data')

    def insertInto(self, table_name, lists_values_in_list, list_column_info):
        values_tuples = []
        for i in lists_values_in_list:
            i = tuple(i)
            values_tuples.append(i)
        if 'id' in list_column_info:
            list_column_info.remove('id')
        mass = []
        for i in range(len(list_column_info)):
            mass.append('%s')
        mass = self.listToString(mass)
        line = mass.split()
        values = ', '.join(line)
        string_columns = self.getStringForRequest(list_column_info)
        my_cursor = self.base.cursor()
        for i in values_tuples:
            sql = "INSERT INTO " + table_name + " (" + string_columns + ") VALUES (" + values + ")"
            my_cursor.execute(sql, i)
            self.base.commit()

    def search(self, table_name, column_name, text_search):
        my_cursor = self.base.cursor()
        sql = "SELECT * FROM " + table_name + " WHERE " + column_name + " =" + "\'" + text_search + "\'"
        my_cursor.execute(sql)
        result = my_cursor.fetchall()
        return result

    def searchLike(self, table_name, column_name, expression_for_search):
        my_cursor = self.base.cursor()
        sql = "SELECT * FROM " + table_name + " WHERE " + column_name + " LIKE " + "\'" + expression_for_search + "\'"
        my_cursor.execute(sql)
        result = my_cursor.fetchall()
        return result

    def update(self, table_name, column_name, old_data, new_data):
        my_cursor = self.base.cursor()
        sql = ("UPDATE " + table_name + " SET " + column_name + " =" + "\'" + new_data + "\'" + " WHERE " +
               column_name + " =" + "\'" + old_data + "\'")
        my_cursor.execute(sql)
        self.base.commit()

    def showDataTable(self, table_name):
        my_cursor = self.base.cursor()
        my_cursor.execute("SELECT * FROM " + table_name)
        result = my_cursor.fetchall()
        return result

    def showTablesList(self):
        tables = []
        my_cursor = self.base.cursor()
        my_cursor.execute("SHOW TABLES")
        for x in my_cursor:
            for y in x:
                tables.append(y)
        return tables

    def showColumnInfo(self, database, table_name):
        my_cursor = self.base.cursor()
        my_cursor.execute('SHOW COLUMNS FROM ' + table_name + ' IN ' + database)
        mass = []
        for x in my_cursor:
            mass.append(x)
        return mass

    def getColumnList(self, database, table_name):
        column_info = self.showColumnInfo(database, table_name)
        column_list = self.getColumnInfo(column_info, 0)
        return column_list

    @staticmethod
    def getColumnInfo(list_column_info, num):
        mass = []
        if type(num) == int:
            for x in list_column_info:
                mass.append(x[num])
        return mass

    @staticmethod
    def listToString(list_to_string):
        string = ' '
        return string.join(list_to_string)

    def getStringForRequest(self, list_for_string):
        s = self.listToString(list_for_string)
        line = s.split()
        string = ', '.join(line)
        return string

    @staticmethod
    def console(result):
        for x in result:
            for j in x:
                print(j)

    @staticmethod
    def count(result):
        count = len(result)
        return count
