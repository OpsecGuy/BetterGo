import PySimpleGUI as gui

class GUI():
    def __init__(self) -> None:
        gui.theme('Dark')
        gui.theme_text_color('white')
        self.layout = [
            [gui.Text('Spectator list', key='spec_list_text')],
            [gui.Text('', key='spec_list')]]

    def create_window(self):
        window = gui.Window('_', self.layout,
            resizable=True ,no_titlebar=True,
            finalize=True, grab_anywhere=True, keep_on_top=True, 
            alpha_channel=0.7, element_justification='center')

        return window
