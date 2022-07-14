# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""


from netmiko import ConnectHandler
from pprint import pprint
import textfsm
import yaml

def parse_output_to_dict(template, command_output):
    with open(template) as t:
        fsm = textfsm.TextFSM(t)
        result = fsm.ParseTextToDicts(command_output)
    return result

# вызов функции должен выглядеть так
if __name__ == "__main__":
    with open('devices.yaml') as f:
        dev_params = yaml.safe_load(f)[0]
    with ConnectHandler(**dev_params) as ssh:
        ssh.enable()
        output = ssh.send_command("sh ip int br")
    result = parse_output_to_dict("templates/sh_ip_int_br.template", output)
    print(result)
