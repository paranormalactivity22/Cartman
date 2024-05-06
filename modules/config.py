import configparser

class Config():
    def __init__(self):
        self.config =  configparser.ConfigParser()
        self.config.read("./database/config.ini")
        
    def getConfigCategory(self, category, setting):
        return self.config.get(category, setting)