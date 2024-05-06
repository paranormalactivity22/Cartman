"""
Save the received information in a file.
"""

class FileManager():
    def __init__(self, info : dict):
        self.info = info
    
    def saveFile(self) -> None:
        with open(self.info["hash"] + ".txt", "w") as F:
            F.write(f"Link -> <{self.info['url']}>\n")
            
            if "source_code" in self.info:
                F.write(f"Source Code -> <{self.info['source_code']}>\n")
                
            F.write(f"Scam Type -> {self.info['type']}\n")
            F.write(f"ASN -> {self.info['ASN']}\n")
            
            if self.info['type'] == "Popup":
                F.write(f"Phone -> {self.info['telephone']}\n")
                F.write(f"Country -> {self.info['phone_country']}\n")
                
            F.write(f"PhishTarget (Experimental) -> {self.info['phish_target']}\n")
                
            F.write(f"Hash -> {self.info['hash']}\n")
            F.write(f"Google Safebrowsing -> {self.info['google_safebrowsing']}\n")
            F.write(f"Abuse Emails -> {self.info['abuse-email']}\n")
            F.write(f"VT Info -> {self.info["vt_res"]}\n")
            F.write(f"Screenshot:\n")
            
            F.write(f"Additional Information:\n")
            if "google_tag" in self.info:
                F.write(f"Google Tag ID -> {self.info['google_tag']}\n")
                
            # Additional information
                
            if "live_chat_script" in self.info:
                F.write(f"[!] Found live chat script -> {self.info['live_chat_script']}\n")
                
            if "obfuscated_script" in self.info:
                F.write(f"[!] Obfuscated script was detected.\n")
                
            if "browser_crash_tool" in self.info:
                F.write(f"[!] Browser crash tool was found.\n")
                
            if "ip_logger_detected" in self.info:
                F.write(f"[!] Found an ip logger.\n")