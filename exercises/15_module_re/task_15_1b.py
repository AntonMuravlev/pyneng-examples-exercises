# -*- coding: utf-8 -*-
"""
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a
на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них.

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким
образом, чтобы в значении словаря она возвращала список кортежей
для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет
несколько кортежей. Ключом остается имя интерфейса.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность
IP-адреса, диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""

import re


def get_ip_from_cfg(file_name):
    regex = re.compile(
    r"interface (?P<int_name>\S+)\n"
    r"( .*\n)*"
    r" ip address (?P<ip>([\d.])+) (?P<mask>([\d.])+)\n"
    r"( ip address (?P<sec_ip>([\d.])+) (?P<sec_mask>([\d.])+) secondary)*"
    )
    out_dict = {}
    with open(file_name) as f:
        content = f.read()
        for m in regex.finditer(content):
            if m.group("sec_ip"):
                out_dict[m.group("int_name")] = [m.group("ip", "mask"),
            m.group("sec_ip", "sec_mask")]
            else:
                out_dict[m.group("int_name")] = [(m.group("ip", "mask"))]
    return out_dict


if __name__ == "__main__":
    print(get_ip_from_cfg("config_r2.txt"))
