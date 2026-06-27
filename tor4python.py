import requests
import socks
import socket

# Metoda 1: Bezpośrednio w bibliotece requests
proxies = {
    'http': 'socks5://127.0.0.1:9052',
    'https': 'socks5://127.0.0.1:9052'
}
response = requests.get('https://check.torproject.org/api/ip', proxies=proxies)
print(response.text)

# Metoda 2: Globalne ustawienie socka (dla bibliotek używających socket)
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9052)
socket.socket = socks.socksocket
response = requests.get('https://check.torproject.org/api/ip')
print(response.text)