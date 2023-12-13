import json

THEME_OPTIONS = ["darkly", 
                 "flatly", 
                 "journal", 
                 "cosmo",
                 "litera",
                 "lumen",
                 "minty",
                 "pulse",
                 "sandstone",
                 "simplex",
                 "sketchy",]
FONT_OPTIONS = ["Arial", 
                "Calibri", 
                "Cambria", 
                "Comic Sans MS", 
                "Consolas", 
                "Courier New", 
                "Georgia", 
                "Helvetica", 
                "Impact"]
FONT_SIZE_OPTIONS = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22]

class Config():
    def __init__(self, theme="darkly", font="arial", font_size=12):
        self.theme = theme
        self.font = font
        self.font_size = font_size
    def getTheme(self):
        return self.theme
    def getFont(self):
        return self.font
    def getFontSize(self):
        return self.font_size
    def setTheme(self, theme):
        self.theme = theme
    def setFont(self, font):
        self.font = font
    def setFontSize(self, font_size):
        self.font_size = font_size
    def save(self):
        config = {
            "theme": self.theme,
            "font": self.font,
            "font_size": self.font_size
        }
        with open("config/config.json", "w") as f:
            json.dump(config, f)
    def load(self):
        with open("config/config.json") as f:
            data = json.load(f)
            self.theme = data["theme"]
            self.font = data["font"]
            self.font_size = data["font_size"]
