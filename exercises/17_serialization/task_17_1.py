# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод
команды show dhcp snooping binding из разных файлов и записывает обработанные
данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла,
остальные - из содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.

"""

import re
import csv

def write_dhcp_snooping_to_csv(filenames, output):
    regex = re.compile(r"(?P<mac>\S+) +(?P<ip>[\d.]+).*?(?P<vlan>\d+) +(?P<int_name>\S+)\n")
    out_list = [["switch", "mac", "ip", "vlan", "interface"]]
    for name in filenames:
        with open(name) as f:
            switch_name = name.split("_")[0]
            content = f.read()
            [out_list.append([switch_name] + (list(m.groups()))) for m in regex.finditer(content)]
#    print(out_list)

    with open(output, 'w') as f:
        writer = csv.writer(f)
        for row in out_list:
            writer.writerow(row)

if __name__ == "__main__":
    filenames = ["sw1_dhcp_snooping.txt", "sw2_dhcp_snooping.txt",
    "sw3_dhcp_snooping.txt"]
    write_dhcp_snooping_to_csv(filenames, "output.csv")

