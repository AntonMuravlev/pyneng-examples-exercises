# -*- coding: utf-8 -*-

"""
Задание 22.2a

Скопировать класс CiscoTelnet из задания 22.2 и изменить
метод send_show_command добавив три параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей,
  полученный после обработки с помощью TextFSM.
  При parse=True должен возвращаться список словарей, а parse=False обычный вывод.
  Значение по умолчанию - True.
* templates - путь к каталогу с шаблонами. Значение по умолчанию - "templates"
* index - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"


Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_22_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command("sh ip int br", parse=True)
Out[4]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'}]

In [5]: r1.send_show_command("sh ip int br", parse=False)
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status
Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up
up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up...'


"""
import telnetlib
import yaml
import time
from textfsm import clitable
class CiscoTelnet:
    def _write_line(self, line):
        self.telnet.write(f"{line}\n".encode("utf-8"))
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b'Username:')
        self._write_line(self.username)
        self.telnet.read_until(b'Password:')
        self._write_line(self.password)
        self.telnet.read_until(b'>')
        self._write_line('enable')
        self.telnet.read_until(b'Password:')
        self._write_line(self.secret)
        self.telnet.read_until(b'#')
        self._write_line("terminal length 0")
        #time.sleep(1)
        self.telnet.read_until(b'#')
    def send_show_command(self, show_command, parse=True, templates="templates", index="index"):
        attributes_dict = {
        "Command": show_command,
        "Vendor": "cisco_ios"
        }
        self._write_line(show_command)
        #time.sleep(1)
        output = self.telnet.read_until(b'#', timeout=5).decode("utf-8")
        if parse:
            cli_table = clitable.CliTable(index, templates)
            cli_table.ParseCmd(output, attributes_dict)
            return [dict(zip(cli_table.header, row)) for row in cli_table]
        return output


if __name__ == "__main__":
    with open('devices.yaml') as f:
        dev_params = yaml.safe_load(f)[0]
    r1 = CiscoTelnet(**dev_params)
    print(r1.send_show_command("show clock"))
