import winreg
import os
import sys
import time
import random
import string
import re

# Registry Path
BASE_REG_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"

# Terminal Colors
GREEN = '\033[92m'
RED = '\033[91m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Padhne yogya (Readable) App name banane ka function
def get_clean_app_name(raw_name):
    # Desktop apps (jaise C:\Program Files\Google\Chrome.exe)
    if '\\' in raw_name or '/' in raw_name or '.exe' in raw_name.lower():
        name = raw_name.replace('\\', '/').split('/')[-1]
        return name.replace('.exe', '').replace('.EXE', '').title()
        
    # Store apps (jaise Microsoft.WindowsCamera_8wekyb3d8bbwe)
    name = raw_name.split('_')[0] # Underscore ke baad ka kachra hatao
    
    # Faltu prefixes hatao
    for prefix in ['Microsoft.', 'Windows.', 'App.', 'Zune']:
        if name.startswith(prefix):
            name = name.replace(prefix, '', 1)
            
    # CamelCase words ko alag karo (e.g. SkypeApp -> Skype App)
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    name = name.replace('.', ' ').strip()
    
    return name if name else raw_name.split('_')[0]

def execute_hacker_payload():
    clear_screen()
    os.system('color 0A')
    
    # 20 se 40 second ka random time
    duration = random.randint(20, 40)
    end_time = time.time() + duration
    
    print(f"{RED}[!] INITIATING SYSTEM OVERRIDE PAYLOAD... (ETA: {duration}s){GREEN}\n")
    time.sleep(1)
    
    fake_ips = [f"{random.randint(11,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}" for _ in range(30)]
    
    try:
        while time.time() < end_time:
            mode = random.randint(1, 100)
            
            # Alag-alag tarike ke hacking scrolls
            if mode <= 25:
                # 1. Memory Hex Dump
                hex_line = " ".join([f"0x{random.randint(0, 255):02X}" for _ in range(10)])
                print(f"[MEM_ALLOC] Addr: {hex_line} | BYPASSED")
            
            elif mode <= 50:
                # 2. Binary Stream
                bin_line = "".join([str(random.randint(0, 1)) for _ in range(85)])
                print(f"{bin_line}")
                
            elif mode <= 75:
                # 3. Network Connection Tracing
                print(f"[TRACE] Re-routing traffic through proxy {random.choice(fake_ips)}... OK")
                
            elif mode <= 90:
                # 4. Decryption Brute Force
                gibberish = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
                print(f"[DECRYPT] Cracking registry key hash: {gibberish} ... FAILED")
                
            else:
                # 5. Core Actions
                actions = [
                    "Injecting DLL into target process...",
                    "Overwriting Windows Defender telemetry...",
                    "Escalating privileges to SYSTEM...",
                    "Modifying CapabilityAccessManager keys..."
                ]
                print(f"{YELLOW}[*] {random.choice(actions)}{GREEN}")
            
            # 8x Speed ka delay
            time.sleep(0.015)
            
    except KeyboardInterrupt:
        # Agar user Ctrl+C dabaye toh skip ho jayega
        print(f"\n{YELLOW}[!] MANUAL OVERRIDE DETECTED. SKIPPING ANIMATION...{RESET}")
        time.sleep(0.5)

    print(f"\n{RED}[+] PAYLOAD DEPLOYED SUCCESSFULLY.{RESET}")
    time.sleep(1.5)

def get_all_apps():
    apps = []
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, BASE_REG_PATH, 0, winreg.KEY_READ)
        for i in range(winreg.QueryInfoKey(key)[0]):
            app = winreg.EnumKey(key, i)
            if app != "NonPackaged":
                apps.append({"name": app, "parent": BASE_REG_PATH, "path": app})
        
        np_path = BASE_REG_PATH + r"\NonPackaged"
        try:
            np_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, np_path, 0, winreg.KEY_READ)
            for i in range(winreg.QueryInfoKey(np_key)[0]):
                app = winreg.EnumKey(np_key, i)
                apps.append({"name": app, "parent": np_path, "path": app})
            winreg.CloseKey(np_key)
        except FileNotFoundError:
            pass
        winreg.CloseKey(key)
    except Exception:
        pass

    for app in apps:
        app_key_path = app["parent"] + "\\" + app["path"]
        try:
            app_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, app_key_path, 0, winreg.KEY_READ)
            try:
                val, _ = winreg.QueryValueEx(app_key, "Value")
                app["permission"] = val
            except FileNotFoundError:
                app["permission"] = "Prompt"
            
            try:
                last_stop, _ = winreg.QueryValueEx(app_key, "LastUsedTimeStop")
                app["is_active"] = (last_stop == 0)
            except FileNotFoundError:
                app["is_active"] = False
                
            app["full_path"] = app_key_path
            
            # Yahan hum naya clean name generate kar rahe hain
            app["display_name"] = get_clean_app_name(app["name"])
            winreg.CloseKey(app_key)
        except:
            pass
            
    return apps

def modify_permission(app_reg_path, action):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, app_reg_path, 0, winreg.KEY_SET_VALUE)
        if action == "block":
            winreg.SetValueEx(key, "Value", 0, winreg.REG_SZ, "Deny")
            print(f"\n{RED}[!] TARGET NEUTRALIZED: Camera access strictly BLOCKED.{RESET}")
        elif action == "reset":
            try:
                winreg.DeleteValue(key, "Value") 
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
        return True
    except PermissionError:
        print(f"\n{RED}[X] ACCESS DENIED: Requires Admin Privileges.{RESET}")
        return False
    except Exception as e:
        print(f"\n{RED}[X] ERROR: {e}{RESET}")
        return False

def show_banner():
    banner = f"""{GREEN}
  _    _          _____ _  __ ______ _____  
 | |  | |   /\   / ____| |/ /|  ____|  __ \ 
 | |__| |  /  \ | |    | ' / | |__  | |__) |
 |  __  | / /\ \| |    |  <  |  __| |  _  / 
 | |  | |/ ____ \ |____| . \ | |____| | \ \ 
 |_|  |_/_/    \_\_____|_|\_\|______|_|  \_\
                                            
 :: ADVANCED CAMERA EXPLOIT & MANAGER ::  
{RESET}"""
    print(banner)

def main_menu():
    # Chota intro script start hone par
    clear_screen()
    os.system('color 0A')
    print(f"{GREEN}[*] Bypassing Windows Security... OK")
    time.sleep(0.5)
    print(f"[*] Accessing CapabilityAccessManager... OK{RESET}")
    time.sleep(0.5)

    while True:
        clear_screen()
        os.system('color 0A')
        show_banner()
        
        apps = get_all_apps()
        if not apps:
            print(f"{RED}[!] NO TARGETS FOUND ON THIS SYSTEM.{RESET}")
            break

        print(f"{CYAN}{'ID':<4} | {'APP NAME (CLEANED)':<30} | {'LIVE STATUS':<15} | {'AUTHORIZATION'}{RESET}")
        print(GREEN + "-" * 75 + RESET)
        
        for idx, app in enumerate(apps):
            if app.get("is_active"):
                active_text = f"{RED}◉ SPYING NOW{RESET}"
            else:
                active_text = f"{GREEN}○ OFFLINE{RESET}"
                
            perm = app.get('permission')
            if perm == "Deny":
                perm_styled = f"{RED}BLOCKED{RESET}"
            elif perm == "Allow":
                perm_styled = f"{CYAN}GRANTED{RESET}"
            else:
                perm_styled = f"{YELLOW}PROMPT{RESET}"

            print(f"[{idx:<2}] | {app['display_name'][:28]:<30} | {active_text:<24} | {perm_styled}")
        
        print(GREEN + "-" * 75 + RESET)
        print(f"\n{YELLOW}AVAILABLE EXPLOITS:{RESET}")
        print(f" {GREEN}[ID]{RESET} - Block target (Enter ID number like 0, 1, 2)")
        print(f" {GREEN}[R]{RESET}  - RESET ALL (Wipe all permissions from registry)")
        print(f" {GREEN}[Q]{RESET}  - Disconnect & Exit")
        
        choice = input(f"\n{RED}root@system:~# {RESET}").strip().lower()
        
        if choice == 'q':
            print(f"\n{CYAN}[*] Disconnecting from registry...{RESET}")
            time.sleep(1)
            break
        elif choice == 'r':
            confirm = input(f"{YELLOW}[?] ARE YOU SURE? Wipe all data? (y/n): {RESET}")
            if confirm.lower() == 'y':
                execute_hacker_payload() # 20-40 sec animation
                for app in apps:
                    modify_permission(app["full_path"], "reset")
                print(f"\n{CYAN}[+] ALL PERMISSIONS WIPED SUCCESSFULLY!{RESET}")
                input(f"\n{GREEN}Press Enter to continue...{RESET}")
        elif choice.isdigit():
            idx = int(choice)
            if 0 <= idx < len(apps):
                app = apps[idx]
                execute_hacker_payload() # 20-40 sec animation
                modify_permission(app["full_path"], "block")
                input(f"\n{GREEN}Press Enter to return to main frame...{RESET}")
            else:
                input(f"{RED}[X] INVALID TARGET ID! Press Enter...{RESET}")
        else:
            input(f"{RED}[X] UNKNOWN COMMAND! Press Enter...{RESET}")

if __name__ == "__main__":
    if os.name != 'nt':
        print("[X] FATAL ERROR: This payload is designed for Windows architecture only.")
        sys.exit()
    main_menu()
