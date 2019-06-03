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

    main_window_layout = [
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


    window = sg.Window('Multi Part Print Calculator', main_window_layout)  

    while True: # Event Loop
        event, values = window.Read(timeout=100)  
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
                num_models = len(models)

                progress_bar_window_layout = [
                    [sg.Text('', key='title')],
                    [sg.ProgressBar(max_value=num_models, orientation='h',
                        size=(20, 20), key='progressbar'),
                        sg.Text('', key='num_completed'), sg.Text('/'), 
                        sg.Text('', key='num_total')],      
                    [sg.Cancel()]
                ]

                progress_bar_window = sg.Window('Slicing models...', 
                                                progress_bar_window_layout)
                progress_bar = progress_bar_window.Element('progressbar')
                progress_bar_window.Element('title').Update(
                    value='This is the longest step! Please be patient, even' +\
                          ' if the program stops responding.')
                progress_bar_window.Element('num_total').Update(
                    value=str(num_models))

                gcode_file_names = []
                for i in range(num_models):
                    # sg.OneLineProgressMeter('Slicing models...', i+1, 
                    #                                num_models, 
                    #                                'single')
                    mpp.slice_models(layer_height, supports, [models[i]])
                    gcode_file_names.append(
                        mpp.get_gcode_output_path(models[i], layer_height))
                    event, values = window.Read(timeout=0)  
                    if event is None or event == 'Cancel':  
                        break
                    progress_bar.UpdateBar(i+1)
                    progress_bar_window.Element('num_completed').Update(
                        text=str(i+1))
                
                estimates = []
                print("gcode_file_names", gcode_file_names)
                for i in range(num_models):
                    # the scraper function returns a list and we just want the
                    # first element
                    estimates.append(
                        mpp.scrape_time_and_usage_estimates(
                            [gcode_file_names[i]])
                            [0])
                    sg.OneLineProgressMeter('Scraping .gcode files ' + \
                                            'for estimates...', i+1, 
                                            num_models, 'scraping_progress')
                
                estimates.insert(0, mpp.aggregate_data(estimates))

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
