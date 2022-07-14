# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


"""

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        temp_topology = {}
        for key, value in topology_dict.items():
            if not temp_topology.get(value) == key:
                temp_topology[key] = value
        return temp_topology

    def delete_link(self, local_port, remote_port):
        if local_port in self.topology.keys() and self.topology[local_port] == remote_port:
            del self.topology[local_port]
        elif remote_port in self.topology.keys() and self.topology[remote_port] == local_port:
            del self.topology[remote_port]
        else:
            print("Такого соединения нет")

    def delete_node(self, del_node):
        links_list = list(self.topology.items())
        del_flag = False
        for link in links_list:
            if del_node == link[0][0] or del_node == link[1][0]:
                del self.topology[link[0]]
                del_flag = True
        if not del_flag:
            print("Такого устройства нет")

    def add_link(self, new_l_link, new_r_link):
        new_link = (new_l_link, new_r_link)
        reverse_link = (new_r_link, new_l_link)
        all_ports = list(self.topology.keys()) + list(self.topology.values())
        if new_link in list(self.topology.items()) or reverse_link in list(self.topology.items()):
            print("Такое соединение существует")
        elif new_l_link in all_ports or new_r_link in all_ports:
            print("Cоединение с одним из портов существует")
        else:
            self.topology[new_l_link] = new_r_link


if __name__ == "__main__":

    topology_example = {
        ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
        ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
        ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
        ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
        ("R3", "Eth0/1"): ("R4", "Eth0/0"),
        ("R3", "Eth0/2"): ("R5", "Eth0/0"),
        ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
        ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
        ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
    }

    top = Topology(topology_example)
    print(top.topology)
    top.add_link((("R33", "Eth0/0"), ("SW11", "Eth0/3")))
    print(top.topology)
