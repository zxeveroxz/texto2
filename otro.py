import tkinter as tk
import pyautogui
import pyperclip
import pygetwindow as gw
from datetime import datetime

# Lista de colores para los botones
button_colors = ['#FF5733', '#2ADFAD','#33FF57', '#5733FF', '#33FFFF', '#FFCFAA', '#33AFFA',  '#3CCFFF',]


def get_focused_window():
    return gw.getWindowsWithTitle(gw.getActiveWindow().title)[0]

def write_to_active_window(text):
    active_window = get_focused_window()
    active_window.activate()
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')

def on_button_click(text):
    write_to_active_window(text)

def read_button_text_from_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

app = tk.Tk()
app.title('Aplicación de Escritorio')
app.geometry('300x400')

# Frame para contener los botones dinámicos
button_frame = tk.Frame(app)
button_frame.pack(pady=20)

# Leer el contenido del archivo lista.txt y crear botones
button_texts = read_button_text_from_file('lista.txt')
for text in button_texts:
    button_text = text.strip()
    if button_text:
        # Seleccionar un color X para cada botón según el índice
        button_color = button_colors[index % len(button_colors)]

        button = tk.Button(button_frame, text=button_text, bg=button_color, command=lambda t=button_text: on_button_click(t))
        button.pack(pady=5)

# Establecer el atributo "topmost" de la ventana en True
app.wm_attributes("-topmost", True)

app.mainloop()