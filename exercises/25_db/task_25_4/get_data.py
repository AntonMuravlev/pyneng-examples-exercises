import sqlite3
from sys import argv
from pprint import pprint
from tabulate import tabulate


def read_data(db_name, query):
    con = sqlite3.connect(db_name)
    result = [row for row in con.execute(query)]
    con.close()
    return result


def print_all_data(db_name):
    get_all_data_active = "SELECT * from dhcp WHERE active = 1"
    get_all_data_passive = "SELECT * from dhcp WHERE active = 0"
    print("Active")
    print(tabulate(read_data(db_name, get_all_data_active)))
    if read_data("dhcp_snooping.db", get_all_data_passive):
        print("Passive")
        print(tabulate(read_data("dhcp_snooping.db", get_all_data_passive)))


def print_data_by_params(db_name, column, value):
        query_template = 'SELECT * from dhcp WHERE {}="{}" AND active = {}'
        params_list = ["mac", "ip", "vlan", "interface", "switch"]
        if column not in params_list:
            print('''
Данный параметр не поддерживается.
Допустимые значения параметров: mac, ip, vlan, interface, switch'''
                )
        else:
            query = query_template.format(column, value, 1)
            print("Информация об устройствах с такими параметрами: {} {}".format(column, value))
            print("Active")
            print(tabulate(read_data("dhcp_snooping.db", query)))
            if read_data("dhcp_snooping.db", query_template.format(column, value, 0)):
                print("Passive")
                print(tabulate(read_data("dhcp_snooping.db", query_template.format(column, value, 0))))


if __name__ == "__main__":

    db_name = "dhcp_snooping.db"

    if len(argv)<2:
        print_all_data(db_name)
    elif len(argv) == 3:
        column = argv[1]
        value = argv[2]
        print_data_by_params(db_name, column, value)
    else:
        print("Пожалуйста, введите два или ноль аргументов")

