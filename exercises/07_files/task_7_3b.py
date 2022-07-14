# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

file_name = "CAM_table.txt"

output_template = "{:<10}{:<20}{}"

mac_string = []
with open(file_name, "r") as input_file:
    for line in input_file:
        if line.find("DYNAMIC") != -1:
            mac_string.append(line.split())

vlan_number = input("Enter vlan number: ")

for string in mac_string:
    if vlan_number == string[0]:
        print(output_template.format(string[0], string[1], string[3]))
