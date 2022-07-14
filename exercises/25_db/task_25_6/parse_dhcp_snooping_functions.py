
import yaml
import sqlite3
import re
import glob
import os
from datetime import datetime, timedelta
from tabulate import tabulate

def _insert_data(db_name, query, data_list):
    con = sqlite3.connect(db_name)
    for row in data_list:
        try:
            with con:
                con.execute(query, row)
        except sqlite3.IntegrityError as e:
            print(f"При добавлении данных:{row} Возникла ошибка:{e}")
    con.close()


def _parser_dhcp_snoop(output_file_name):
    hostname = os.path.basename(output_file_name).split("_")[0]
    regex = re.compile(r"(?P<mac>\S+)\s+(?P<ip>\S+)\s+\d+\s+\S+\s+(?P<vlan>\d+)\s+(?P<intf>\S+)")
    with open (output_file_name) as f:
        output_data = f.read()
    out_list = [out_match.groups() + (hostname, ) for out_match in regex.finditer(output_data)]
    return out_list


def _remove_old_records(db_name):
    con = sqlite3.connect(db_name)
    now = datetime.today().replace(microsecond=0)
    week_ago = str(now - timedelta(days=7))
    query = "delete from dhcp where last_active < ?"
    con.execute(query, (week_ago,))
    con.commit()
    con.close()


def _reset_active_flag(db_name):
    query_active_to_zero = "UPDATE dhcp set active = 0 WHERE active = 1"
    con = sqlite3.connect(db_name)
    with con:
        con.execute(query_active_to_zero)
    con.close()


def create_db(db_name, db_schema):
    if not os.path.isfile(db_name):
        print("Создаю базу данных...")
        with open(db_schema) as f:
            schema = f.read()
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.executescript(schema)
    else:
        print("База данных существует")


def add_data_switches(db_name, sw_data_file):
    query_sw = "INSERT into switches values (?, ?)"
    if not os.path.isfile(db_name):
        print("База данных не существует. Перед добавлением данных, ее надо создать")
        return
    else:
        with open(sw_data_file[0]) as f:
            data = yaml.safe_load(f)
        sw_list = [(key, value) for key, value in data["switches"].items()]
        print("Добавляю данные в таблицу switches...")
        _insert_data(db_name, query_sw, sw_list)


def add_data(db_name, dhcp_snoop_files):
    _remove_old_records(db_name)
    query_dhcp = "INSERT OR REPLACE INTO dhcp values (?, ?, ?, ?, ?, ?, datetime('now'))"
    _reset_active_flag(db_name)
    if not os.path.isfile(db_name):
        print("База данных не существует. Перед добавлением данных, ее надо создать")
        return
    else:
        print("Добавляю данные в таблицу dhcp...")
        for file in dhcp_snoop_files:
            dhcp_list = _parser_dhcp_snoop(file)
            updated_list = [row + (1, ) for row in dhcp_list]
            _insert_data(db_name, query_dhcp, updated_list)


def read_data(db_name, query):
    con = sqlite3.connect(db_name)
    result = [row for row in con.execute(query)]
    con.close()
    return result


def get_all_data(db_name):
    get_all_data_active = "SELECT * from dhcp WHERE active = 1"
    get_all_data_passive = "SELECT * from dhcp WHERE active = 0"
    print("Active")
    print(tabulate(read_data(db_name, get_all_data_active)))
    if read_data("dhcp_snooping.db", get_all_data_passive):
        print("Passive")
        print(tabulate(read_data("dhcp_snooping.db", get_all_data_passive)))


def get_data(db_name, column, value):
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

