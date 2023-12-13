from gui import *
from task import *
from config import *

if __name__ == "__main__":
    config = Config()
    config.load()
    app = Application(config)
    # update data when tasklist is changed
    
