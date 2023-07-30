import tkinter as tk
import pyautogui
import pyperclip
import pygetwindow as gw
from datetime import datetime

def get_focused_window():
    return gw.getWindowsWithTitle(gw.getActiveWindow().title)[0]

def read_button_text_from_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def write_to_active_window(text):
    active_window = get_focused_window()
    active_window.activate()
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press(' ') 

    app.after(100, show_main_window)

    # Enfocar el cuadro de texto en la ventana externa después de escribir el texto
    try:
        text_widget = active_window.widget(text='Text')
        text_widget.focus()
    except tk.TclError:
        print("Error: No se pudo encontrar el cuadro de texto en la ventana externa.")



def on_copy_button_click2(ttt):
    # Ocultar temporalmente la ventana de la aplicación
    app.withdraw()

    write_to_active_window(ttt)

    # Volver a mostrar la ventana de la aplicación después de la escritura
    app.deiconify()

def on_copy_button_click():
    current_time = datetime.now().strftime('%H:%M:%S')
    # Ocultar temporalmente la ventana de la aplicación
    app.withdraw()

    write_to_active_window(current_time)

    # Volver a mostrar la ventana de la aplicación después de la escritura
    app.deiconify()


def select_all_text():
      # Ocultar temporalmente la ventana de la aplicación
    app.withdraw()
    active_window = get_focused_window()
    active_window.activate()
    pyautogui.hotkey('ctrl', 'e')
    pyautogui.press('backspace')  # Emular la pulsación de la tecla "Retroceso" para borrar el espacio

 # Volver a mostrar la ventana de la aplicación después de la escritura
    app.deiconify()


def show_main_window():
    app.deiconify()



app = tk.Tk()
app.title('Aplicación de Escritorio')
# Obtener la altura de la pantalla
screen_height = app.winfo_screenheight()-100
#app.geometry(f'300x{screen_height}')
app.geometry(f'250x400')

copy_button = tk.Button(app, text='Escribir hora actual en ventana enfocada', command=on_copy_button_click)
copy_button.pack(pady=10)

copy_button2 = tk.Button(app, text='Copiar texto específico', command=lambda: on_copy_button_click2('Texto específico a copiar'))
copy_button2.pack(pady=30)


# Frame para contener los botones dinámicos
button_frame = tk.Frame(app)
button_frame.pack(pady=40)

# Leer el contenido del archivo lista.txt y crear botones
button_texts = read_button_text_from_file('lista.txt')
for text in button_texts:
    text_to_write, button_text = text.strip().split("|")
    button_text = button_text.strip()
    if button_text:
        button = tk.Button(button_frame, text=button_text, command=lambda r=text_to_write: on_copy_button_click2(r))
        button.pack(pady=5)

# Botón para seleccionar todo el texto en la ventana externa
select_all_button = tk.Button(app, text='Seleccionar Todo', command=select_all_text)
select_all_button.pack(pady=10)

# Establecer el atributo "topmost" de la ventana en True
app.wm_attributes("-topmost", True)

# Volver a mostrar la ventana principal después de un tiempo para evitar que se quede escondida si algo falla
app.after(1000, show_main_window)

app.mainloop()
