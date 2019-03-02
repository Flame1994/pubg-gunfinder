import numpy as np
import cv2
from PIL import ImageGrab as ig
import time
import pyautogui
import pytesseract
import difflib
import json

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
last_time = time.time()
screen_width = pyautogui.size().width
screen_height = pyautogui.size().height

key_words = ['killed', 'with']

data = {
    "users": []
}
death_words = ['headshot', 'Playzone']
gun_list = ['AKM','AUG A3','Beryl M762','Groza','M16A4','M416','Mk47 Mutant','QBZ95','SCAR-L','G36C', # Assault Rifles
            'Mini 14','Mk14 EBR','QBU','SKS','SLR','VSS', # DMRs
            'Winchester', # Rifles
            'DP-28','M249', # Light Machine Guns
            'Crossbow', # Miscellaneous
            'S12K','S1897','S686','Sawed-off', # Shotguns
            'AWM','Kar98','M24', # Sniper Rifles
            'Micro UZI','Tommy Gun','UMP9','Vector','PP-19 Bizon‎‎'] # Submachine Guns‎‎‎

handgun_list = ['Flare Gun','P18C','P1911','P92','R1895','R45','Skorpion']
melee_list = ['Crowbar','Machete','Pan','Sickle']
throwable_list = ['Frag Grenade','Molotov Cocktail','Smoke Grenade','Stun Grenade']

def LD(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
       
    res = min([LD(s[:-1], t)+1,
               LD(s, t[:-1])+1, 
               LD(s[:-1], t[:-1]) + cost])
    return res


def user_exists(user):
    print('--------------------------------- CHECK USER EXISTS ---------------------------------')
    print('Checking user ' + user)    
    has_player = False
    for player in data['users']:
        if LD(user, player['name']) < 2:
            has_player = True
            break

    print(has_player)
    return has_player

def weapon_exists(weapon):
    has_weapon = False

    return has_weapon

def get_user_from_list(name):
    print('--------------------------------- GET USER FROM LIST ---------------------------------')
    for n in data['users']:
        # if new name is close enough to previous name, update and return
        if LD(name, n['name']) < 2:
            n['name'] = name
            return n
            

while(True):
    screen = ig.grab(bbox=(1200,70,1920,300))
    #print('Loop took {} seconds',format(time.time()-last_time))
    gray = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)    
    # blurred = cv2.blur(gray, (3,3))
    cv2.imshow("test", gray)
    output = pytesseract.image_to_string(gray, lang='eng')
    if len(output):
        # print(output)
        # print('')
        text_chunk = output.split('\n')
        for text_line in text_chunk:
            words = text_line.split(' ')
            print(words)
            for index, word in enumerate(words):
                print(difflib.get_close_matches(word, key_words))
                if 'killed' in difflib.get_close_matches(word, key_words):
                    # check if user already in list
                    # x killed y with z
                    if index > 0 and user_exists(words[index - 1]) == False:
                        # if not in list - add a new user with all their info
                        # TODO: Check headshot killfeed
                        weapon = ''
                        if len(words) >= index + 3 and 'with' in difflib.get_close_matches(words[index + 2], key_words):
                            weapon = words[index + 3]

                        print('----------------------------------------WEAPON CHECK ')
                        print(difflib.get_close_matches(weapon, gun_list))
                        if weapon != '':
                            possible_weapons = difflib.get_close_matches(weapon, gun_list)
                            if len(possible_weapons) > 0:
                                weapon = possible_weapons[0]
                        user = {
                            'name': words[index - 1],
                            'weapon_1': weapon,
                            'weapon_2': '',
                            'handgun': '',
                            'kills': 1,
                            'temp_weapon': ''
                        }
                        data['users'].append(user)
                        print(words)
                    else:
                        # Check the info of the words and see if guns have updated
                        print('User exists')
                        weapon = ''
                        if len(words) >= index + 3 and 'with' in difflib.get_close_matches(words[index + 2], key_words):
                            weapon = words[index + 3]
                        if weapon != '':
                            possible_weapons = difflib.get_close_matches(weapon, gun_list)
                            if len(possible_weapons) > 0:
                                weapon = possible_weapons[0]

                        user = get_user_from_list(words[index - 1])
                        if user != None:
                            if user['weapon_1'] != weapon and user['weapon_2'] != weapon:
                                if user['weapon_2'] == '':
                                    user['weapon_2'] = weapon
                                else:
                                    if weapon == user['temp_weapon']:
                                        user['weapon_2'] = user['temp_weapon']
                                        user['temp_weapon'] = ''
                                    else:
                                        user['temp_weapon'] = user['weapon_1']
                                        user['weapon_1'] = weapon
                            
                            print(get_user_from_list(words[index - 1]))

        
        print('users:')
        print(data['users'])
        # print(output)
    last_time = time.time()
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break




# players [ player { name, primary_gun, secondary_gun, kills}]