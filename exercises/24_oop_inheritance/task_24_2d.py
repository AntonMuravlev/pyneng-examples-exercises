# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."
"""
import re
from netmiko.cisco.cisco_ios import CiscoIosSSH


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


class MyNetmiko(CiscoIosSSH):

    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.enable()

    def _check_error_in_command(self, command, output):
        if re.search(r"% (.*)", output):
            raise ErrorInCommand(f'При выполнении команды "{command}" на устройстве {self.host} возникла ошибка "{re.search(r"% (.*)",output).group(1)}"')

    def send_command(self, command, *args, **kwargs):
        output = super().send_command(command, **kwargs)
        self._check_error_in_command(command, output)
        return output

    def send_config_set(self, command, ignore_errors=True, *args, **kwargs):
        if type(command) == str:
            command = [command]
        output = ""
        self.config_mode()
        for cmd in command:
            temp_output = super().send_config_set(cmd, exit_config_mode=False)
            if ignore_errors == False:
                self._check_error_in_command(cmd, temp_output)
            output +=temp_output
        self.exit_config_mode()
        return output
if __name__ == "__main__":

    device_params = {
        "device_type": "cisco_ios",
        "ip": "192.168.122.101",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    r1 = MyNetmiko(**device_params)
#    print(r1.send_command("show ip int br"))
#    print(r1.send_command("show ipdfint br"))
    print(r1.send_config_set(['int loopback99', 'ip address 9.9.9.das9 255.255.255.255'], ignore_errors=False))
