"""Using this script to configure
Tor and ProxyChains para di takaw aresto
Blessed by: PCA fam and PCM
Coded by ~Vend3ttA"""

from time import sleep
import os
import shutil
import sys
from colorama import Fore, init

init(autoreset=True)
CONFIG_FILE = "/etc/proxychains4.conf"
PROXIES = [
    ("socks5", "127.0.0.1", "9050"),
    ("http", "192.168.1.100", "8080"),
    ("socks4", "10.0.0.2", "1080")
]

def clear_terminal():
    os.system("clear" if os.name == "posix" else "cls")

def check_root():
    clear_terminal()
    if os.geteuid() != 0:
        sys.exit(Fore.RED + "Please run this script as root user." + Fore.RESET)

def load_config(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.readlines()
    return []

def modify_config(lines, proxies, strict_chain=True, random_chain=False, enable_dns=True):
    new_lines = []
    found_proxy_section = False

    for line in lines:
        if "strict_chain" in line and strict_chain:
            new_lines.append("strict_chain\n")
        elif "random_chain" in line:
            new_lines.append("random_chain\n" if random_chain else "# random_chain\n")
        elif "proxy_dns" in line and enable_dns:
            new_lines.append("proxy_dns\n")
        elif line.strip().startswith(("http", "socks4", "socks5")):
            if not found_proxy_section:
                found_proxy_section = True
            continue
        else:
            new_lines.append(line)

    new_lines.append("# Custom proxy list\n")
    for ptype, ip, port in proxies:
        new_lines.append(f"{ptype} {ip} {port}\n")

    return new_lines

def save_file(file_path, lines):
    with open(file_path, "w") as file:
        file.writelines(lines)

def update_config():
    config_lines = load_config(CONFIG_FILE)
    updated_lines = modify_config(config_lines, PROXIES)
    save_file(CONFIG_FILE, updated_lines)
    print(Fore.GREEN + f"✅ ProxyChains configuration updated at {CONFIG_FILE} with {len(PROXIES)} proxies." + Fore.RESET)

def check_required_packages():
    clear_terminal()
    print(Fore.YELLOW + "Checking required packages..." + Fore.RESET)
    sleep(1)
    packages = ["proxychains4", "tor"]
    missing_packages = []

    for package in packages:
        if shutil.which(package) is None:
            print(Fore.RED + f"Error! {package} is not installed." + Fore.RESET)
            missing_packages.append(package)

    if missing_packages:
        sys.exit(Fore.RED + "Still error? Please run ->\nsudo apt install proxychains4 && sudo apt install tor: " + ", ".join(missing_packages) + Fore.RESET)

def main():
    check_root()
    check_required_packages()
    update_config()

if __name__ == "__main__":
    main()
