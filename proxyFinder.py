import random
import requests
import time
import socket, base64
import os, threading, sys

def GenerateRandomIp(baseIP):
    baseIPlen = len(baseIP.split("."))
    
    ip = ""
    for i in range(4 - baseIPlen):
        ip += str(random.randint(0, 255)) + "."
    
    ip = ip[:-1]
    ip = baseIP + "." + ip
    return ip

#ip echo api
apis = []
apis.append("http://ip-api.com/json/")
apis.append("https://user.ip138.com/ip/")
apis.append("http://www.net.cn/static/customercare/yourip.asp")
apis.append("http://ip.chinaz.com/getip.aspx")
apis.append("https://ipecho.net/extra")
apis.append("https://api.ipify.org?format=json")
apis.append("https://api-ipv4.ip.sb/ip")
apis.append("https://ip4.seeip.org")
apis.append("http://api.ipaddress.com/myip?format=json&callback=myCallback")
try:
    isDebug = sys.argv[1] 
    isDebug = True
except:
    isDebug = False

def CheckProxy(proxy, timeout=5):
    try:
        proxy = {'https': proxy, 'http': proxy}
        r = requests.get(random.choice(apis), proxies=proxy, timeout=timeout)
        if r.status_code == 200:
            if proxy.split(':')[0] in r.text:
                return 2
            return 1
        else:
            return 0
    except:
        return 0

def check_if_alive(proxy):
    sock = socket.socket()
    sock.settimeout(5)
    try:
        sock.connect((proxy.split(':')[0], int(proxy.split(':')[1])))
        return True
    except:
        return False

def sendwebhookMessage(message):
    webhook_url = base64.b64decode("aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTA2MzAyMzI2MTA4NjEyNjEzMC83YXc2YldINW1HZlh3SUdweVlTWUJHRE13Y1NUOVlhR19WQjdhWHdKVEFjWC1vTEwycWhueW1HTWFFR29xdjNuZlZ2VA==")
    data = {"content": message}
    result = requests.post(webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        pass
totalProxies = 0
def GetProxy():
    while True:
        baseIP = ["23.229.80", "51", "163.116.248", "51.210"]
        common_ports = [8080, 3128, 1080, 6588, 8081, 8081, 8090, 13128]
        ip = GenerateRandomIp(random.choice(baseIP))
        print(ip)
        proxys = [ip + ":" + str(port) for port in common_ports]
        for proxy in proxys:
            is_alive = check_if_alive(proxy)
            if is_alive:
                if CheckProxy(proxy) == 1:
                    sendwebhookMessage(proxy + "Transparent Proxy")
                    print("+"  +proxy)
                elif CheckProxy(proxy) == 2:
                    sendwebhookMessage(proxy + "Anonymous / Elite Proxy")
                    print("+" + proxy)
                elif isDebug:
                    print("/" + proxy)
            elif isDebug:
                print("-" + proxy)

if __name__ == '__main__':
    sendwebhookMessage("Proxy Finder Started")

    for i in range(100):
        t = threading.Thread(target=GetProxy)
        t.start()
    while(1):
        input()
