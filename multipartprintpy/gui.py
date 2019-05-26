import PySimpleGUI as sg
import typing
import sys

import multipartprintpy.core as mpp

def validate_input(stl_files: typing.List[str], output_directory: str):
    """
    only validates whether or not input files and output directory are
    specified
    """
    if stl_files != '' and output_directory != '':
        return True
    else:
        return False

def main():
    layout = [
            #   [sg.Text('Your typed chars appear here:'),
            #    sg.Text('', key='_OUTPUT_') ],  
            #   [sg.Input(do_not_clear=True, key='_IN_')],  
            #   [sg.Button('Show'), sg.Button('Exit')],
                 [sg.Text('Broswe for .stl files (Hold shift to select '\
                          + 'multiple)')],
                 [sg.InputText(key='_STL_FILES_'), sg.FilesBrowse()],
                 [sg.Text('Select where the output data should be stored')],
                 [sg.InputText(key='_OUTPUT_FILE_DIR_'), sg.FolderBrowse()],
                 [sg.Text('Layer height')],
                 [sg.Slider(range=(0.05, 0.35), default_value=(0.2), 
                     resolution=(0.05), orientation='horizontal',
                     key='_LAYER_HEIGHT_')],
                 [sg.Checkbox('Generate supports', default=False,
                     key='_GENERATE_SUPPORTS?_')],
                 [sg.Button(button_text='Get Estimates', visible=True)],
                 [sg.Image(filename='assets/loading.gif', size=(60,60),
                     key='_LOADING_GIF_', visible=False)],
             ]

    window = sg.Window('Multi Part Print Calculator', layout)  

    while True: # Event Loop
        event, values = window.Read()  
        print(event, values)
        if event is None or event == 'Exit':  
            break
        if event == 'Get Estimates':
            print(values['_STL_FILES_'])
            if(validate_input(values['_STL_FILES_'],
                              values['_OUTPUT_FILE_DIR_'])):
                window.Element('Get Estimates').Update(visible=False)
                sg.Popup('Now slicing!')
            else:
                sg.Popup('You must input at least one .stl file and a place ' \
                         + 'to store the output!')
            # change the "output" element to be the value of "input" element  
          #   window.Element('_OUTPUT_').Update(values['_IN_'])

    window.Close()

if __name__ == '__main__':
    main()
