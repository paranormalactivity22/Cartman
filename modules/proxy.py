import random
import requests

"""
Manage to enter any malicious website using a proxy.
"""

class ProxyManager():
    def __init__(self):
        self.proxies = []
        self.protocol = "http"
        self.timeout = 1000 # a second

    def checkProxy(self, proxy: str) -> None:
        if not proxy in self.proxies and proxy != "":
            info = {
                "http"  : f'{self.protocol}://'+proxy,
                "https"  : f'{self.protocol}://'+proxy,
            }
            try:
                obj = requests.get("https://api.ipify.org", proxies=info, timeout=1)
                port = proxy.split(":")[1]
                if obj.status_code == 200 and port == "80":
                    self.proxies.append(proxy)
                    return True
                else:
                    return False
            except:
                return False
                
    def getProxy(self) -> None:
        x = requests.get(f'https://api.proxyscrape.com/v2/?request=getproxies&protocol={self.protocol}&timeout={self.timeout}&country=all', allow_redirects=True)
        proxies = x.text.split('\n')
        r2 = input(f"[#] Received total {len(proxies)} proxies. Do you wish to check everything or skip on first working proxy? [Y/N] -> ")
        found = False
        
        if r2 == "Y":
            r2 = True
        else:
            r2 = False
        
        for y in range(0, len(proxies)):
            proxies[y] = proxies[y].split('\r')[0]

        for proxy in proxies:
            if not r2:
                if self.checkProxy(proxy):
                    found = True
                    break
            else:
                status = self.checkProxy(proxy)
                if status:
                    found = True
                print(f"[{'!' if status == False else '+'}] The proxy {proxy} is {'not working' if status == False else 'working'}.")
                
        if r2:
            print(f"[#] Check done. Found {len(self.proxies)} total proxies.\n")
            
        if not found or len(self.proxies) == 0:
            print(f"[!] No Proxies found, defaulting to external IP Address.\n")
            
    def getProxyLen(self) -> int:
        return len(self.proxies)
        
    def getRandomProxy(self) -> str:
        return random.choice(self.proxies)
        
    def removeProxy(self, _proxy) -> None:
        self.proxies.remove(_proxy)