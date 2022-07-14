# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

from sys import argv

file_name = argv[1]

counter = 0

with open(file_name, "r") as f:
    for line in f:
        if line.startswith("!") == False:
            for bad_command in ignore:
                if line.find(bad_command) != -1:
                    break
                elif ignore[-1] == bad_command:
                    print(line.rstrip())
