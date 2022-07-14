# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

out_template = """
Prefix                {:<25}
AD/Metric             {:<25}
Next-Hop              {:<25}
Last update           {:<25}
Outbound Interface    {:<25}
"""

with open("ospf.txt", "r") as f:
    for line in f:
        line_list = line.split()
        print(
            out_template.format(
                line_list[1],
                line_list[2].strip("[]"),
                line_list[4].strip(","),
                line_list[5].strip(","),
                line_list[6],
            )
        )
