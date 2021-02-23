# (c) Kosolapov Denis 2018
# License GPLv2
from DataBase import DataBase
from DataBase import MySQL
import numpy


class Search:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        mysql = MySQL(host, user, password)
        self.database = mysql.userDatabases()

    def searchAllDatabases(self, search_text):
        for i in range(len(self.database)):
            base = DataBase(self.host, self.user, self.password, self.database[i])
            table_list = base.showTablesList()
            for table in table_list:
                column_info = base.showColumnInfo(self.database[i], table)
                column_list = base.getColumnInfo(column_info, 0)
                for column in column_list:
                    result = base.searchLike(table, column, search_text)
                    if len(result) > 0:
                        return result, [self.database[i], table, column]

    def searchInDatabase(self, database, search_text):
        if database in self.database:
            base = DataBase(self.host, self.user, self.password, database)
            table_list = base.showTablesList()
            for table in table_list:
                column_info = base.showColumnInfo(database, table)
                column_list = base.getColumnInfo(column_info, 0)
                for column in column_list:
                    result = base.searchLike(table, column, search_text)
                    if len(result) > 0:
                        return result, [database, table, column]
        else:
            print('no such databases')

    def searchInTable(self, table_name, search_text):
        for i in range(len(self.database)):
            base = DataBase(self.host, self.user, self.password, self.database[i])
            table_list = base.showTablesList()
            for table in table_list:
                if table_name == table:
                    column_info = base.showColumnInfo(self.database[i], table_name)
                    column_list = base.getColumnInfo(column_info, 0)
                    for column in column_list:
                        result = base.searchLike(table_name, column, search_text)
                        if len(result) > 0:
                            return result, [self.database[i], table_name, column]


    def searchInColumn(self,table_name, column_name, search_text):
        for i in range(len(self.database)):
            base = DataBase(self.host, self.user, self.password, self.database[i])
            table_list = base.showTablesList()
            for table in table_list:
                if table_name == table:
                    column_info = base.showColumnInfo(self.database[i], table_name)
                    column_list = base.getColumnInfo(column_info, 0)
                    if column_name in column_list:
                        result = base.searchLike(table_name, column_name, search_text)
                        if len(result) > 0:
                            return result, [self.database[i], table, column_name]

    # def searchInColumn(self, column_name, search_text):
    #     for i in range(len(self.database)):
    #         base = DataBase(self.host, self.user, self.password, self.database[i])
    #         table_list = base.showTablesList()
    #         for table in table_list:
    #             column_info = base.showColumnInfo(self.database[i], table)
    #             column_list = base.getColumnInfo(column_info, 0)
    #             if column_name in column_list:
    #                 result = base.searchLike(table, column_name, search_text)
    #                 if len(result) > 0:
    #                     return result, [self.database[i], table, column_name]



class Result_Search():
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        mysql = MySQL(host, user, password)
        self.database = mysql.userDatabases()

    def unique_table_rows(self,table,  text):
        base = DataBase(self.host, self.user, self.password, self.database)
        search = '%' + text + '%'
        function = Search(self.host, self.user, self.password)
        columns = base.showColumnInfo(self.database, table)
        column_list = base.getColumnInfo(columns, 0)
        search_column_list = [column_list[1], column_list[2], column_list[3]]
        search_result = []

        for column in search_column_list:
            result = function.searchInColumn(table, column, search)
            if result is not None:
                for res in result:
                    search_result.append(list(res))

        temp_equals = []
        for i in range(len(search_result)):
            temp_equals.append(search_result[i][1])

        list_of_links_without_repeats = list(set(temp_equals))

        unique_table_rows = []
        for i in range(len(search_result)):
            if search_result[i][1] in list_of_links_without_repeats and search_result[i] not in unique_table_rows:
                unique_table_rows.append(search_result[i])

        return unique_table_rows


# this is a test version of class !
# this version need to the remodel !

class DataValidation:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.base = DataBase(self.host, self.user, self.password, self.database)

    def getArrayTable(self, table_name):
        column_list = self.base.getColumnList(self.database, table_name)
        table_data = []
        for i in range(len(column_list)):
            column = self.base.select(table_name, column_list[i])
            table_data.append(column)
        table_data = numpy.array(table_data).T
        return table_data

    def validationInsertData(self, table_name, new_data):
        column_list = self.base.getColumnList(self.database, table_name)
        table_data = self.getArrayTable(table_name)
        add_list = []
        for row in new_data:
            for table_cell in row:
                if table_cell not in table_data:
                    add_list.append(row)
        self.base.insertInto(table_name, add_list, column_list)
