# -*i coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ip_string = input("Please input ip address in this way 10.0.0.1: ")
x = 0
if len(ip_string.split(".")) == 4:
    octet_list = ip_string.split(".")

    for octet in octet_list:
        x = x + 1
        try:
            if 0 <= int(octet) <= 255:
                if x == 4:
                    if 1 <= int(octet_list[0]) <= 223:
                        print("unicast")
                    elif 224 <= int(octet_list[0]) <= 239:
                        print("multicast")
                    elif ip_string == "255.255.255.255":
                        print("local broadcast")
                    elif ip_string == "0.0.0.0":
                        print("unassigned")
                    else:
                        print("unused")
            else:
                print("Неправильный IP-адрес")
                break
        except ValueError:
            print("Неправильный IP-адрес")
            break
else:
    print("Неправильный IP-адрес")
