import winreg
import os
import sys
import time
import random
import string
import re
import socket
import getpass
from datetime import datetime

# Base Paths for Camera and Microphone
REG_PATHS = {
    "CAMERA": r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam",
    "MICROPHONE": r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone"
}

# Terminal Colors
GREEN = '\033[92m'
RED = '\033[91m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_action(action):
    try:
        with open("system_override.log", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {action}\n")
    except:
        pass

def get_clean_app_name(raw_name):
    if '\\' in raw_name or '/' in raw_name or '.exe' in raw_name.lower():
        name = raw_name.replace('\\', '/').split('/')[-1]
        return name.replace('.exe', '').replace('.EXE', '').title()
        
    name = raw_name.split('_')[0]
    for prefix in ['Microsoft.', 'Windows.', 'App.', 'Zune']:
        if name.startswith(prefix):
            name = name.replace(prefix, '', 1)
            
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    name = name.replace('.', ' ').strip()
    return name if name else raw_name.split('_')[0]

def hacker_intro():
    """Start hone par 20 se 30 second ka hacking intro"""
    clear_screen()
    os.system('color 0A')
    
    duration = random.randint(20, 30)
    end_time = time.time() + duration
    
    print(f"{GREEN}Initiating System Hook... (Press Ctrl+C to skip if you are impatient){RESET}")
    time.sleep(1)
    
    try:
        while time.time() < end_time:
            mode = random.randint(1, 10)
            if mode <= 3:
                hex_dump = " ".join([f"0x{random.randint(0, 255):02X}" for _ in range(12)])
                print(f"[BOOT_SEQ] MemAddr: {hex_dump}")
            elif mode <= 7:
                bin_stream = "".join([str(random.randint(0, 1)) for _ in range(85)])
                print(bin_stream)
            else:
                actions = ["Bypassing Windows Defender...", "Fetching CapabilityAccessManager keys...", 
                           "Decrypting SAM Database...", "Loading Rootkit Module..."]
                print(f"{YELLOW}[*] {random.choice(actions)}{GREEN}")
            
            time.sleep(0.015) # Fast scroll
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] SKIP COMMAND RECEIVED. BOOTING MAIN FRAME...{RESET}")
        time.sleep(0.5)

    print(f"\n{RED}[+] SYSTEM COMPROMISED. ROOT ACCESS GRANTED.{RESET}")
    time.sleep(1.5)

def execute_hacker_payload():
    """Command execute karne se pehle 20-40 sec ka scroll"""
    clear_screen()
    os.system('color 0A')
    
    duration = random.randint(20, 40)
    end_time = time.time() + duration
    
    print(f"{RED}[!] DEPLOYING OVERRIDE PAYLOAD... (ETA: {duration}s) [Ctrl+C to Skip]{GREEN}\n")
    time.sleep(1)
    
    fake_ips = [f"192.168.{random.randint(1,255)}.{random.randint(1,255)}" for _ in range(10)]
    
    try:
        while time.time() < end_time:
            mode = random.randint(1, 100)
            if mode <= 30:
                print(f"[INJECT] Writing to registry block {random.randint(1000,9999)}... OK")
            elif mode <= 60:
                print("".join([str(random.randint(0, 1)) for _ in range(80)]))
            elif mode <= 85:
                gibberish = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
                print(f"[DECRYPT] HASH: {gibberish}")
            else:
                print(f"{YELLOW}[TRACE] Bouncing connection via {random.choice(fake_ips)}...{GREEN}")
            
            time.sleep(0.02)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] MANUAL OVERRIDE. SKIPPING PAYLOAD ANIMATION...{RESET}")
        time.sleep(0.5)

    print(f"\n{RED}[+] PAYLOAD EXECUTED SUCCESSFULLY.{RESET}")
    time.sleep(1.5)

def get_all_apps(target_type="CAMERA"):
    apps = []
    base_path = REG_PATHS[target_type]
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_path, 0, winreg.KEY_READ)
        for i in range(winreg.QueryInfoKey(key)[0]):
            app = winreg.EnumKey(key, i)
            if app != "NonPackaged":
                apps.append({"name": app, "parent": base_path, "path": app})
        
        np_path = base_path + r"\NonPackaged"
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
            print(f"\n{RED}[!] TARGET NEUTRALIZED: Access strictly BLOCKED.{RESET}")
        elif action == "allow":
            winreg.SetValueEx(key, "Value", 0, winreg.REG_SZ, "Allow")
            print(f"\n{CYAN}[!] TARGET WHITELISTED: Access GRANTED.{RESET}")
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

def show_banner(target_type):
    user = getpass.getuser()
    hostname = socket.gethostname()
    banner = f"""{GREEN}
  _    _          _____ _  __ ______ _____  
 | |  | |   /\   / ____| |/ /|  ____|  __ \ 
 | |__| |  /  \ | |    | ' / | |__  | |__) |
 |  __  | / /\ \| |    |  <  |  __| |  _  / 
 | |  | |/ ____ \ |____| . \ | |____| | \ \ 
 |_|  |_/_/    \_\_____|_|\_\|______|_|  \_\
                                            
 :: SPYWARE & PERMISSION EXPLOIT MODULE ::  
{RESET}
{YELLOW}SYS_USER:{RESET} {user}@{hostname} | {YELLOW}OS:{RESET} {os.name.upper()} 
{YELLOW}CURRENT TARGET:{RESET} {RED if target_type == "CAMERA" else CYAN}[ {target_type} ]{RESET}
"""
    print(banner)

def main_menu():
    # Application startup intro (20-30s)
    hacker_intro()
    
    current_target = "CAMERA"

    while True:
        clear_screen()
        os.system('color 0A')
        show_banner(current_target)
        
        apps = get_all_apps(current_target)
        
        if not apps:
            print(f"{RED}[!] NO APPLICATIONS FOUND REQUESTING {current_target} ACCESS.{RESET}")
        else:
            print(f"{CYAN}{'ID':<3} | {'APP NAME (CLEANED)':<28} | {'LIVE STATUS':<15} | {'AUTHORIZATION'}{RESET}")
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

                print(f"[{idx:<1}] | {app['display_name'][:26]:<28} | {active_text:<24} | {perm_styled}")
            
            print(GREEN + "-" * 75 + RESET)

        print(f"\n{YELLOW}COMMAND TERMINAL:{RESET}")
        print(f" {GREEN}B <ID>{RESET}  - Block App (e.g., B 2)")
        print(f" {GREEN}A <ID>{RESET}  - Allow App (e.g., A 2)")
        print(f" {GREEN}R{RESET}       - Reset All Permissions for {current_target}")
        print(f" {GREEN}SW{RESET}      - Switch Target (Camera <-> Microphone)")
        print(f" {GREEN}Q{RESET}       - Exit Protocol")
        
        choice = input(f"\n{RED}root@sys_override:~# {RESET}").strip().upper().split()
        
        if not choice:
            continue
            
        cmd = choice[0]
        
        if cmd == 'Q':
            print(f"\n{CYAN}[*] Wiping traces and disconnecting...{RESET}")
            time.sleep(1)
            break
            
        elif cmd == 'SW':
            current_target = "MICROPHONE" if current_target == "CAMERA" else "CAMERA"
            print(f"\n{YELLOW}[*] Switching target payload to {current_target}...{RESET}")
            time.sleep(1)
            
        elif cmd == 'R':
            confirm = input(f"{YELLOW}[?] WIPE ALL {current_target} PERMISSIONS? (Y/N): {RESET}")
            if confirm.upper() == 'Y':
                execute_hacker_payload() # 20-40 sec intro
                for app in apps:
                    modify_permission(app["full_path"], "reset")
                log_action(f"RESET ALL PERMISSIONS for {current_target}")
                print(f"\n{CYAN}[+] ALL {current_target} PERMISSIONS WIPED SUCCESSFULLY!{RESET}")
                input(f"\n{GREEN}Press Enter to return...{RESET}")
                
        elif cmd in ['B', 'A'] and len(choice) > 1:
            if choice[1].isdigit():
                idx = int(choice[1])
                if 0 <= idx < len(apps):
                    app = apps[idx]
                    action = "block" if cmd == 'B' else "allow"
                    
                    execute_hacker_payload() # 20-40 sec intro
                    
                    if modify_permission(app["full_path"], action):
                        log_action(f"{action.upper()}ED app: {app['display_name']} ({current_target})")
                    
                    input(f"\n{GREEN}Press Enter to return to main frame...{RESET}")
                else:
                    input(f"{RED}[X] INVALID TARGET ID! Press Enter...{RESET}")
            else:
                input(f"{RED}[X] COMMAND SYNTAX ERROR. Use format: B 2 or A 2. Press Enter...{RESET}")
        else:
            input(f"{RED}[X] UNKNOWN COMMAND! Press Enter...{RESET}")

if __name__ == "__main__":
    if os.name != 'nt':
        print("[X] FATAL ERROR: This payload is designed for Windows architecture only.")
        sys.exit()
    main_menu()
