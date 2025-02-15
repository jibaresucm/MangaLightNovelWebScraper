import threading
import queue
import requests

q = queue.Queue()
valid_proxies = []

with open("proxies.txt", "r") as file:
    proxies = file.read().split('\n')
    for p in proxies:
        q.put(p)

def checkProxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            response = requests.get("http://ipinfo.io/json", 
            proxies={
                "http": proxy,
                "https": proxy
            })
        except:
            print("error")
            continue

        if response.status_code == 200:
            print(proxy)

checkProxies()

for i in range(40):
    threading.Thread(target=checkProxies).start()