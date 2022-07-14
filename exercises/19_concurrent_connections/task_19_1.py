# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""

import subprocess
import re
from concurrent.futures import ThreadPoolExecutor

def ping_one_address(ip_add):
    shell_result = str(subprocess.run(f"ping -c 3 -i 0.1 -W 0.5 {ip_add}", shell=True,
        stdout=subprocess.PIPE))
    return shell_result


def ping_ip_addresses(ip_list, limit=3):
    reach_ip = []
    unreach_ip = []
    regex = re.compile(r" 0% packet loss")
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_one_address, ip_list)
        for r, ip in zip(result, ip_list):
            if regex.search(r):
                reach_ip.append(ip)
            else:
                unreach_ip.append(ip)
    return(reach_ip, unreach_ip)

if __name__ == "__main__":
    ip_list = ["8.8.8.8", "8.8.4.4", "77.88.8.8", "1.1.2.3"]
    print(ping_ip_addresses(ip_list))
