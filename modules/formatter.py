from urllib.parse import urlparse
import re

class Helper(str):
    def __init__(self) -> None:
        pass
        
    def _formatDomain(self, web : str) -> str:
        return urlparse(web).hostname

    def _formatPhoneNumber(self, phone : str) -> str:
        phone = re.sub(r'\D', '', phone)
            
        if (phone[0] == '0' and phone[1] in ['1', '5', '7', '8', '9'] and phone[2] == '0' and len(phone) == 11): # Japan
            return f"+81 {phone[:3]}-{phone[3:7]}-{phone[7:]}"

        elif phone[0:4] == "0101" and len(phone) == 14: # Japan
            return f"+81 {phone[:4]}-{phone[4:7]}-{phone[8:11]}-{phone[11:]}"

        elif phone[0:3] == "020" and len(phone) == 11: # United Kingdom
            phone = phone[1:]
            return f"+44 {phone[:2]} {phone[2:6]} {phone[6:]}"
        
        elif (phone[0] == '1' and len(phone) == 11) or len(phone) == 10: # United States
            phone = phone[1:]
            phone = f"+1 ({phone[:3]}) {phone[3:6]}-{phone[6:]}"
            if phone[4:7] in ["800", "833", "844", "855", "866", "877", "888"]:
                phone = phone + " (Toll-free)"
            return phone
        
        elif phone[0:2] == "49": # Germany
            phone = phone[2:]
            return f"+49 {phone[:4]} {phone[4:]}"
        
        # France
        return phone    

    def _formatWebsite(self, web : str) -> str:
        if web.startswith("http"):
            return web
        
        web = "http://" + web
        return web

    def getPhoneCountry(self, phone : str) -> str:
        if "+1" in phone:
            return "United States (US)"
        
        elif "+81" in phone:
            return "Japan (JP)"
        
        elif "+49" in phone:
            return "Germany (DE)"
        
        elif "+44" in phone:
            return "United Kingdom (UK)"
        
        elif "+33" in phone:
            return "France (FR)"
        
        return "UNKNOWN"