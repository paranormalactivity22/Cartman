import pysafebrowsing
import requests
import re
import socket
import zlib
from modules.formatter import Helper
from ipwhois import IPWhois

class Web():
    def __init__(self, _web, _proxy, _type) -> None:
        # Objects
        self.formatter = Helper()
        self.proxy = _proxy
        self._type = _type

        # Strings
        self.website = self.formatter._formatWebsite(_web)

    def __hash__(self) -> int:
        return hash(self.website)
    
    def getResponse(self, pagesrc : bool = False) -> str:
        page_src = ""

        try:
            if self.proxy.getProxyLen() > 0:
                __proxy = self.proxy.getRandomProxy()
            
                info = {
                    "http"  : f'{self.proxy.protocol}://'+__proxy,
                    "https" : f'{self.proxy.protocol}://'+__proxy
                }
            
                obj = requests.get(self.website, proxies=info, allow_redirects=True)
                if obj.status_code != 200:
                    print(f"[!] The proxy {__proxy} does not work anymore.")
                    self.proxy.removeProxy(__proxy)
                    return getResponse(pagesrc)
            else:
                print(f"[!] Using default IP address.")
                obj = requests.get(self.website, allow_redirects=True)            
            
            page_src = obj.text

        except requests.exceptions.RequestException as e:
            page_src = f"Error -> {e}"

        return page_src
    
    def findPhoneNumber(self, pagesource : str) -> dict:
        found_phones = list(dict.fromkeys(re.findall(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', pagesource)))
        
        format_phones = []
        for phone in found_phones:
            phone = phone.replace(' ', '')
            if not phone in ["9999999999"] and len(phone) >= 10 and len(phone) <= 20:
                if not '.' in phone:
                    format_phones.append(self.formatter._formatPhoneNumber(phone))

        if len(format_phones) == 0:
            format_phones.append("N/A")

        return format_phones
    
    def getPageInfo(self) -> dict:
        whois = self.getWhoisInfo(self.getWebsiteIP(self.formatter._formatDomain(self.website)))
        typ = "Phishing"
    
        if self._type == True:
            typ = "Popup"
            phones = self.findPhoneNumber(self.getResponse(True))
            print("[#] Received information about the pop up.")
            return {
                    "url" : self.website, 
                    "type": typ,
                    "hash" : str(zlib.crc32(str(self.website).encode())), 
                    "telephone" : phones, 
                    "phone_country" : self.formatter.getPhoneCountry(phones[0]), 
                    "ASN" : f"{str(whois['asn_description']).capitalize()} ({whois['asn']})",
                    "abuse-email": f"{', '.join(whois['nets'][0]['emails'])}",
                    "google_safebrowsing" : self.getSafebrowsingStatus(self.website)
            }
        else:
            print("[#] Received information about the phishing page.")
            return {
                    "url" : self.website, 
                    "type": typ,
                    "hash" : str(zlib.crc32(str(self.website).encode())), 
                    "ASN" : f"{str(whois['asn_description']).capitalize()} ({whois['asn']})",
                    "abuse-email": f"{', '.join(whois['nets'][0]['emails'])}",
                    "google_safebrowsing" : self.getSafebrowsingStatus(self.website)
            }
            
    def getWebsiteIP(self, domain : str) -> str:
        return socket.gethostbyname(domain)
        
    def getWhoisInfo(self, ip : str) -> dict:
        obj = IPWhois(ip)
        return obj.lookup_whois()
        
    def getSafebrowsingStatus(self, web : str) -> bool:
        obj = pysafebrowsing.SafeBrowsing("")
        info = obj.lookup_url(web)
        return info['malicious']