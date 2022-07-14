# -*- coding: utf-8 -*-
"""
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Вывод сети и маски должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов (в двоичном формате
  надо добавить два пробела между столбцами
  для разделения октетов между собой)

Подсказка: Получить маску в двоичном формате можно так:
In [1]: "1" * 28 + "0" * 4
Out[1]: '11111111111111111111111111110000'


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

prefix_str = input("Input ip address like 10.1.1.0/24: " )
subnet_str = prefix_str.split("/")[0]
mask_str = prefix_str.split("/")[1]

first_oct = int(subnet_str.split(".")[0])
second_oct = int(subnet_str.split(".")[1])
third_oct = int(subnet_str.split(".")[2])
fourth_oct = int(subnet_str.split(".")[3])

mask_bin_str = "1" * int(mask_str) + "0" * (32- int(mask_str))
first_mask = int(mask_bin_str[:8], 2)
second_mask = int(mask_bin_str[8:16], 2)
third_mask = int(mask_bin_str[16:24], 2)
fourth_mask = int(mask_bin_str[24:32], 2)

print("""
Network:
{:<10}{:<10}{:<10}{:<10}
{:08b}  {:08b}  {:08b}  {:08b}

Mask:
/{}
{:<10}{:<10}{:<10}{:<10}
{:08b}  {:08b}  {:08b}  {:08b}
""".format(first_oct, second_oct, third_oct, fourth_oct, first_oct, second_oct, third_oct, fourth_oct, mask_str, first_mask, second_mask, third_mask, fourth_mask, first_mask, second_mask, third_mask, fourth_mask))
