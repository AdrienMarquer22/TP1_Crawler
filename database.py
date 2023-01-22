import sqlite3
import csv
import requests


class Database():
    def __init__(self,name) -> None:
        conn = sqlite3.connect(name + '.db')
        self.cursor = conn.cursor()

    def init_base(self):
        self.cursor.execute('''CREATE TABLE links (
            link text,
            last_modified text,
            html text
        )''')

    def get_cursor(self):
        return self.cursor