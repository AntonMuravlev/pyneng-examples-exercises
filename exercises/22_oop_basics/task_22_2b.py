# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

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
    def send_config_commands(self, command):
        if type(command) == str:
            self._write_line('conf t' + '\n' + f'{command}' + '\n' + 'end')
            time.sleep(0.5)
            return self.telnet.read_very_eager().decode('utf-8')
        elif type(command) == list:
            self._write_line('conf t')
            for cmd in command:
                self._write_line(cmd)
            self._write_line('end')
            time.sleep(0.5)
            return self.telnet.read_very_eager().decode('utf-8')

if __name__ == "__main__":
    with open('devices.yaml') as f:
        dev_params = yaml.safe_load(f)[0]
    r1 = CiscoTelnet(**dev_params)
    print(r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255']))
