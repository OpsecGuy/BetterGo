import json, os
from helper import config_example

class Config():
    def __init__(self):
        # Default config name
        self.config_name = 'BetterGo_config'
        # Get absolute directory
        self.get_abs_dir = os.getcwd()
        # Config folder name to set
        self.get_cfg_dir = self.get_abs_dir + '\\' + self.config_name
        
        # Check if config folder exists
        if os.path.exists(self.get_cfg_dir):
            pass
        else:
            # Create folder with configs
            os.mkdir(self.config_name)

    def create_default_config(self, file_name):
        try:
            with open(f'{self.get_cfg_dir}\\'+ rf'{file_name}', 'w+') as file:
                file.flush()
                file.write(json.dumps(config_example))

        except Exception as err:
            print(err)

    def get_config_list(self):
        buffer = []
        list = os.listdir(self.get_cfg_dir)
        for config in list:
            if '.json' in config:
                buffer.append(config.removesuffix('.json'))
        return buffer

    def read_value(self, file_name: str, category: str, object: str):
        try:
            with open(f'{self.get_cfg_dir}\\'+ rf'{file_name}.json', 'r') as f:
                content = json.load(f)
                return(content[category][object])
        except Exception as err:
            print(err)
