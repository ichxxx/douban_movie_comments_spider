import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('create table comments_data (id int, comment text, rating int)')
cursor.close()
conn.commit()
conn.close()