import json, os
from helper import config_example

class Config():
    def __init__(self, cfg_name: str = None):
        self.cfg_name = cfg_name
        # Current dir
        self.get_abs_dir = os.getcwd()
        
        self.cfg_folder = 'Config'
        self.cfg_folder_dir = self.get_abs_dir + '\\' + self.cfg_folder
        
        # Check if config folder exists
        if not os.path.exists(self.cfg_folder_dir):
            os.mkdir(self.cfg_folder)

    def create_default(self):
        try:
            default_cfg_dir = self.cfg_folder_dir + '\\' + 'default.json'
            if not os.path.exists(default_cfg_dir):
                with open(default_cfg_dir, 'w+') as file:
                    file.flush()
                    file.write(json.dumps(config_example))
            
        except Exception as err:
            print(err)

    def get_path(self):
        return self.cfg_folder_dir + '\\' + self.cfg_name
    
    def get_config_list(self):
        return os.listdir(self.cfg_folder_dir)

    def read_value(self, category: str, object: str):
        try:
            config = self.cfg_folder_dir + '\\' + self.cfg_name
            # Check if config exists
            if os.path.exists(config):
                with open(config, 'r') as file:
                    data = json.load(file)
                    return(data[category][object])

        except Exception as err:
            print(err)
