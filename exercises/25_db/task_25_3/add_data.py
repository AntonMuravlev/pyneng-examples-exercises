
import yaml
import sqlite3
import re
import glob
import os

def parser_dhcp_snoop(output_file_name):
    hostname = os.path.basename(output_file_name).split("_")[0]
    regex = re.compile(r"(?P<mac>\S+)\s+(?P<ip>\S+)\s+\d+\s+\S+\s+(?P<vlan>\d+)\s+(?P<intf>\S+)")
    with open (output_file_name) as f:
        output_data = f.read()
    out_list = [out_match.groups() + (hostname, ) + (1, ) for out_match in regex.finditer(output_data)]
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
    query_dhcp = "INSERT OR REPLACE INTO dhcp values (?, ?, ?, ?, ?, ?)"
    reset_active_flag(db_name)
    if not os.path.isfile(db_name):
        print("База данных не существует. Перед добавлением данных, ее надо создать")
        return
    else:
        print("Добавляю данные в таблицу dhcp...")
        for file in dhcp_snoop_files:
            dhcp_list = parser_dhcp_snoop(file)
            insert_data(db_name, query_dhcp, dhcp_list)

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
