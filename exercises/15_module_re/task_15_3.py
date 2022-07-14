# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""

import re


def convert_ios_nat_to_asa(in_file, out_file):
    regex = re.compile(
        r"ip nat inside source static tcp (?P<host>[\d.]+) (?P<port_1>\d+) \S+ \S+ (?P<port_2>\d+)\n"
    )
    with open(in_file) as f:
        in_file_content = f.read()
    with open(out_file, "w") as out:
        for m in regex.finditer(in_file_content):
            out.write(
                f"""
object network LOCAL_{m.group("host")}
 host {m.group("host")}
 nat (inside,outside) static interface service tcp {m.group("port_1")} {m.group("port_2")}"""
            )


if __name__ == "__main__":
    convert_ios_nat_to_asa("cisco_nat_config.txt", "asa_config.txt")
