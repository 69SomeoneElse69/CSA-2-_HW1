import locale
import platform
import subprocess
from ipaddress import ip_address
from pprint import pprint
import threading
import time

result = []


def ip_or_url(value):
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    return ipv4


def ping(ipv4, result, get_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    response = subprocess.Popen(['ping', param, '1', str(ipv4)], stdout=subprocess.PIPE)
    if response.wait() == 0:
        result['Доступные узлы'] += f'{str(ipv4)}\n'
        res = f'{str(ipv4)} - доступен'
        if not get_list:
            print(res)
        return res
    else:
        result['Недоступные узлы'] += f'{str(ipv4)}\n'
        res = f'{str(ipv4)} - недоступен'
    if not get_list:
        print(res)
        return res


def host_ping(host_list, get_list=False):
    threads = []
    for host in host_list:
        try:
            ipv4 = ip_or_url(host)
        except Exception as e:
            print(f'{host} - {e} воспринимаю как доменное имя')
            ipv4 = host

        thread = threading.Thread(target=ping, args=(ipv4, result, get_list), deamon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if get_list:
        return result


host_list = ['0.8.8.8', 'yandex.ru', '192.168.8.1', '8.8.8.8', 'google.com', 'goоgle.com']
start = time.time()
host_ping(host_list)
end = time.time()
print(f'time: {int(end - start)}')
pprint(result)
