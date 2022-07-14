
import yaml
import sqlite3
import re
import glob
import os
from datetime import datetime, timedelta

def parser_dhcp_snoop(output_file_name):
    hostname = os.path.basename(output_file_name).split("_")[0]
    regex = re.compile(r"(?P<mac>\S+)\s+(?P<ip>\S+)\s+\d+\s+\S+\s+(?P<vlan>\d+)\s+(?P<intf>\S+)")
    with open (output_file_name) as f:
        output_data = f.read()
    out_list = [out_match.groups() + (hostname, ) for out_match in regex.finditer(output_data)]
    return out_list


def insert_data(db_name, query, data_list):
    con = sqlite3.connect(db_name)
    for row in data_list:
        try:
            with con:
                con.execute(query, row)
        except sqlite3.IntegrityError as e:
            print(f"При добавлении данных:{row} Возникла ошибка:{e}")
    con.close()


def insert_to_switches_table(db_name, sw_data_file):
    query_sw = "INSERT into switches values (?, ?)"
    if not os.path.isfile(db_name):
        print("База данных не существует. Перед добавлением данных, ее надо создать")
        return
    else:
        with open(sw_data_file) as f:
            data = yaml.safe_load(f)
        sw_list = [(key, value) for key, value in data["switches"].items()]
        print("Добавляю данные в таблицу switches...")
        insert_data(db_name, query_sw, sw_list)


def insert_to_dhcp_table(db_name, dhcp_snoop_files):
    remove_old_records(db_name)
    query_dhcp = "INSERT OR REPLACE INTO dhcp values (?, ?, ?, ?, ?, ?, datetime('now'))"
    reset_active_flag(db_name)
    if not os.path.isfile(db_name):
        print("База данных не существует. Перед добавлением данных, ее надо создать")
        return
    else:
        print("Добавляю данные в таблицу dhcp...")
        for file in dhcp_snoop_files:
            dhcp_list = parser_dhcp_snoop(file)
            updated_list = [row + (1, ) for row in dhcp_list]
            insert_data(db_name, query_dhcp, updated_list)

def remove_old_records(db_name):
    con = sqlite3.connect(db_name)
    now = datetime.today().replace(microsecond=0)
    week_ago = str(now - timedelta(days=7))
    query = "delete from dhcp where last_active < ?"
    con.execute(query, (week_ago,))
    con.commit()
    con.close()

def reset_active_flag(db_name):
    query_active_to_zero = "UPDATE dhcp set active = 0 WHERE active = 1"
    con = sqlite3.connect(db_name)
    with con:
        con.execute(query_active_to_zero)
    con.close()

if __name__ == "__main__":
    dhcp_snoop_files = glob.glob("sw*.txt")
    new_dhcp_snoop_files = glob.glob("new_data/sw*.txt")
    insert_to_switches_table("dhcp_snooping.db", "switches.yml")
    insert_to_dhcp_table("dhcp_snooping.db", dhcp_snoop_files)
    insert_to_dhcp_table("dhcp_snooping.db", new_dhcp_snoop_files)
