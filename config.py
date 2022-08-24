import json, os
from helper import config_example, ctypes

class Config():
    def __init__(self):
        pass
    
    def file_exist(self, file_name):
        path = f'{os.getcwd()}\\'
        config = path + file_name + '.json'
        if os.path.exists(config):
            return True
        else:
            return False
    
    def save_file(self, file_name: str):
        try:
            with open(f'{file_name}.json', 'x') as file:
                file.write(json.dumps(config_example))
        except FileExistsError as err:
            ctypes.windll.user32.MessageBoxW(0, f'File {file_name}.json already exists!', 'Config Error', 0)

    def read_value(self, file_name: str, category: str, object: str):
        if self.file_exist(file_name):
            with open(f'{file_name}.json', 'r') as f:
                content = json.load(f)
                return(content[category][object])
        return
