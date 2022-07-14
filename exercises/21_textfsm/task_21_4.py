# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
from textfsm import clitable
from netmiko import ConnectHandler
from task_21_3 import parse_command_dynamic
import yaml

def send_and_parse_show_command(device_dict, command, templates_path,
        index='index'):
    #prepare attributes_dict
    attributes_dict = {"Command": command, "Vendor": device_dict["device_type"]}
    #collect output
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        command_output = ssh.send_command(command)
    #parse output
    return parse_command_dynamic(command_output, attributes_dict,
            index_file="index", templ_path=templates_path)

if __name__ == "__main__":
    with open('devices.yaml') as f:
        dev_params = yaml.safe_load(f)[0]
    command = "sh ip int br"
    templates_path = "templates"
    result = send_and_parse_show_command(dev_params, command, templates_path)
    print(result)
