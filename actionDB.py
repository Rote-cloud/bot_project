import psycopg2

from setting import PASSWORD

class ActionRepository:
    def __init__(self):
        self.conn = psycopg2.connect(dbname='postgres', user='postgres', password=PASSWORD, host='127.0.0.1')
        self.cursor = self.conn.cursor()

    def add(self, name, url):
        request = "insert into weather (username, url) values (%s, %s)"
        self.cursor.execute(request, (name, url))
        self.conn.commit()

    def value_output(self, name):
        request = "select * from weather where username = %s"
        self.cursor.execute(request, (name,))
        value = self.cursor.fetchall()

        return value

    def closeDB(self):
        self.cursor.close()
        self.conn.close()