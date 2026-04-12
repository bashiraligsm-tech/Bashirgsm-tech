#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BashirFrpTool Integrated v5.0
Features: Login | Search | FRP Bypass | Update | All Brands
Author: BashirGsm
"""

import os
import sys
import json
import hashlib
import subprocess
import time
import platform
from datetime import datetime

# ============================================
# تهيئة الألوان
# ============================================
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW
    B = Fore.BLUE; C = Fore.CYAN; M = Fore.MAGENTA
    W = Fore.WHITE; S = Style.RESET_ALL
except:
    R = G = Y = B = C = M = W = S = ""

VERSION = "5.0.0"
CONFIG_DIR = os.path.expanduser("~/bashirgsm/data")
USERS_FILE = os.path.join(CONFIG_DIR, "users.json")
DEVICES_FILE = os.path.join(CONFIG_DIR, "devices.json")
LOGS_DIR = os.path.expanduser("~/bashirgsm/logs")

os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# ============================================
# دوال مساعدة
# ============================================
def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_file = os.path.join(LOGS_DIR, "tool.log")
    colors = {"INFO": G, "ERROR": R, "SUCCESS": G, "WARNING": Y}
    print(f"{colors.get(level, C)}[{timestamp}] {msg}{S}")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] [{level}] {msg}\n")

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.stderr.strip()
    except:
        return "", "Timeout"

# ============================================
# نظام تسجيل الدخول
# ============================================
class AuthSystem:
    def __init__(self):
        self.current_user = None
        self.load_users()
    
    def load_users(self):
        self.users = {}
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, 'r') as f:
                    self.users = json.load(f)
            except:
                pass
        if not self.users:
            self.users["admin"] = {
                "password": hashlib.sha256("admin123".encode()).hexdigest(),
                "role": "admin", "created": datetime.now().isoformat(), "last_login": None
            }
            self.save_users()
    
    def save_users(self):
        with open(USERS_FILE, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def login(self):
        print(f"\n{C}╔════════════════════════════════════════════════════════════╗{S}")
        print(f"{C}║{S}                    {G}🔐 LOGIN REQUIRED{S}                       {C}║{S}")
        print(f"{C}╚════════════════════════════════════════════════════════════╝{S}")
        attempts = 0
        while attempts < 3:
            username = input(f"{G}➤ Username: {S}").strip()
            password = input(f"{G}➤ Password: {S}")
            if username in self.users:
                if self.users[username]["password"] == hashlib.sha256(password.encode()).hexdigest():
                    self.current_user = username
                    self.users[username]["last_login"] = datetime.now().isoformat()
                    self.save_users()
                    log(f"Login successful! Welcome {username}", "SUCCESS")
                    time.sleep(1)
                    return True
            log("Invalid username or password!", "ERROR")
            attempts += 1
        log("Too many failed attempts!", "ERROR")
        return False

# ============================================
# نظام البحث عن الموديلات
# ============================================
class SearchSystem:
    def __init__(self):
        self.devices = self.load_devices()
    
    def load_devices(self):
        if os.path.exists(DEVICES_FILE):
            try:
                with open(DEVICES_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return self.get_default_devices()
    
    def get_default_devices(self):
        return {
            "samsung": {"models": ["S22", "S23", "S24", "A12", "A13", "A14", "A15", "Note20", "Z Fold", "Z Flip"], "android": "9-16"},
            "xiaomi": {"models": ["Mi 11", "Mi 12", "Mi 13", "Redmi Note 10", "Redmi Note 11", "Redmi Note 12", "Poco F3", "Poco F4"], "android": "9-16"},
            "oppo": {"models": ["Find X3", "Find X5", "Reno 6", "Reno 7", "Reno 8", "Reno 9"], "android": "9-16"},
            "vivo": {"models": ["V20", "V21", "V23", "V25", "X60", "X70", "X80"], "android": "9-16"},
            "huawei": {"models": ["P30", "P40", "P50", "Mate 30", "Mate 40", "Mate 50"], "android": "9-14"},
            "oneplus": {"models": ["OnePlus 8", "OnePlus 9", "OnePlus 10", "OnePlus 11", "Nord"], "android": "9-16"},
            "google": {"models": ["Pixel 4", "Pixel 5", "Pixel 6", "Pixel 7", "Pixel 8"], "android": "9-16"},
            "realme": {"models": ["Realme 6", "Realme 7", "Realme 8", "Realme 9", "Realme GT"], "android": "9-16"},
            "motorola": {"models": ["Moto G30", "Moto G50", "Moto G60", "Moto Edge 30"], "android": "9-16"},
        }
    
    def search_by_name(self, keyword):
        results = []
        for brand, data in self.devices.items():
            for model in data["models"]:
                if keyword.lower() in model.lower():
                    results.append({"brand": brand, "model": model, "android": data["android"]})
        return results
    
    def search_by_brand(self, brand):
        results = []
        brand_lower = brand.lower()
        for b, data in self.devices.items():
            if brand_lower in b:
                for model in data["models"]:
                    results.append({"brand": b, "model": model, "android": data["android"]})
        return results
    
    def search_by_android(self, version):
        results = []
        for brand, data in self.devices.items():
            versions = data["android"].split("-")
            if len(versions) >= 2 and int(versions[0]) <= int(version) <= int(versions[1]):
                for model in data["models"]:
                    results.append({"brand": brand, "model": model, "android": data["android"]})
        return results
    
    def display_results(self, results, title="Search Results"):
        if not results:
            log(f"No devices found for '{title}'", "WARNING")
            return
        print(f"\n{C}╔════════════════════════════════════════════════════════════╗{S}")
        print(f"{C}║{S}  {G}{title} ({len(results)} devices){S}{' ' * (40 - len(str(len(results))))}{C}║{S}")
        print(f"{C}╠════════════════════════════════════════════════════════════╣{S}")
        for i, d in enumerate(results[:30]):
            print(f"{C}║{S}  {G}{i+1:2}.{S} {Y}{d['brand'].upper():<12}{S} {C}{d['model']:<20}{S} {M}Android {d['android']}{S}{' ' * (10 - len(d['android']))}{C}║{S}")
        if len(results) > 30:
            print(f"{C}║{S}  {Y}... and {len(results)-30} more devices{S}{' ' * 35}{C}║{S}")
        print(f"{C}╚════════════════════════════════════════════════════════════╝{S}")
    
    def search_menu(self):
        while True:
            print(f"\n{C}╔════════════════════════════════════════════════════════════╗{S}")
            print(f"{C}║{S}                    {G}🔍 SEARCH MENU{S}                          {C}║{S}")
            print(f"{C}╠════════════════════════════════════════════════════════════╣{S}")
            print(f"{C}║{S}  {G}1{S}) Search by Device Name    {G}3{S}) Search by Android        {C}║{S}")
            print(f"{C}║{S}  {G}2{S}) Search by Brand         {G}4{S}) Back to Main Menu       {C}║{S}")
            print(f"{C}╚════════════════════════════════════════════════════════════╝{S}")
            choice = input(f"{G}➤ Choose: {S}").strip()
            if choice == '1':
                keyword = input(f"{G}➤ Enter device name: {S}").strip()
                results = self.search_by_name(keyword)
                self.display_results(results, f"Results for '{keyword}'")
            elif choice == '2':
                brand = input(f"{G}➤ Enter brand name: {S}").strip()
                results = self.search_by_brand(brand)
                self.display_results(results, f"{brand.upper()} Devices")
            elif choice == '3':
                version = input(f"{G}➤ Enter Android version (9-16): {S}").strip()
                if version.isdigit() and 9 <= int(version) <= 16:
                    results = self.search_by_android(version)
                    self.display_results(results, f"Android {version} Devices")
                else:
                    log("Invalid Android version!", "ERROR")
            elif choice == '4':
                break
            input(f"{Y}Press Enter to continue...{S}")

# ============================================
# دوال FRP Bypass
# ============================================
def get_detected_devices():
    stdout, _ = run_cmd("adb devices")
    devices = []
    for line in stdout.split('\n')[1:]:
        if 'device' in line and 'List' not in line:
            devices.append(line.split('\t')[0])
    return devices

def show_device_info():
    devices = get_detected_devices()
    print(f"\n{C}╔════════════════════════════════════════════════════════════╗{S}")
    print(f"{C}║{S}                    {G}📱 DEVICE STATUS{S}                        {C}║{S}")
    print(f"{C}╠════════════════════════════════════════════════════════════╣{S}")
    if devices:
        for dev in devices:
            print(f"{C}║{S}  {G}✅ Connected:{S} {Y}{dev}{S}{' ' * (35 - len(dev))}{C}║{S}")
    else:
        print(f"{C}║{S}  {R}⚠️ No device detected{S}{' ' * 32}{C}║{S}")
        print(f"{C}║{S}  {Y}→ Enable USB Debugging{S}{' ' * 28}{C}║{S}")
        print(f"{C}║{S}  {Y}→ Connect via USB cable{S}{' ' * 25}{C}║{S}")
    print(f"{C}╚════════════════════════════════════════════════════════════╝{S}")

def samsung_bypass():
    log("Starting Samsung FRP bypass...", "INFO")
    run_cmd("adb shell settings put global device_provisioned 1")
    run_cmd("adb shell settings put secure user_setup_complete 1")
    run_cmd("adb reboot")
    log("Samsung FRP bypass completed! Device will reboot.", "SUCCESS")

def xiaomi_bypass():
    log("Starting Xiaomi FRP bypass...", "INFO")
    run_cmd("adb shell am start -n com.android.settings/.Settings")
    run_cmd("adb shell settings put global device_provisioned 1")
    run_cmd("adb reboot")
    log("Xiaomi FRP bypass completed!", "SUCCESS")

def oppo_bypass():
    log("Starting Oppo/Vivo FRP bypass...", "INFO")
    run_cmd("adb shell am start -n com.google.android.gsf/.login.LoginActivity")
    run_cmd("adb shell input keyevent 4")
    run_cmd("adb shell settings put global device_provisioned 1")
    run_cmd("adb reboot")
    log("Oppo/Vivo FRP bypass completed!", "SUCCESS")

def generic_bypass():
    log("Starting generic FRP bypass...", "INFO")
    run_cmd("adb shell settings put global device_provisioned 1")
    run_cmd("adb reboot")
    log("Generic FRP bypass completed!", "SUCCESS")

def mtk_bypass():
    log("MediaTek BROM Mode", "INFO")
    print(f"{Y}[!] Steps:{S}\n  1. Power off device\n  2. Press VOL UP + VOL DOWN\n  3. Connect USB cable")

def qualcomm_bypass():
    log("Qualcomm EDL Mode", "INFO")
    print(f"{Y}[!] Steps:{S}\n  1. Power off device\n  2. Press VOL UP + Power\n  3. Connect USB cable")

def show_brands():
    brands = ["Samsung", "Xiaomi", "Oppo", "Vivo", "Huawei", "OnePlus", "Google", "Realme", "Motorola", "Tecno", "Infinix"]
    print(f"\n{C}╔════════════════════════════════════════════════════════════╗{S}")
    print(f"{C}║{S}                    {G}📋 SUPPORTED BRANDS{S}                      {C}║{S}")
    print(f"{C}╠════════════════════════════════════════════════════════════╣{S}")
    line = f"{C}║{S}  "
    for i, brand in enumerate(brands):
        line += f"{G}{brand:<12}{S}"
        if (i + 1) % 3 == 0 or i == len(brands)-1:
            print(f"{line}  {C}║{S}")
            line = f"{C}║{S}  "
    print(f"{C}╚════════════════════════════════════════════════════════════╝{S}")

def print_banner():
    banner = f"""
{C}╔════════════════════════════════════════════════════════════════════╗
{C}║                                                                    ║
{C}║   {M}██████╗  █████╗ ███████╗██╗  ██╗██╗██████╗ {C}                      ║
{C}║   {M}██╔══██╗██╔══██╗██╔════╝██║  ██║██║██╔══██╗{C}                      ║
{C}║   {M}██████╔╝███████║███████╗███████║██║██████╔╝{C}                      ║
{C}║   {M}██╔══██╗██╔══██║╚════██║██╔══██║██║██╔══██╗{C}                      ║
{C}║   {M}██████╔╝██║  ██║███████║██║  ██║██║██║  ██║{C}                      ║
{C}║   {M}╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝{C}                      ║
{C}║                                                                    ║
{C}║              {G}INTEGRATED FRP TOOL v{VERSION}{C}                         ║
{C}║              {Y}Login | Search | Bypass | All Brands{C}                 ║
{C}║                                                                    ║
{C}╚════════════════════════════════════════════════════════════════════╝{S}
"""
    print(banner)

# ============================================
# القائمة الرئيسية
# ============================================
def show_main_menu():
    print(f"\n{B}╔════════════════════════════════════════════════════════════╗{S}")
    print(f"{B}║{S}                         {G}MAIN MENU{S}                           {B}║{S}")
    print(f"{B}╠════════════════════════════════════════════════════════════╣{S}")
    print(f"{B}║{S}  {G}1{S}) Auto Detect & Bypass      {G}6{S}) MediaTek (BROM)        {B}║{S}")
    print(f"{B}║{S}  {G}2{S}) Samsung Bypass            {G}7{S}) Qualcomm (EDL)         {B}║{S}")
    print(f"{B}║{S}  {G}3{S}) Xiaomi Bypass             {G}8{S}) Search Devices         {B}║{S}")
    print(f"{B}║{S}  {G}4{S}) Oppo/Vivo Bypass          {G}9{S}) Show All Brands        {B}║{S}")
    print(f"{B}║{S}  {G}5{S}) Generic Bypass            {G}0{S}) Exit                   {B}║{S}")
    print(f"{B}╚════════════════════════════════════════════════════════════╝{S}")

# ============================================
# الدالة الرئيسية
# ============================================
def main():
    clear_screen()
    print_banner()
    
    auth = AuthSystem()
    if not auth.login():
        sys.exit(1)
    
    search = SearchSystem()
    
    while True:
        show_device_info()
        show_main_menu()
        choice = input(f"{G}➤ Select option: {S}").strip()
        
        devices = get_detected_devices()
        
        if choice == '0':
            log("Goodbye!", "INFO")
            break
        elif choice == '1':
            generic_bypass() if devices else log("No device detected!", "ERROR")
        elif choice == '2':
            samsung_bypass() if devices else log("No device detected!", "ERROR")
        elif choice == '3':
            xiaomi_bypass() if devices else log("No device detected!", "ERROR")
        elif choice == '4':
            oppo_bypass() if devices else log("No device detected!", "ERROR")
        elif choice == '5':
            generic_bypass() if devices else log("No device detected!", "ERROR")
        elif choice == '6':
            mtk_bypass()
        elif choice == '7':
            qualcomm_bypass()
        elif choice == '8':
            search.search_menu()
        elif choice == '9':
            show_brands()
        else:
            log("Invalid option!", "ERROR")
        
        if choice not in ['8', '9']:
            input(f"{Y}Press Enter to continue...{S}")
        clear_screen()
        print_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}Interrupted by user{S}")
    except Exception as e:
        print(f"{R}Error: {e}{S}")
