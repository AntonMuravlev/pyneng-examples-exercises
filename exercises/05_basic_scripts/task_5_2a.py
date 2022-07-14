# -*- coding: utf-8 -*-
"""
Задание 5.2a

Всё, как в задании 5.2, но, если пользователь ввел адрес хоста, а не адрес сети,
надо преобразовать адрес хоста в адрес сети и вывести адрес сети и маску,
как в задании 5.2.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.195/28 - хост из сети 10.0.5.192/28

Если пользователь ввел адрес 10.0.1.1/24, вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000


Проверить работу скрипта на разных комбинациях хост/маска, например:
    10.0.5.195/28, 10.0.1.1/24

Вывод сети и маски должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов (в двоичном формате
  надо добавить два пробела между столбцами
  для разделения октетов между собой)


Подсказка:
Есть адрес хоста в двоичном формате и маска сети 28. Адрес сети это первые 28 бит
адреса хоста + 4 ноля.
То есть, например, адрес хоста 10.1.1.195/28 в двоичном формате будет
bin_ip = "00001010000000010000000111000011"

А адрес сети будет первых 28 символов из bin_ip + 0000 (4 потому что всего
в адресе может быть 32 бита, а 32 - 28 = 4)
00001010000000010000000111000000

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

prefix_str = input("Input ip address like 10.1.1.0/24: " )
subnet_str = prefix_str.split("/")[0]
mask_str = prefix_str.split("/")[1]

first_oct = int(subnet_str.split(".")[0])
second_oct = int(subnet_str.split(".")[1])
third_oct = int(subnet_str.split(".")[2])
fourth_oct = int(subnet_str.split(".")[3])

bin_ip = "{:08b}{:08b}{:08b}{:08b}".format(first_oct, second_oct, third_oct, fourth_oct)

bin_subnet = bin_ip[:int(mask_str)] + "0"*(32 - int(mask_str))

subnet_first = int(bin_subnet[:8], 2)
subnet_second = int(bin_subnet[8:16], 2)
subnet_third = int(bin_subnet[16:24], 2)
subnet_fourth = int(bin_subnet[24:32], 2)

mask_bin_str = "1" * int(mask_str) + "0" * (32 - int(mask_str))
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
""".format(subnet_first, subnet_second, subnet_third, subnet_fourth, subnet_first, subnet_second, subnet_third, subnet_fourth, mask_str, first_mask, second_mask, third_mask, fourth_mask, first_mask, second_mask, third_mask, fourth_mask))
