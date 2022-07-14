import sqlite3
import os

if not os.path.isfile("dhcp_snooping.db"):
    print("Создаю базу данных...")
    with open("dhcp_snooping_schema.sql") as f:
        schema = f.read()
    connection = sqlite3.connect('dhcp_snooping.db')
    cursor = connection.cursor()
    cursor.executescript(schema)
else:
    print("База данных существует")




