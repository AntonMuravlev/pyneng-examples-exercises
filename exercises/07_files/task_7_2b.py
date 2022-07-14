# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

from sys import argv

file_source = argv[1]
file_dest = argv[2]

counter = 0

with open(file_source, "r") as f, open(file_dest, 'w') as dest:
    for line in f:
        if line.startswith("!") == False:
            for bad_command in ignore:
                if line.find(bad_command) != -1:
                    break
                elif ignore[-1] == bad_command:
                    dest.write(line)
