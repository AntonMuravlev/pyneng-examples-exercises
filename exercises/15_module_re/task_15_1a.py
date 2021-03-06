# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""

import re


def get_ip_from_cfg(file_name):
    regex = re.compile(
    r"interface (?P<int_name>\S+)\n"
    r"( .*\n)*"
    r" ip address (?P<ip>([\d.])+) (?P<mask>([\d.])+)",
    )
    out_dict = {}
    with open(file_name) as f:
        content = f.read()
        for m in regex.finditer(content):
            out_dict[m.group("int_name")] = (m.group("ip", "mask"))
    return out_dict


if __name__ == "__main__":
    print(get_ip_from_cfg("config_r1.txt"))

    
