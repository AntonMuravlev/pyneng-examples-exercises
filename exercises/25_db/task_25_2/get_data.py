import sqlite3
from sys import argv
from pprint import pprint
from tabulate import tabulate


def read_data(db_name, query):
    con = sqlite3.connect(db_name)
    result = [row for row in con.execute(query)]
    con.close()
    return result

if __name__ == "__main__":

    query_template = 'SELECT * from dhcp WHERE {}="{}"'

    if len(argv)<2:
        get_all_data = "SELECT * from dhcp"
        print(tabulate(read_data("dhcp_snooping.db", get_all_data)))
    elif len(argv) == 3:
        column = argv[1]
        value = argv[2]
        params_list = ["mac", "ip", "vlan", "interface", "switch"]
        if column not in params_list:
            print('''
Данный параметр не поддерживается.
Допустимые значения параметров: mac, ip, vlan, interface, switch'''
                )
        else:
            query = query_template.format(column, value)
            print("Информация об устройствах с такими параметрами: {} {}".format(column, value))
            print(tabulate(read_data("dhcp_snooping.db", query)))
    else:
        print("Пожалуйста, введите два или ноль аргументов")

