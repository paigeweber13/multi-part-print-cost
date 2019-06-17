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

    main_window_layout = [
                 [sg.Text('Broswe for .stl files (Hold shift to select '\
                          + 'multiple)')],
                 [sg.InputText(key='_STL_FILES_'), sg.FilesBrowse()],
                 [sg.Text('Select where the output data should be stored')],
                 [sg.InputText(key='_OUTPUT_FILE_DIR_'), sg.FolderBrowse()],
                 [sg.Text('Select which profile to use.')],
                 [sg.Text('Any slic3r-pe config file will work.')],
                 [sg.InputText(default_text='./profiles/default-profile.ini', key='_PROFILE_'), sg.FileBrowse()],
                 [sg.Text('Layer height')],
                 [sg.Slider(range=(0.05, 0.35), default_value=(0.2), 
                     resolution=(0.05), orientation='horizontal',
                     key='_LAYER_HEIGHT_')],
                 [sg.Checkbox('Generate supports', default=False,
                     key='_GENERATE_SUPPORTS?_')],
                 [sg.Button(button_text='Get Estimates', visible=True)],
             ]

    window = sg.Window('Multi Part Print Calculator', main_window_layout)  

    while True: # Event Loop
        event, values = window.Read(timeout=100)  
        if event is None or event == 'Exit':  
            break
        if event == 'Get Estimates':
            if validate_input(values['_STL_FILES_'],
                              values['_OUTPUT_FILE_DIR_']):
                window.Element('Get Estimates').Update(visible=False)

                layer_height = values['_LAYER_HEIGHT_']
                supports = values['_GENERATE_SUPPORTS?_']
                models = values['_STL_FILES_'].split(';')
                profile = values['_PROFILE_']

                result = ''
                gcode_file_names = []
                num_models = len(models)
                for i in range(num_models):
                    mpp.slice_models(layer_height, supports, [models[i]], 
                            profile=profile)
                    gcode_file_names.append(
                        mpp.get_gcode_output_path(models[i], layer_height))
                    if sg.OneLineProgressMeter('Slicing models...', i+1, 
                                                num_models, 'single') is False:
                        if num_models != i + 1:
                            result += 'Slicing was cancelled, not all ' + \
                                      'selected models are included.\n'
                        break
                
                estimates = []
                num_gcode_files = len(gcode_file_names)
                for i in range(num_gcode_files):
                    # the scraper function returns a list and we just want the
                    # first element
                    estimates.append(
                        mpp.scrape_time_and_usage_estimates(
                            [gcode_file_names[i]])
                            [0])
                    if sg.OneLineProgressMeter('Scraping .gcode files ' + \
                                               'for estimates...', i+1, 
                                               num_gcode_files,
                                               'scraping_progress') is False:
                        if num_models != i + 1:
                            result += 'Data scraping was cancelled, not ' + \
                                      'all selected models are included.\n'
                        break
                
                estimates.insert(0, mpp.aggregate_data(estimates))

                output_file = values['_OUTPUT_FILE_DIR_'] \
                    + '/_print_estimates.txt'
                result += 'Estimates have also been output to ' + output_file \
                    + '\n\n'
                result += mpp.output_results(estimates, output_file)

                window.Element('Get Estimates').Update(visible=True)
                sg.PopupScrolled(result, size=(120, 35))
            else:
                sg.Popup('You must input at least one .stl file and a place ' \
                         + 'to store the output!')

    window.Close()

if __name__ == '__main__':
    main()
