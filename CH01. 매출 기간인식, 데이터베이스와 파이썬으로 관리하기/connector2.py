# connector2.py
import mysql.connector

class Connector:
    def __enter__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            port="3306",
            password="fastcampus1!",
            database="daily_sales"
        )
        self.cursor = self.connection.cursor(dictionary=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()

    def insert_data(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()
