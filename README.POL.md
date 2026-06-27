# Tor Proxy Rotator

## Opis

Tor Proxy Rotator to narzędzie w języku Python, które automatycznie uruchamia i zarządza proxy Tor z funkcją rotacji adresu IP w określonych odstępach czasu.

## Funkcje

- Automatyczne uruchamianie procesu Tor
- Rotacja adresu IP co zdefiniowany interwał czasowy
- Obsługa portów SOCKS5
- Wykrywanie i zarządzanie zajętymi portami
- Automatyczne wyszukiwanie pliku wykonywalnego Tor
- Sprawdzanie aktualnego adresu IP przez proxy Tor
- Łatwe zatrzymywanie poprzez Ctrl+C

## Wymagania

- Python 3.x
- Biblioteki: `stem`, `requests`, `psutil`
- Plik wykonywalny Tor (`tor.exe`)


### Instalacja zależności Pythona

pip install stem requests psutil

### Konfiguracja 

Aby zmienic porty uzywane przez program oraz czas pomiedzy zmianami IP edytuj plik tpr.py
na koncu skryptu znajdziesz ...
SOCKS_PORT = 9052      # Zalecany port (bezpieczny i rzadko używany)
CONTROL_PORT = 9051    # Port kontrolny
ROTATION_INTERVAL = 10 # Czas pomiedzy zmianami IP, podany w sekundach

### Utworzony adres proxy: 

- localhost:9052 
- 127.0.0.1:9052

### Dodanie Proxy do przegladarek

#Chrome#

"Ustawienia"
"System"
"Otwórz ustawienia proxy"
"Ręczna konfiguracja serwera proxy"
Wprowadź adres i numer portu
Kliknij przycisk OK, aby zapisać zmiany.

#Firefox#

"Opcje"
"Sieć"
"Ręczna konfiguracja serwerów proxy"
Wprowadź adres i numer portu
Kliknij przycisk OK, aby zapisać zmiany.
Adres proxy to : localhost:9052   

### Obsługa Nmap

Nmap nie obsługuje natywnie proxy SOCKS. 
Aby skanować przez Tor, użyj narzędzia torsocks.
torsocks nmap -sT -Pn example.com

### Dodanie proxy do skryptu pythona 

tor4python.py

### Author

mediacoder666









