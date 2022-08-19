#!/usr/bin/python
import requests
import os

def heroku_token(oldtoken):
    url = 'https://api.heroku.com/oauth/authorizations'
    headers = {
        'Accept': 'application/vnd.heroku+json; version=3',
        'Authorization': 'Bearer '+oldtoken,
    }

    data = {
        "description": "Long-lived user authorization",
        "expires_in": None,
        "scope": [
            "global"
        ]
    }
    r = requests.post(url, json=data, headers=headers)

    token = r.json()['access_token']['token']
    return token

pwd = os.popen('pwd').read()
pwd = pwd.strip()
netrc_path = pwd+'/.netrc'
print(netrc_path)
with open(netrc_path, 'r') as f:
    netrc = f.readlines()




old_token = None
for x in netrc:
    if "password" in x:
        otoken = x.split()[-1]
        old_token = otoken

token = heroku_token(oldtoken=old_token)


new_netrc = []
for x in netrc:
    #print(x)
    if "password" in x:
        p = x.split(' ')[:-1]
        pjoin = " ".join(p)
        line = pjoin + ' ' + token + '\n'
        # print(line)
        new_netrc.append(line)
    else:
        # print(x)
        new_netrc.append(x)



os.remove(netrc_path)

for x in new_netrc:
    with open(netrc_path, 'a') as r:
        r.write(x)

username = pwd.split('/')[-1]
os.system("chown -R "+username+":"+username+" "+netrc_path)
print("Done .. ")