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
    loading_gif_path = 'assets/loading64x64.gif'

    gray = '#444444'
    sg.SetOptions(background_color='black',
                  element_background_color='black',
                  text_element_background_color='black',
                  input_elements_background_color=gray,
                  text_color='white',
                  element_text_color='white',
                  input_text_color='white',
                  button_color=('white', gray),
                  window_location=(600, 200))

    layout = [
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
                 [sg.Text('Now slicing...', key='_LOADING_TEXT_',
                     visible=False)],
                 [sg.Image(filename=loading_gif_path, size=(64,64),
                     key='_LOADING_GIF_', visible=False)],
                 [sg.Button(button_text='Get Estimates', visible=True)],
             ]

    window = sg.Window('Multi Part Print Calculator', layout)  

    while True: # Event Loop
        event, values = window.Read(timeout=100)  
        window.Element('_LOADING_GIF_').UpdateAnimation(loading_gif_path)
        print(event, values)
        if event is None or event == 'Exit':  
            break
        if event == 'Get Estimates':
            if validate_input(values['_STL_FILES_'],
                              values['_OUTPUT_FILE_DIR_']):
                window.Element('Get Estimates').Update(visible=False)
                window.Element('_LOADING_TEXT_').Update(visible=True)
                window.Element('_LOADING_GIF_').Update(
                    filename=loading_gif_path, visible=True)
            else:
                sg.Popup('You must input at least one .stl file and a place ' \
                         + 'to store the output!')

    window.Close()

if __name__ == '__main__':
    main()
