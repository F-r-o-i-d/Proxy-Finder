import random
import requests
import time
import socket
import os, threading

def GenerateRandomIp():
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return ip

#ip echo api
apis = []
apis.append("http://ip.chinaz.com/getip.aspx")
apis.append("http://ip.taobao.com/service/getIpInfo.php?ip=myip")
apis.append("http://ip-api.com/json/")
apis.append("http://ip.ws.126.net/ipquery")
apis.append("http://ip.360.cn/IPShare/info")
apis.append("http://ip138.com/ips1388.asp?ip=")
apis.append("http://ip.taobao.com/service/getIpInfo.php?ip=")
apis.append("http://www.net.cn/static/customercare/yourip.asp")
apis.append("http://ip.chinaz.com/getip.aspx")
apis.append("http://pv.sohu.com/cityjson?ie=utf-8")


def CheckProxy(proxy, timeout=5):
    try:
        proxy = {'http': proxy}
        r = requests.get(random.choice(apis), proxies=proxy, timeout=timeout)
        if r.status_code == 200 and proxy.split(':')[0] in r.text:
            return True
        else:
            return False
    except:
        return False

def check_if_alive(proxy):
    sock = socket.socket()
    sock.settimeout(5)
    try:
        sock.connect((proxy.split(':')[0], int(proxy.split(':')[1])))
        return True
    except:
        return False

def sendwebhookMessage(message):
    webhook_url = "https://discord.com/api/webhooks/1063023261086126130/7aw6bWH5mGfXwIGpyYSYBGDMwcST9YaG_VB7aXwJTAcX-oLL2qhnymGMaEGoqv3nfVvT"
    data = {"content": message}
    result = requests.post(webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        pass

def GetProxy():
    while True:
        common_ports = [8080, 3128, 1080, 6588, 8000, 8888, 9000, 10000]
        proxy = GenerateRandomIp() + ':' + str(random.choice(common_ports))
        is_alive = check_if_alive(proxy)
        if is_alive:
            if CheckProxy(proxy):
                sendwebhookMessage(proxy)
                print("+"  +proxy)
            else:
                print("/" + proxy)
        else:
            print("-" + proxy)

if __name__ == '__main__':
    for i in range(10):
        t = threading.Thread(target=GetProxy)
        t.start()
    while(1):
        input()