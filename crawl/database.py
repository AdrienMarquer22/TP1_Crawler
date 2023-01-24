import sqlite3



class Database():
    def __init__(self,name) -> None:
        self.conn = sqlite3.connect(name + '.db')
        self.cursor = self.conn.cursor()

    def init_tabe(self,name):
        self.name_tabel=name
        self.cursor.execute("DROP TABLE IF EXISTS "+ name +";")
        self.cursor.execute('CREATE TABLE '+ name +' (link text,last_modified text,html text)')
        self.commit()

    def insert(self,name_table,elem:list):
        self.cursor.execute("INSERT INTO "+name_table +" VALUES (?,?,?)", elem)

    def create_html_from_link(self,link_page,name_table,name_html_page):
        self.cursor.execute("Select html from "+ name_table +" where link like " +link_page)
        html_content = self.cursor.fetchone()[0]
        with open(name_html_page +'.html', 'w') as f:
            f.write(html_content)

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()