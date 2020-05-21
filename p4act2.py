import PySimpleGUI as sg
import string
import random

def draw_letter(filled_spaces, selected_space, board_a, letras, id_letras, identity):
	filled_spaces.append(selected_space[0])
	#En caso de haber clickeado en dos elementos superpuestos, toma el primero
	coord = board_a.GetBoundingBox(selected_space[0])
	print('Dimensión del rectángulo:', coord)
	board_a.DrawText(letras[id_letras.index(identity)], (coord[0][0]+25, coord[0][1]-25), color='#601B1B', font=('Arial', 30),text_location='center')

def draw_boards(board_a, board_b):
	for filas in range(0,500,50):
		for columnas in range(0,500,50):
			board_a.DrawRectangle((0+filas,0+columnas),(50+filas,50+columnas), fill_color='#A1D8E0', line_color='#123E44', line_width=5)

	for columnas in range(0,250,50):
		board_b.DrawRectangle((0+columnas,0),(50+columnas, 50), fill_color='#885873', line_color='#FFFFFF', line_width=5)

def main_layout():
	sg.theme('DarkAmber')
	layout = [
				[sg.Graph((500,500), (0,0), (500,500), background_color='#3296A5', enable_events=True, key='board_a', visible=True),
			 	sg.VerticalSeparator(pad=(25,25)),
			 	sg.Graph((250,50),(0,0), (250,50), background_color='#AC0E47', enable_events=True, key='board_b', visible=True)]
				]
	return layout

def board_a_event(waiting_board, window, board_a, filled_spaces, letras, id_letras, identity, horizontal, vertical):
	while waiting_board:
		event, values = window.read()
		if event is None:
			waiting_board = False
		if event is 'board_a':
			selected_space = board_a.GetFiguresAtLocation(values['board_a'])
			print('Espacio/s obtenidos:', selected_space[0])
			if (len(filled_spaces) == 0):
				draw_letter(filled_spaces, selected_space, board_a, letras, id_letras, identity)
				break
			elif (selected_space[0] not in filled_spaces):
				if ((horizontal == False) and (vertical == False)):
					#Si seleccionó el casillero que está a la izquierda o a la derecha del último
					if (selected_space[0] == filled_spaces[-1]-10) or (selected_space[0] == filled_spaces[-1]+10):
						horizontal = True
					#Si se seleccionó el que está encima o debajo del último
					elif ((selected_space[0] == filled_spaces[-1]-1) or (selected_space[0] == filled_spaces[-1]+1)):
						vertical = True
				if (horizontal == True):
					if ((selected_space[0] == filled_spaces[-1]-10) or (selected_space[0] == filled_spaces[-1]+10)):
						draw_letter(filled_spaces, selected_space, board_a, letras, id_letras, identity)
						break
				elif (vertical == True):
					if ((selected_space[0] == filled_spaces[-1]-1) or (selected_space[0] == filled_spaces[-1]+1)):
						draw_letter(filled_spaces, selected_space, board_a, letras, id_letras, identity)
						break
	return (waiting_board, horizontal, vertical)

def main():
	window = sg.Window('Tableros', main_layout())
	window.Finalize()

	board_a = window['board_a']
	board_b = window['board_b']

	letras = [random.choice(string.ascii_letters) for i in range(0,5)]
	print(letras)

	draw_boards(board_a, board_b)

	id_letras = [board_b.DrawText(letras[i], ((i*50)+25,25), color='#FFFFFF', font=('Arial', 30),text_location='center') for i in range(0,5)]
	print('El ID de cada letra es:', id_letras)

	vertical = False
	horizontal = False
	filled_spaces = []
	waiting_board = True
	while waiting_board:
		event, values = window.read()
		if event is None:
			waiting_board = False
		if event is 'board_b':
			print('Click en la posición', values['board_b'])
			element_obtained = board_b.GetFiguresAtLocation(values['board_b'])
			print('Elemento/s obtenidos:', element_obtained)
			for identity in id_letras:
				if (identity in element_obtained):
					board_b.DeleteFigure(element_obtained[1])
					waiting_board, horizontal, vertical = board_a_event(waiting_board, window, board_a, filled_spaces, letras, id_letras, identity, horizontal, vertical)


if __name__ == '__main__':
	main()
