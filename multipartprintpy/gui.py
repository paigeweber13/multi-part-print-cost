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
                  window_location=(600, 200),
                  font='Fixedsys')

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
                #  [sg.Text('Now slicing...', key='_SLICING_PROGRESS_TEXT_',
                #      visible=False)],
                #  [sg.Image(filename=loading_gif_path, size=(64,64),
                #      key='_LOADING_GIF_', visible=False)],
                 [sg.Button(button_text='Get Estimates', visible=True)],
             ]

    window = sg.Window('Multi Part Print Calculator', layout)  

    while True: # Event Loop
        event, values = window.Read(timeout=100)  
        # window.Element('_LOADING_GIF_').UpdateAnimation(loading_gif_path)
        # print(event, values)
        if event is None or event == 'Exit':  
            break
        if event == 'Get Estimates':
            if validate_input(values['_STL_FILES_'],
                              values['_OUTPUT_FILE_DIR_']):
                window.Element('Get Estimates').Update(visible=False)
                # window.Element('_LOADING_TEXT_').Update(visible=True)
                # window.Element('_LOADING_GIF_').Update(
                #     filename=loading_gif_path, visible=True)

                layer_height = values['_LAYER_HEIGHT_']
                supports = values['_GENERATE_SUPPORTS?_']
                models = values['_STL_FILES_'].split(';')

                gcode_file_names = []
                print('models:', models)
                num_models = len(models)
                for i in range(num_models):
                    if not sg.OneLineProgressMeter('Slicing models...', i+1, 
                                                   num_models, 
                                                   'single'):
                        break
                    event, values = window.Read(timeout=0)
                    if event == 'Cancel' or event is None:
                        break
                    print('i:', i)
                    print('models[i]:', models[i])
                    mpp.slice_model(layer_height, supports, models[i])
                    gcode_file_names.append(
                        mpp.get_gcode_output_path(models[i]))
                
                stats = []
                for i in range(num_models):
                    # the scraper function returns a list and we just want the
                    # first element
                    stats.append(
                        mpp.scrape_time_and_usage_estimates(
                            gcode_file_names[i])[0])
                    if not sg.OneLineProgressMeter('Scraping .gcode files ' + \
                                            'for estimates...', i+1, 
                                            num_models, 'scraping_progress'):
                        break
                
                stats.insert(0, mpp.aggregate_data(stats))

                output_file = values['_OUTPUT_FILE_DIR_'] \
                    + '/_print_estimates.txt'
                result = mpp.output_results(estimates, output_file)
                result = 'Estimates have also been output to ' + output_file \
                    + '\n\n' + result

                window.Element('Get Estimates').Update(visible=True)
                # window.Element('_LOADING_TEXT_').Update(visible=False)
                # window.Element('_LOADING_GIF_').Update(
                #     filename=loading_gif_path, visible=False)

                sg.PopupScrolled(result, size=(120, 35))
            else:
                sg.Popup('You must input at least one .stl file and a place ' \
                         + 'to store the output!')

    window.Close()

if __name__ == '__main__':
    main()
