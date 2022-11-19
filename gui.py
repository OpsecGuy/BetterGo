import dearpygui.dearpygui as dpg
import config, time, paramiko, os

class Window():
    def __init__(self) -> None:
        self.cfg = config.Config()
        print('Window initialization started.')

    def callback(self, sender, data):
        print(f'{sender} ==> {data}')
        return sender, data
        
    def create(self) -> None:
        dpg.create_context()
        
        with dpg.window(label='Window', height=400, width=400, no_title_bar=True, no_bring_to_front_on_focus=True):
            dpg.add_text(default_value='Servers List')
            dpg.add_listbox(items=list(self.cfg.get_servers()), tag='servers_list', width=200)
            with dpg.group(horizontal=True):
                dpg.add_button(label='Refresh', tag='b_refresh', callback=lambda: dpg.set_value('servers_list', (self.cfg.get_servers())))
                dpg.add_button(label='Connect', tag='b_connect', callback=self.connect)
                dpg.add_button(label='Execute', tag='b_execute', callback=self.execute_cmd)

            with dpg.group(horizontal=True):
                dpg.add_text(label='IP', tag='ip', show=False, color=(255, 100, 0))
                dpg.add_text(label='Username', tag='username', show=False, color=(255, 0, 0))
                dpg.add_text(label='Password', tag='password', show=False, color=(255, 0, 100))
                
            with dpg.group(horizontal=True):
                dpg.add_button(label='Show', tag='b_unsafe', callback=self.show_context)
                dpg.add_button(label='Hide', tag='b_safe', callback=self.hide_context)
            
            dpg.add_input_text(label='File Name', default_value='commands', width=200 ,tag='i_commands')
            with dpg.group(horizontal=True):
                dpg.add_button(label='Save', tag='b_confirmed_cmd', callback=self.get_file)
                dpg.add_button(label='Clear', tag='b_purge', callback=lambda: dpg.set_value('i_commands', ''))
                dpg.add_radio_button(['.txt', '.json'], label='extension', tag='rb_extension', default_value='.txt', horizontal=True)
            dpg.add_separator()
            dpg.add_text('Status: Waiting...', tag='status', color=(0, 255, 0))
            
    def update(self):
        while True:
            try:
                dpg.set_value('ip', self.cfg.get_value(dpg.get_value('servers_list'), 'IP'))
                dpg.set_value('username', self.cfg.get_value(dpg.get_value('servers_list'), 'username'))
                dpg.set_value('password', self.cfg.get_value(dpg.get_value('servers_list'), 'password'))
                

            except (FileNotFoundError, PermissionError):
                print(f'Could not find {self.cfg.config_file}! New config has been created.')
                self.cfg.create_example()
            time.sleep(0.01)


    def run(self) -> None:
        dpg.create_viewport(title='Awesome Server Manager 1.0', height=400, width=400)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()


    def destroy(self) -> None:
        dpg.destroy_context()

    def hide_context(self):
        dpg.hide_item('ip')
        dpg.hide_item('username')
        dpg.hide_item('password') 
        
    def show_context(self):
        dpg.show_item('ip')
        dpg.show_item('username')
        dpg.show_item('password')

    def get_file(self) -> str:
        try:
            input = dpg.get_value('i_commands')
            extension_file = dpg.get_value('rb_extension')
            if input != '':
                path = f"{os.getcwd()} + '\\' + {input + extension_file}"
                return input + extension_file
        except Exception as err:
            print(err)
            
    def is_valid(self):
        if dpg.get_value('servers_list') == 'None':
            dpg.set_value('status', f'Chose correct server!')
            return False
        else:
            return True
    
    def parse_command(self):
        dpg.set_value('status', f'Trying to open a file.')
        with open(self.get_file(), 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if line is not '\n':
                    escaped = ''.join(line.replace('\n', ' && '))
                    buffer = buffer + escaped
        return buffer
                
    def connect(self) -> None:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if dpg.get_value('servers_list') == 'None':
                dpg.set_value('status', f'Server "None" can not be used!')
                return
                
            dpg.set_value('status', f'Connecting to {dpg.get_value("ip")}')
            client.connect(hostname=dpg.get_value('ip'), port=22, username=dpg.get_value('username'), password=dpg.get_value('password'), timeout=5.0)
            dpg.set_value('status', f'Connection Established.')
            client.close()
            dpg.set_value('status', f'Connected Successfully.')
        except Exception:
            dpg.set_value('status', f'An Error Occurred!')


    def execute_cmd(self) -> None:
        try:
            buffer = ''
            if self.is_valid():
                dpg.set_value('status', f'Connecting to {dpg.get_value("ip")}')
                dpg.set_value('status', f'Processing..')
                self.parse_command()
                
        except Exception as err:
            print(err)
        