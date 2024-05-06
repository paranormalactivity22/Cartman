import json
import os
from modules.config import Config
from modules.console import DrawConsoleTitle
from modules.file import FileManager
from modules.proxy import ProxyManager
from modules.web import Web
from modules import screenshot
from PyQt5.QtWidgets import QApplication

class Main():
    def __init__(self):
        # Objects
        self.config = Config()
        self.console = DrawConsoleTitle()
        self.proxyman = ProxyManager(self.config)
        
        # List
        self.blockedDomains = []
        
        # Nonetype
        self.web = None
        self.file = None
        self.qApp = None
        
        # String
        self.contains_src = ""
        self.phish_target = ""
        self.use_proxy = ""
        self.typ = "-1"
        self.url = ""

    def init(self):
        self.console.cls()
        self.console.draw()
        self.qApp = QApplication([""])
        self.blockedDomains = json.load(open("./database/blacklist.json"))
        self.use_proxy = input("[?] Do you want to use proxy? [Y/N] -> ")
        if self.use_proxy == "Y":
            self.proxyman.getProxy()
        while 1:
            self.run()
            self.console.cls()
            self.console.draw()
    
    def run(self):
        self.url = input("[?] Website -> ")
        self.typ = input("[?] Is it a pop up? (Leave Y for pop up or N for phishing) -> ")
        self.contains_src = input("[?] Source code URL (Leave empty for not found) -> ")
        if self.typ == "Y":
            self.phish_target = "Tech Support Scam"
        else:
            self.phish_target = input("[?] Specify the phishing target (Leave empty for default) -> ")
            
        if self.url in self.blockedDomains:
            print("The url is safe. You do not need to take any further action.")
            os.system("pause")
            return
        
        self.web = Web(self.url, self.proxyman, self.config, self.typ == "Y")
        info = self.web.getPageInfo()
        screenshot.makeScreenshot(self.qApp, info, self.proxyman)
        info['phish_target'] = self.phish_target if len(self.phish_target) != 0 else "General"
        if self.contains_src: 
            # If source code was found.
            info["source_code"] = self.contains_src
        
        
        self.file = FileManager(info)
        self.file.saveFile()
        self.console.pause()
       
Main().init()


"""
            F.write(f"Additional Information:\n")
            if "google_tag" in self.info:
                F.write(f"Google Tag ID -> {self.info['google_tag']}\n") ########
                
            # Additional information
                
            if "live_chat_script" in self.info:
                F.write(f"[!] Found live chat script -> {self.info['live_chat_script']}\n") ########
                
            if "obfuscated_script" in self.info:
                F.write(f"[!] Obfuscated script was detected.\n") ########
                
            if "browser_crash_tool" in self.info:
                F.write(f"[!] Browser crash tool was found.\n") ########
                
            if "ip_logger_detected" in self.info:
                F.write(f"[!] Found an ip logger.\n") ########
"""