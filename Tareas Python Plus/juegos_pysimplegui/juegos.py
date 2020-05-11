import hangman
import reversegam
import tictactoeModificado
import PySimpleGUI as sg
import json


def main_layout():
	sg.theme('DarkTeal')
	column_layout = [[sg.Combo(['Ahorcado', 'Ta-Te-Ti', 'Otello'], readonly=True, default_value='Ahorcado', auto_size_text=True, font=('Arial',12), key='opciones')],
				[sg.Button('¡Jugar!', key='jugar'), sg.Button('Guardar y salir', key='salir')]]
	frame_layout = [[sg.Text("Aquí se mostrarán sus datos una vez que hayan sido cargados.\nJuegue un juego primero.", key='salida_datos', font=('Arial', 10), text_color='White')]]
	layout = [[sg.Image(filename='menu.png')],
			[sg.Text('¡Bienvenido! Seleccione el juego que desea jugar:', text_color='#88BDD0', font=('Arial', 16))],
			[sg.Column(column_layout), sg.VerticalSeparator(), sg.Frame('Datos del usuario', frame_layout, element_justification='left', key='frame')]]
	return layout

def user_data_layout():
	sg.theme('DarkAmber')
	layout = [[sg.Text('Antes de comenzar a jugar, por favor ingrese sus datos.', font=('Arial', 10), justification='center')],
				[sg.Text('Tenga en cuenta que estos serán guardados una vez que seleccione "Salir", luego de finalizado el juego.', font=('Arial', 10), justification='center')],
				[sg.Text('Nombre: '), sg.InputText(key='nombre')],
				[sg.Text('Edad: '), sg.InputText(key='edad')],
				[sg.Text('Pasatiempo favorito: '), sg.InputText(key='pasatiempo')],
				[sg.Button('OK', key='OK')]]
	return layout

def user_data_window(layout, user_data, selected_game):
	data_window = sg.Window('Datos del usuario', layout)
	data_window.Finalize()
	while True:
		event, values = data_window.read()
		if (event is None):
			break
		if (event is 'OK'):
			user_data['Nombre'] = values['nombre']
			user_data['Edad'] = values['edad']
			user_data['Pasatiempo'] = values['pasatiempo']
			if (selected_game not in user_data['Juegos seleccionados']):
				user_data['Juegos seleccionados'].append(selected_game)
			break
	data_window.Close()
	return user_data

def user_data_load(filename):
	player = {}
	try:
		with open(filename, 'r') as f:
			player = json.load(f)
	except:
		#Si el archivo está dañado o no se encontró, se inicializa la lista de juegos
		player = {'Juegos seleccionados': []}
	return player

def user_data_save(filename, player):
	with open(filename, 'w') as f:
		json.dump(player, f)

def update_output(output_text, user_data):
	if (not empty_user(user_data)):
		output_text.Update(value=f"Hola, {user_data['Nombre']}. ¡{user_data['Pasatiempo']} es un gran pasatiempo! No olvides guardar\ntus datos presionando 'Guardar y salir'")

def empty_user(user_data):
	return len(user_data['Juegos seleccionados']) == 0

def main(args):
	layout = main_layout()
	window = sg.Window('Batería de juegos', layout)
	window.Finalize()

	#Carga los datos del usuario (si los hubiese)
	user_data = user_data_load('jugador.json')

	while True:
		update_output(window['salida_datos'], user_data)
		event, values = window.read()
		if (event is None) or (event is 'salir'):
			#Si jugó al menos un juego, pregunta si desea guardar los datos
			if (not empty_user(user_data)):
				choose = sg.popup_ok_cancel('¿Desea guardar sus datos antes de salir?', keep_on_top=True)
				if choose is 'OK':
					user_data_save('jugador.json', user_data)
			break
		if (event is 'jugar'):
			#Si nunca se cargaron los datos del usuario, los solicita
			if (empty_user(user_data)):
				user_data = user_data_window(user_data_layout(), user_data, values['opciones'])
			elif (values['opciones'] not in user_data['Juegos seleccionados']):
					user_data['Juegos seleccionados'].append(values['opciones'])
			sg.popup('El juego se ejecutará a continuación en la terminal.', title='¡Atención!')
			if (values['opciones'] == 'Ahorcado'):
				hangman.main()
				window.BringToFront()
			elif (values['opciones'] == 'Ta-Te-Ti'):
				tictactoeModificado.main()
				window.BringToFront()
			elif (values['opciones'] == 'Otello'):
				reversegam.main()
				window.BringToFront()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
