# -*- coding: utf-8 -*-
"""
Задание 21.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды sh ip int br с оборудования
и шаблоне templates/sh_ip_int_br.template.

"""
from netmiko import ConnectHandler
from pprint import pprint
import textfsm
import yaml

def parse_command_output(template, command_output):
    with open(template) as t:
        fsm = textfsm.TextFSM(t)
        result = fsm.ParseText(command_output)
    return [fsm.header] + result

# вызов функции должен выглядеть так
if __name__ == "__main__":
#    with open('devices.yaml') as f:
#        dev_params = yaml.safe_load(f)[0]
#    with ConnectHandler(**dev_params) as ssh:
#        ssh.enable()
#        output = ssh.send_command("sh ip int br")
    with open("output/sh_ip_dhcp_snooping.txt") as f:
        output = f.read()
    template = "templates/sh_ip_dhcp_snooping.template"
    result = parse_command_output(template, output)
    print(result)
