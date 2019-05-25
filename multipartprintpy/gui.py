import PySimpleGUI as sg
import sys

def main():
    layout = [[sg.Text('Your typed chars appear here:'),
               sg.Text('', key='_OUTPUT_') ],  
              [sg.Input(do_not_clear=True, key='_IN_')],  
              [sg.Text('Broswe for .stl files'), 
               sg.InputText(key='_STL_FILES_'), sg.FilesBrowse()],
              [sg.Button('Show'), sg.Button('Exit')]]  

    window = sg.Window('Multi Part Print Calculator', layout)  

    while True:                 # Event Loop
      event, values = window.Read()  
      print(event, values)
      if event is None or event == 'Exit':  
          break  
      if event == 'Show':  
          # change the "output" element to be the value of "input" element  
          window.Element('_OUTPUT_').Update(values['_IN_'])

    window.Close()

if __name__ == '__main__':
    main()
