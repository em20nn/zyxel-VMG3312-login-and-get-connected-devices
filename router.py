import requests
import re
import time

def login(username, password):
    session = requests.Session()
    session.get("http://192.168.1.1/login/login-page.cgi")
    data = {"AuthName":username, "AuthPassword":password}
    check=session.post("http://192.168.1.1/login/login-page.cgi", data=data)
    if "The username or password is not correct." in check.text:
        print("\nLogin failed, The username or password is not correct.\n")
        exit()
    else:
        print("\nLogin successfull.\n")
        return session

def get_info(session):
    response=session.get("http://192.168.1.1/pages/connectionStatus/GetNetworkMapInfo.html")
    raw=response.text
    replaced=raw.replace("|", "\n").replace("@", "")
    mac_addresses = re.findall(r'([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})', replaced)
    for mac in mac_addresses:
        a.append(mac[0])
    return session

def logout(session):
    response=session.get("http://192.168.1.1/login/login-logout.cgi")
    if "top.location='/login/login.html'" in session.get("http://192.168.1.1/pages/connectionStatus/GetNetworkMapInfo.html").text:
        print("\nLogout Successfull\n")
    else:
        print("\nLogout Failed\n")

MAC_NAME_MAP = {
    'aa:aa:aa:aa:aa:aa': 'NAME',
}

a=[]
user_key = 'PUSHOVER USER KEY'
api_token = 'PUSHOVER API TOKEN'
pushover_url = 'https://api.pushover.net/1/messages.json'

def send_pushover_notification(message):
    payload = {
        'token': api_token,
        'user': user_key,
        'message': message,
        'title': 'router.py',
        'priority': 0,
    }
    response = requests.post(pushover_url, data=payload)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Error sending notification: {response.status_code} - {response.text}")

def main():
    while True:
        try:
            session=login("USERNAME (admin)","PASSWORD (admin)")
        except Exception as e:
            print(f"ERR WITH LOGIN {e}")
            time.sleep(600)
        for i in range(60):
            b=""
            for i in range(5):
                a=[]
                try:
                    session=get_info(session)
                    for i in a:
                        if i in MAC_NAME_MAP:
                            i = i.replace(i, f"{i} ({MAC_NAME_MAP[i]})\n")
                            b=b+i
                        else:
                            b=b+i+"(UNKNOWN)\n"
                except Exception as e:
                    print(f"ERR WITH GET_INFO {e}")
                    time.sleep(600)
                time.sleep(5)
            try:
                send_pushover_notification("\n".join(sorted(set(b.splitlines()), key=b.splitlines().index)).replace(")", ")\n"))
                time.sleep(600)
            except Exception as e:
                print(f"ERR WITH PUSHOVER {e}")
                time.sleep(600)
        try:
            logout(session)
        except Exception as e:
            print(f"ERR WITH LOGOUT {e}")
            time.sleep(600)

if __name__=='__main__':
    main()