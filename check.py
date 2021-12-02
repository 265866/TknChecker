import re
import requests
from colorama import Fore, init
import os
from datetime import datetime

init(convert=True, autoreset=True)
green, red, white, cyan, yellow, reset = (
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTRED_EX,
    Fore.WHITE,
    Fore.LIGHTCYAN_EX,
    Fore.YELLOW,
    Fore.RESET,
)
pref = f"{white}[{red}>{white}]{reset} "

tokens = []

fullyverified = []
emailverified = []
unverified = []
invalid = []
withservers = []
hasbilling = []
hasnitro = []
specialflag = []
nitroandbilling = []
withoutservers = []
spammer = []

try:
    for line in [x.strip() for x in open("input.txt", errors="ignore").readlines() if x.strip()]:
        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
            for token in re.findall(regex, line):
                tokens.append(token)
except:
    print("No input.txt file detected!")
tokens = list(dict.fromkeys(tokens))

for token in tokens:
    try:
        json = requests.get("https://discordapp.com/api/v9/users/@me?verified", headers={"authorization": token})           
        if json.status_code == 200:
            json_response = json.json()
        else:
            pass

        if type(json_response['phone']) == str and type(json_response['email']) == str:
            veritype = "Fully Verified"
            fullyverified.append(token)

        if json_response['phone'] == None and type(json_response['email']) == str:
            veritype = "Email Verified"
            emailverified.append(token)

        if json_response['phone'] == None and json_response['email'] == None:
            veritype = "Unverified"
            unverified.append(token)

        try:
            if json_response['premium_type'] == 1:
                nitrotype = "Nitro Classic"
                hasnitro.append(token)
            if json_response['premium_type'] == 2:
                nitrotype = "Nitro Boost"
                hasnitro.append(token)
        except:
            nitrotype = "No Nitro"

        if json_response['flags'] == 1:
            Flag = "Flag = Discord Employee"
            specialflag.append(token)
        elif json_response['flags'] == 2:
            Flag = "Flag = Discord Partner"
            specialflag.append(token)
        elif json_response['flags'] == 4:
            Flag = "Flag = HypeSquad Events member"
            specialflag.append(token)
        elif json_response['flags'] == 8:
            Flag = "Flag = Bug Hunter (lvl 1)"
            specialflag.append(token)
        elif json_response['flags'] == 512:
            Flag = "Flag = Early Supporter"
            specialflag.append(token)
        elif json_response['flags'] == 16384:
            Flag = "Flag = Bug Hunter (lvl 2)"
            specialflag.append(token)
        elif json_response['flags'] == 131072:
            Flag = "Flag = Bot Developer"
            specialflag.append(token)
        elif json_response['flags'] == 262144:
            Flag = "Flag = Bot Developer"
            specialflag.append(token)
        elif json_response['flags'] == 1048576:
            Flag = "Flag = Spammer"
            spammer.append(token)
        elif json_response['flags'] == 64 or json_response['flags'] == 128 or json_response['flags'] == 256:
            Flag = "Flag = Regular Hypesquad"
        else:
            Flag = "Flag = No Flags"

        if json_response['mfa_enabled'] == True:
            twof = "2FA Enabled"
        else:
            twof = "2FA Disabled"

        json = requests.get("https://discordapp.com/api/v9/users/@me/billing/payment-sources", headers={"authorization": token})           
        if json.status_code == 200:
            json_response = json.json()
        else:
            pass
        if not json_response:
            paymentMethod = "No Payment Method"
        else:
            paymentMethod = "Payment Method"
            hasbilling.append(token)

        json = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={"authorization": token})
        if json.status_code == 200:
            json_response = json.json()
        else:
            pass
        friends = "Friends: " + str(len(json_response))

        json = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={"authorization": token})
        if json.status_code == 200:
            json_response = json.json()
        else:
            pass
        if len(json_response) >= 90:
            withservers.append(token)
        elif len(json_response) < 90:
            withoutservers.append(token)
        guilds = "Guilds: " + str(len(json_response))
        


        print(f"[{green}+{reset}] {token} | {veritype} | {nitrotype} | {twof} | {Flag} | {paymentMethod} | {friends} | {guilds}")

        if nitrotype == "Nitro Classic" or nitrotype == "Nitro Boost":
            if paymentMethod == "Payment Method":
                nitroandbilling.append(token)

    except:
        print(f"[{red}-{reset}] {token} | Invalid Token!")
        invalid.append(token)

e = datetime.now()
current_date = e.strftime("%Y-%m-%d-%H-%M-%S")
if not os.path.exists(f"Results/{current_date}/"):
    os.makedirs(f"Results/{current_date}/")
with open(f"Results/{current_date}/fullyverified.txt", 'w') as f:
    for i in fullyverified:
        f.write(i + "\n")
with open(f"Results/{current_date}/emailverified.txt", 'w') as f:
    for i in emailverified:
        f.write(i + "\n")
with open(f"Results/{current_date}/unverified.txt", 'w') as f:
    for i in unverified:
        f.write(i + "\n")
with open(f"Results/{current_date}/invalid.txt", 'w') as f:
    for i in invalid:
        f.write(i + "\n")
with open(f"Results/{current_date}/hasservers.txt", 'w') as f:
    for i in withservers:
        f.write(i + "\n")
with open(f"Results/{current_date}/hasbilling.txt", 'w') as f:
    for i in hasbilling:
        f.write(i + "\n")
with open(f"Results/{current_date}/hasnitro.txt", 'w') as f:
    for i in hasnitro:
        f.write(i + "\n")
with open(f"Results/{current_date}/nitroandbilling.txt", 'w') as f:
    for i in nitroandbilling:
        f.write(i + "\n")
with open(f"Results/{current_date}/specialflag.txt", 'w') as f:
    for i in specialflag:
        f.write(i + "\n")
with open(f"Results/{current_date}/putinjoinify.txt", 'w') as f:
    for i in withoutservers:
        f.write(i + "\n")
with open(f"Results/{current_date}/spammer.txt", 'w') as f:
    for i in spammer:
        f.write(i + "\n")

os.system('cls||clear')
print(pref + f"[{cyan}DONE{reset}]")
print(pref + f"Fully Verified: {cyan}{str(len(fullyverified))}{reset}")
print(pref + f"Email Verified: {cyan}{str(len(emailverified))}{reset}")
print(pref + f"Unverified: {cyan}{str(len(unverified))}{reset}")
print(pref + f"Invalid: {cyan}{str(len(invalid))}{reset}")
print(pref + f"Has 90+ Servers: {cyan}{str(len(withservers))}{reset}")
print(pref + f"Doesn't have 90+ Servers: {cyan}{str(len(withoutservers))}{reset}")
print(pref + f"Has Billing Info: {cyan}{str(len(hasbilling))}{reset}")
print(pref + f"Has Nitro: {cyan}{str(len(hasnitro))}{reset}")
print(pref + f"Has Billing Info and Nitro: {cyan}{str(len(nitroandbilling))}{reset}")
print(pref + f"Has Special Flag(s): {cyan}{str(len(specialflag))}{reset}")
print(pref + f"Flagged As Spammmer: {cyan}{str(len(spammer))}{reset}")
print(pref + f"Results Saved To: Results/{current_date}/")
input("Press Enter to exit...")
