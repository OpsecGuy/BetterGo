import json, ctypes

class Config():
    def __init__(self):
        pass
    
    def read(*args):
        try:
            with open('settings.json') as f:
                content = json.load(f)
                
                if len(args) == 1:
                     return content[args[0]]
                    
                elif len(args) > 1:
                    # Validate variable read from json file
                    for title in content:
                        if title == args[0]:
                            return content[title][args[1]]
                
        except Exception as err:
            ctypes.windll.user32.MessageBoxW(0, f'Reason:\n{err}', 'Fatal Error', 0)
            return
