import PySimpleGUI as sg
import os

layout = [
			[sg.Graph((500,500), (0,0), (500,500), background_color='White', key='lienzo', visible=True)],
			[sg.Text('Archivo de colores:')],
            [sg.Input(key='colores_directorio'), sg.FileBrowse('Explorar', file_types=(('TXT', '*.txt'),), button_color=('White', 'Black'), font=('Arial', 10), target='colores_directorio', key='colores')],
			[sg.Text('Archivo de coordenadas:')],
		    [sg.Input(key='coord_directorio'), sg.FileBrowse('Explorar', file_types=(('TXT', '*.txt'),), button_color=('White', 'Black'), font=('Arial', 10), target='coord_directorio', key='coord')],
			[sg.Button('OK')]
        ]

window = sg.Window('Puntos y colores', layout)
window.Finalize()
lienzo = window['lienzo']

while True:
	event, values = window.read()
	if event is None:
		break
	if event is 'OK':
		if (os.path.isfile(values['colores_directorio'])) and (os.path.isfile(values['coord_directorio'])):
			color_list = open(values['colores_directorio'], 'r').read()
			color_list = color_list.splitlines()
			coord_list = open(values['coord_directorio'], 'r').read()
			coord_list = coord_list.splitlines()
			if len(coord_list) == len(color_list):
				coord_list = [coord.split(",") for coord in coord_list]
				for index in range(0, len(coord_list)):
					try:
						lienzo.DrawPoint((int(coord_list[index][0]), int(coord_list[index][1])), size=8, color=color_list[index])
					except ValueError:
						#Si la coordenada contiene un sólo valor (sólo x, o sólo y), no es una coordenada
						if (len(coord_list[index]) == 1):
							sg.popup_error('La coordenada', coord_list[index][0], 'es incorrecta')
			else:
				sg.popup_error('La cantidad de líneas en los archivos de texto no coinciden. Falta un color o una coordenada.')
		else:
			sg.popup_error('Falta seleccionar uno de los dos archivos')
