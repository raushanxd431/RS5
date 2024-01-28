@@ -1,347 +1 @@
import os
import time
import requests
from platform import system
import logging
from datetime import datetime
import socket
from time import sleep
from bs4 import BeautifulSoup
import pytz
import uuid


API_VERSION = 'v15.0'

HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

brown_text = "\033[0;33m"
yellow_text = "\033[1;33m"
red_text = "\033[1;31m"
green_text = "\033[1;32m"
cyan_text = "\033[1;36m"
blue_text = "\033[1;34m"
magenta_text = "\033[1;35m"
pink_text = "\033[1;38;5;206m"  # Pink
purple_text = "\033[1;38;5;90m"  # Purple
golden_text = "\033[1;38;5;178m"  # Golden
teal_text = "\033[1;38;5;30m"  # Teal
orange_text = "\033[1;38;5;208m"  # Orange
midnight_blue_text = "\033[1;38;5;17m"  # Midnight Blue
khaki_text = "\033[1;38;5;185m"  # Khaki
coral_text = "\033[1;38;5;209m"  # Coral
reset_text = "\033[0m"

additional_logo = f"""
{blue_text}                   ⢀⣀⣀⣀⣀⣀⡀⢀⣀⣀⡀                 
             ⣠⣤⣶⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀              
         ⣀⣴⣶⣶⡜⢿⣿⣿⣿⢿⣿⣿⣿⣧⠘⢿⢿⣿⣿⣿⣿⣿⣿⣿⣶⣄⡀          
      ⢀⣤⣾⣿⣿⣿⣿⣿⣦⠙⠿⣿⡞⡏⣿⡿⣿⡄⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤       
    ⢀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀ ⣡⣤⡘  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢉⣹⣿⡀      
  ⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣷⢰⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠉⣽⣿⣿⣿⣷⣄     
⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡏⠁  ⠋⢛⣿⣿⣿⣿⣧⡄   
⠸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢁⣤⣿⣷⣦⣄ ⠚⣿⣿⣿⣿⣿⣿⡆  
⢀⠰⢿⠧ ⢻⣿⣿⣿⣿⡿⠋      ⠘⠟⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣄⢘⣿⣿⣿⣿⣿⣿⡀ 
⠸⣿⢿⣷⣤⣿⣿⣿⡟⠉           ⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣿⣿⣿⡿⠁ 
 ⢸⣷⣶⣾⣿⣿⣿                ⠛⠿⣿⣿⣿⣿⣿⣿⠛⠉   ⠈⢻⣿⣿⣿⣿⠁  
 ⠸⣿⣿⣿⣿⣿⣇                 ⢀⣈⣿⣿⣿⣿⣿⡆     ⢀⣿⣿⣿⣿⠂  
  ⢿⣿⣿⣿⣿⣿                ⣤⣾⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⡀ ⢨⣿⣿⣿⣿⡇  
 ⢠⠞⢻⣿⣿⣿⣿⡷               ⠐⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠉ ⠺⣿⣿⣿⣯⠴⢶⡄
 ⣾⣶⣶⡿⣿⣿⣿⠁  ⣠⣴⣦⣀     ⢀ ⢸⡄⢰⣿⣿⣿⣿⣿⣿⡿⠛⣿⣿⡿⢿⠆ ⢸⣿⣿⣿⣠⣾⣿
 ⢻⣹⣿⡇⢸⣿⡏  ⠟⠋⠉⠈⢻⣧    ⠈⢷⡀⣿⣾⣿⣿⡟⣻⣿⡟⢁⡾⠋⠁    ⢸⣿⣿⣿⣿⣿⡿
 ⠈⠏⠁⣰⣄⣿⣇   ⣦⣸⣄⣤⣿⣷⣄   ⢸⣷⣿⣿⣿⣿⢣⡿⢫⣶⣟⣥⣄⣀⣤⣴⣶⡄⣸⣿⡏⣾⡇⠘ 
   ⢸⣿⠋⢻⣿   ⠘⠟⢻⣟⠉⠙⠛⢷⣤⣴⣼⣡⣇⣿⣿⣇⣻⡶⠿⡿⠟⣉⡿⣿⣿⣿⣿⣿⣿⣿⠁⢻⣧⡀ 
  ⠰⡎⢻⣦⣈⣗      ⠭⣰⣶⣶⠿⠟⠉⠏⠈⠉⣿⣿⢾⣿⣷⣌⣙⣋⣉⣠⣿⣿⣿⣿⡉⠁⡏⢠⡾⠏⠃ 
   ⢳⡀⢸⠏⠉      ⣀⡈⠉⠁      ⠿⠋ ⢿⣿⣿⣿⣿⣿⣿⣿⠟⠉   ⠡⠿⠁   
    ⠉    ⣶⣶⣶⣶⣾⣿⣿⣦⣤⡄     ⢾⣿⣶⡾⠿⠟⠻⠿⢿⣿⣿⣤⣤⡀        
         ⠻⣿⣿⡿⣿⠛⠉        ⠸⣿⡟⢹⣿⣿⣿⣷⣿⣿⣿⣷⣾⠇        
          ⠈⢿⢿⣶⣤⡀   ⢀⣄⡀  ⣰⠟⢇⣸⣿⠿⣿⣟⡽⣟⣿⡟⠁         
           ⠈⠁⢻⣿⣿⣷⣶⣤⣀⡀⠙⠦⠴⣿⣾⣿⣿⣿⣿⡿⢿⣾⡿⠉⣶          
         ⢷    ⢿⣿⡉⠉⠛⠿⠿⣷⢶⣶⣿⣭⠹⡿⠉  ⢸⣿⠁⢠⠇          
         ⠈⣇   ⠘⣿⣧⣤⣀⡀ ⠁ ⠋   ⡀⢠⣤⣴⣿⠇ ⡿           
          ⠘⣦   ⠘⣿⣤ ⠉⠓⠂  ⠠⠟⠛⢛⠉⣴⣿⡏              
           ⢺⠳⠄  ⠘⢿⣦⡄⡀⢀ ⡀⢠⢀⣼⣼⣿⣿⠃    ⡄          
           ⢸⡆ ⢱⡄ ⠈⢻⣿⣷⣬⣤⣿⣿⣿⣿⣿⢿⠅   ⡞ ⡇          
           ⢸⣿  ⢱⡄  ⠉⠛⢿⣿⣿⣿⣿⠿⠛⠃   ⣾⠁ ⡇          
           ⠈⣿⡄  ⢣⡀ ⢤⣤⣴⣿⣿⣿⣿⣿⣿⣿⡆ ⣸⣿ ⣸⠃          
            ⠈⢷⡄ ⠈⢣⡀ ⠙⠉⠉⠙⣛⠛⢿⣿⣿⠇⢠⣿⡟⣢⠋           
              ⠙⣦⡀⠈⢣⡀  ⢀⣴⣋⣠⣾⣿⡟⣠⣿⡿⣷⠋            
               ⠈⠙⠦⡄⠙⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠁             
                  ⠈⠳⢦⣿⣿⣿⣿⣿⣿⠟⠋⠁                
                     ⣹⣿⣍⡉⠁                    
                    ⣾⣿⣿⣿⣿                     
                    ⠙⢿⣿⣿⠛                     
                     ⠈⠙⠛                      
                       ⣀    
{cyan_text}[*]⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊❊╌──┈⊰᯽⊱❊╌──┈⊰᯽⊱❊╌──┈⊰᯽⊱❊╌──┈⊰᯽⊱❊╌──┈⊰᯽⊱❊╌──┈⊰᯽⊱❊╌──┈⊰᯽⊱\n 
 {purple_text}
 _  .-')                 .-')                
( \( -O )               ( OO ).              
 ,------.  .-'),-----. (_)---\_) ,--. ,--.   
 |   /`. '( OO'  .-.  '/    _ |  |  | |  |   
 |  /  | |/   |  | |  |\  :` `.  |  | | .-') 
{orange_text} |  |_.' |\_) |  |\|  | '..`''.) |  |_|( OO )
 |  .  '.'  \ |  | |  |.-._)   \ |  | | `-' /
 |  |\  \    `'  '-'  '\       /('  '-'(_.-' 
 `--' '--'     `-----'  `-----'   `-----'    
 
                
{reset_text}
"""

logo = f"""
{teal_text}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n{golden_text}[•] :{green_text}OWNER : ANAND MEHRA \n{khaki_text}[•]: {cyan_text} TOOL TYPE : MULTI TOKEN +MULTI GROUP\n{midnight_blue_text}[•] :{pink_text}STATUS : PAID & PREMIUM\n{khaki_text}[•] :{brown_text}OWNER CONTACT: +917643890954
{reset_text}
"""

made_by_text = f"{magenta_text}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n{red_text}[•]{green_text}IT'S FREE FOR ONLY 1 DAY{reset_text}"

def main_apv():
    global key1
    os.system('clear')
    ak = "L3G3ND_M3HR9"
    print(f"{purple_text}⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊❊╌──┈⊰᯽⊱")
    Name = input(f"{cyan_text}Enter Your Name :")

    # Initialize key1
    key1 = "v2VJsp6BjBBae102yKAdEnqIkVVy55CrcwN6ZlxDvBEtoPYkoAfzgxVxKBGE8qSwKN2xg2nr3thmWNvCu1xT5tDGFWRa0gnxQcUT8vevXaZ4bi"

    try:
        key1 = open('/data/data/com.termux/files/usr/bin/.MEHRA-cov', 'r').read()
    except FileNotFoundError:
        print(logo)
        print(f"{magenta_text}✶⊶⊷⊶⊷⊷⊶❍⊶⊷⊶⊷✶⊷✶⊶⊶⊷✶")
        print(f"{red_text}*{reset_text}Your Token Is Not Approved Already")
        print(f"{blue_text}༒━━━━°❀•°:🎀[$]🎀:°•❀°━━━━༒")
        print(f"{golden_text}[$]THIS IS PAID TOOL BRO{reset_text}")
        uid = uuid.uuid4().hex[:10].upper()
        print(f"{red_text}[•]{golden_text} :{Name}THIS IS YOUR KEY BRO :{ak}{key1}{reset_text}")

        with open('/data/data/com.termux/files/usr/bin/.MEHRA-cov', 'w'):

            pass
        print("\nCopy the key and send it for approval.\n")
        sleep(6)
        os.system("xdg-open https://wa.me/+917643890954")

    try:
        r1 = requests.get("https://raw.githubusercontent.com/aaanandsir/MEHRA_KING/main/Aproval.txt").text
        if key1 not in r1:
            print(logo)
            print(f"{magenta_text}✘▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬⌧")
            print(f"[{purple_text}*{reset_text}]{red_text} Your Token is not approved")
            print(f"{khaki_text}⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊⊰᯽⊱┈──╌❊")
            print(f"{green_text}[☞]{cyan_text}{Name} THIS IS YOUR KEY BRO: {ak}{key1}")
            print(f"{orange_text}⊰᯽]|•--------------------------------------------------------------------------»")
            print(f"{cyan_text}Copy the key and send it for approval.")
            print(f"{brown_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"{cyan_text}༒━━━━━━━━━━━°❀•°:🎀{golden_text}[$]{cyan_text}🎀:°•❀°━━━━━━━━━━༒")
            print(f"{golden_text}THIS TOOL IS PAID BRO :")

            sleep(3.5)
            tks = f'Dear%20Admin,%20Please%20Approved%20My%20Key%20To%20Premium%20%20Thanks%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20My%20Email%20:%20' + '' + f'%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20My%20Name%20:%20' + '' + f'%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20My%20%20Key%20%20:%20' + ak + key1 
            os.system(f'am start https://wa.me/+917643890954?text={tks}')
        else:
            main()
    except requests.exceptions.RequestException as e:
        print(f"Error making a request: {e}")
        exit()

def is_internet_available():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        pass
    return False

def get_user_name(access_token):
    try:
        response = requests.get(f'https://graph.facebook.com/{API_VERSION}/me', params={'access_token': access_token})
        response.raise_for_status()
        user_data = response.json()
        return user_data.get('name', 'Unknown User')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching user name: {e}")
        return 'Unknown User'

def send_message(api_url, access_token, thread_id, message):
    parameters = {'access_token': access_token, 'message': message}
    try:
        response = requests.post(api_url, data=parameters, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending message: {e}")
        return None

def get_colored_input(prompt, color_code):
    user_input = input(f"{color_code}{prompt}{reset_text}")
    return user_input

def print_brown(text):
    print(f"{brown_text}{text}{reset_text}")

def print_yellow(text):
    print(f"{yellow_text}{text}{reset_text}")

def print_red(text):
    print(f"{red_text}{text}{reset_text}")

def print_green(text):
    print(f"{green_text}{text}{reset_text}")

def print_cyan(text):
    print(f"{cyan_text}{text}{reset_text}")

def print_blue(text):
    print(f"{blue_text}{text}{reset_text}")

def print_magenta(text):
    print(f"{magenta_text}{text}{reset_text}")

def print_pink(text):
    print(f"{pink_text}{text}{reset_text}")

def print_purple(text):
    print(f"{purple_text}{text}{reset_text}")

def print_golden(text):
    print(f"{golden_text}{text}{reset_text}")

def print_teal(text):
    print(f"{teal_text}{text}{reset_text}")

def print_orange(text):
    print(f"{orange_text}{text}{reset_text}")

def print_midnight_blue(text):
    print(f"{midnight_blue_text}{text}{reset_text}")

def print_khaki(text):
    print(f"{khaki_text}{text}{reset_text}")

def print_coral(text):
    print(f"{coral_text}{text}{reset_text}")

def get_access_tokens():
    choice = input(f"{red_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{pink_text}Press 1 to input access tokens from a file, Press 2 for manual input: ")

    if choice == '1':
        try:
            file_path = input(f"{purple_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{magenta_text}Enter the file path containing access tokens: ")
            with open(file_path, 'r') as file:
                access_tokens = file.read().splitlines()
        except FileNotFoundError:
            print_red(f"File not found. Please provide a valid file path.")
            exit()
    elif choice == '2':
        num_tokens = int(input(f"{golden_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{purple_text}Enter the number of access tokens: "))
        access_tokens = [input(f"{green_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{golden_text}Enter access token {i + 1}: ") for i in range(num_tokens)]
    else:
        print_red(f"Invalid choice. Exiting.")
        exit()

    return access_tokens

def get_thread_ids():
    choice = input(f"{cyan_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{blue_text}Press 1 to input thread IDs from a file, Press 2 for manual input: ")

    if choice == '1':
        try:
            file_path = input(f"{brown_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{coral_text}Enter the file path containing thread IDs: ")
            with open(file_path, 'r') as file:
                thread_ids = file.read().splitlines()
        except FileNotFoundError:
            print_red(f"File not found. Please provide a valid file path.")
            exit()
    elif choice == '2':
        num_threads = int(input(f"{pink_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{khaki_text}Enter the number of thread IDs: "))
        thread_ids = [input(f"{teal_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{cyan_text}Enter thread ID {i + 1}: ") for i in range(num_threads)]
    else:
        print_red(f"Invalid choice. Exiting.")
        exit()

    return thread_ids

def get_access_tokens_and_thread_ids():
    access_tokens = get_access_tokens()
    thread_ids = get_thread_ids()
    return access_tokens, thread_ids

def round_robin_send_messages(access_tokens, thread_ids, messages, mn, sleep_time):
    ist = pytz.timezone('Asia/Kolkata')

    num_tokens = len(access_tokens)
    num_threads = len(thread_ids)
    num_messages = len(messages)
    current_message_index = 0

    while True:
        for j in range(num_tokens):
            access_token = access_tokens[j]
            user_name = get_user_name(access_token)

            for k in range(num_threads):
                thread_id = thread_ids[k]
                api_url = f'https://graph.facebook.com/{API_VERSION}/t_{thread_id}/'
                current_message = messages[current_message_index]
                message = f'{mn} {current_message}'

                response = send_message(api_url, access_token, thread_id, message)
                current_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S %Z")

                if response and response.status_code == 200:
                    print_green(f"{purple_text}[🍼]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{green_text}[*]{user_name} : Sir Message sent to thread {thread_id}: ({mn}) {message} - Time: {current_time}\n{blue_text}••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
                else:
                    print_red(f"Failed to send message to {user_name} in thread {thread_id}: {message}")

                sleep(sleep_time)

        current_message_index = (current_message_index + 1) % num_messages

def main():
    print(additional_logo)
    print(made_by_text)
    logging.basicConfig(level=logging.INFO)

    while True:
        try:
            while not is_internet_available():
                print_red("Internet connection not available. Waiting for connection...")
                sleep(10)

            access_tokens, thread_ids = get_access_tokens_and_thread_ids()
            mn_color = input(f"{blue_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{red_text}Enter your haters name: ")
            txt_file_path = input(f"{green_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{golden_text}Enter the path to your message file (txt): ")

            try:
                with open(txt_file_path, 'r') as file:
                    messages = file.read().splitlines()
            except FileNotFoundError:
                print_red("File not found. Please provide a valid file path.")
                exit()

            sleep_time = float(input(f"{orange_text}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{teal_text}Enter the time delay between messages (in seconds): "))

            round_robin_send_messages(access_tokens, thread_ids, messages, mn_color, sleep_time)

        except KeyboardInterrupt:
            logging.info("Script terminated by user.")

if __name__ == "__main__":
    main_apv()