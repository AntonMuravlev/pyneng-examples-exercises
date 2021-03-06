# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
import yaml
import re
from pprint import pprint
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
from task_20_5 import create_vpn_config

def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        output = ssh.send_command(command)
    return output

def send_config_commands(device, commands):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        output = ssh.send_config_set(commands)
    return output

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    config1, config2 = create_vpn_config(src_template, dst_template, vpn_data_dict)

    #collect tunnel int
    out1 = send_show_command(src_device_params, "show ip int br")
    out2 = send_show_command(dst_device_params, "show ip int br")

    #parse output
    regex = re.compile(r"Tunnel(\d+)")
    tun_numbers1 = []
    tun_numbers2 = []
    if "Tunnel" in out1:
        tun_numbers1 = [tun_num.group(1) for tun_num in regex.finditer(out1)]
    if "Tunnel" in out2:
        tun_numbers2 = [tun_num.group(1) for tun_num in regex.finditer(out2)]
    all_tun_numbers = list(map(int, set(tun_numbers1 + tun_numbers2)))

    #calculate tunnel id
    if not all_tun_numbers:
        vpn_data_dict['tun_num'] = 0
    elif len(all_tun_numbers) == max(all_tun_numbers):
        vpn_data_dict['tun_num'] = max(all_tun_numbers) + 1
    else:
        for i in range(1, max(all_tun_numbers)):
            if i not in all_tun_numbers:
                vpn_data_dict['tun_num'] = i
                break
    #prepare config
    config1, config2 = create_vpn_config(src_template, dst_template, vpn_data_dict)
    config1 = config1.split("\n")
    config2 = config2.split("\n")
    #send config
    out1 = send_config_commands(src_device_params, config1)
    out2 = send_config_commands(dst_device_params, config2)
    return out1, out2


if __name__ == "__main__":
    data = {
        "tun_num": None,
        "wan_ip_1": "192.168.100.1",
        "wan_ip_2": "192.168.100.2",
        "tun_ip_1": "10.0.1.1 255.255.255.252",
        "tun_ip_2": "10.0.1.2 255.255.255.252",
    }

    src_template = "templates/gre_ipsec_vpn_1.txt"
    dst_template = "templates/gre_ipsec_vpn_2.txt"

    with open("devices.yaml") as f:
        dev_data = yaml.safe_load(f)

    src_device_params = dev_data[0]
    dst_device_params = dev_data[1]

    print(configure_vpn(src_device_params, dst_device_params, src_template,
        dst_template, data))
