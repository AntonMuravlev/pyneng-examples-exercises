# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
        self.items = [(key, value) for key, value in self.topology.items()]
    def __add__(self, other):
        temp_dict1 = self.topology.copy()
        temp_dict1.update(other)
        return Topology(temp_dict1)
    def __getitem__(self, index):
        return self.items[index]
    def __iter__(self):
        print('Вызываю __iter__')
        return iter(self.topology.items())
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

    for link in top:
        print(link)
