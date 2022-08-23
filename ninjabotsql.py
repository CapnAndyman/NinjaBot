import sqlite3
from sqlcipher3 import dbapi2 as sqlitecipher
from sqlite3 import Error


class Ninjabotsql:

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def sql_select(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("pragma key='#Rt-HPvbqa.S2z^A'")
        cur.execute(sqlquery, sqlvalues)

        rows = cur.fetchall()

        return rows

    def sql_kanjiselect(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.connji.cursor()
        cur.execute(sqlquery, sqlvalues)

        rows = cur.fetchall()

        return rows

    def sql_kanaselect(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.conna.cursor()
        cur.execute(sqlquery, sqlvalues)

        rows = cur.fetchall()

        return rows

    def sql_ganaselect(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.gonna.cursor()
        cur.execute(sqlquery, sqlvalues)

        rows = cur.fetchall()

        return rows

    def sql_aslselect(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.connasl.cursor()
        cur.execute(sqlquery, sqlvalues)

        rows = cur.fetchall()

        return rows

    def sql_triviaselect(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.conntrivia.cursor()
        cur.execute(sqlquery, sqlvalues)

        rows = cur.fetchall()

        return rows

    def sql_japaneseselect(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.connjapanese.cursor()
        cur.execute(sqlquery, sqlvalues)

        rows = cur.fetchall()

        return rows

    def sql_frenchselect(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.connfrench.cursor()
        cur.execute(sqlquery, sqlvalues)

        rows = cur.fetchall()

        return rows

    def sql_dictionaryselect(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.conndictionary.cursor()
        cur.execute(sqlquery, sqlvalues)

        rows = cur.fetchall()

        return rows

    def sql_riddleselect(self, sqlquery):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.connriddle.cursor()
        cur.execute(sqlquery)

        rows = cur.fetchall()

        return rows

    def sql_ffselect(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.connff.cursor()
        cur.execute(sqlquery, sqlvalues)

        rows = cur.fetchall()

        return rows

    def sql_ffinsert(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.connff.cursor()
        cur.execute(sqlquery, sqlvalues)
        self.connff.commit()

        return cur.lastrowid

    def sql_novalues(self, sqlquery):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("pragma key='#Rt-HPvbqa.S2z^A'")
        cur.execute(sqlquery)

        rows = cur.fetchall()

        return rows

    def sql_insert(self, sqlquery, sqlvalues):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("pragma key='#Rt-HPvbqa.S2z^A'")
        cur.execute(sqlquery, sqlvalues)
        self.conn.commit()

        return cur.lastrowid


    def __init__(self):

        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        try:
            self.conn = sqlitecipher.connect("data/pythonsqlite.db")
        except Error as e:
            print(e)

        self.connji = None
        try:
            self.connji = sqlite3.connect("data/kanji.db")
        except Error as e:
            print(e)        

        self.conna = None
        try:
            self.conna = sqlite3.connect("data/kana.db")
        except Error as e:
            print(e)     

        self.gonna = None
        try:
            self.gonna = sqlite3.connect("data/gana.db")
        except Error as e:
            print(e)   

        self.conntrivia = None
        try:
            self.conntrivia = sqlite3.connect("data/trivia.db")
        except Error as e:
            print(e)   

        self.connjapanese = None
        try:
            self.connjapanese = sqlite3.connect("data/nihongo.db")
        except Error as e:
            print(e)   

        self.connasl = None
        try:
            self.connasl = sqlite3.connect("data/asl.db")
        except Error as e:
            print(e)

        self.connfrench = None
        try:
            self.connfrench = sqlite3.connect("data/french.db")
        except Error as e:
            print(e)

        self.conndictionary = None
        try:
            self.conndictionary = sqlite3.connect("data/dictionary.db")
        except Error as e:
            print(e)

        self.connriddle = None
        try:
            self.connriddle = sqlite3.connect("data/riddles.db")
        except Error as e:
            print(e)

        self.connff = None
        try:
            self.connff = sqlite3.connect("data/ff.db")
        except Error as e:
            print(e)