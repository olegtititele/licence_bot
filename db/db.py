from operator import truediv
import psycopg2

class DB():

    def __init__(self):
        self.connection = psycopg2.connect(host='localhost', user='postgres', password='admin1305', database='LicenceBot')

    def create_users_table(self):
        cursor = self.connection.cursor()
        # with self.connection.cursor() as cursor:
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (user_id VARCHAR(255))''')
        self.connection.commit()

    def add_user(self, chat_id):
        sql = "INSERT INTO users (user_id) VALUES (%s)"
        val = chat_id,
        cursor = self.connection.cursor()
        cursor.execute(sql, val)
        self.connection.commit()

    def check_user(self, chat_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = '%s'", (chat_id, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return True

    def get_users_len(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        length = len(cursor.fetchall())
        return length
    
    def get_all_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id FROM users")
        data = cursor.fetchall()
        return data