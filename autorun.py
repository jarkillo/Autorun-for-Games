import tkinter as tk
from tkinter import simpledialog
import keyboard
import threading
import time
import pygetwindow as gw

app = tk.Tk()
app.title("Control de Autorun")

# Variables globales
autorun_active = tk.BooleanVar(value=False)
hotkey = None
window_focus_title = None

def run_autorun():
    """ Simula la pulsación continua de la tecla 'w' solo si la ventana deseada está enfocada. """
    while autorun_active.get():
        focused_window = gw.getActiveWindow()
        if focused_window and focused_window.title == window_focus_title:
            keyboard.press('w')
            time.sleep(0.1)
        else:
            keyboard.release('w')
            time.sleep(0.5)

def toggle_autorun():
    """ Activa o desactiva el autorun. """
    if autorun_active.get():
        autorun_active.set(False)
        keyboard.release('w')
        status_label.config(text="Autorun: Desactivado")
    else:
        if not hotkey:
            status_label.config(text="Por favor, configura primero una tecla para el autorun.")
            return
        autorun_active.set(True)
        status_label.config(text="Autorun: Activado")
        threading.Thread(target=run_autorun, daemon=True).start()

def set_hotkey():
    """ Configura la hotkey desde un diálogo de entrada. """
    global hotkey
    hotkey = simpledialog.askstring("Configurar Hotkey", "Presiona la tecla que deseas configurar:")
    if hotkey:
        hotkey_label.config(text=f"Tecla configurada para autorun: {hotkey}")
        keyboard.add_hotkey(hotkey, toggle_autorun)
        status_label.config(text="Autorun: Desactivado")

def show_window_selector():
    """ Muestra una ventana nueva con una lista de ventanas abiertas. """
    selector = tk.Toplevel(app)
    selector.title("Seleccionar Ventana")
    
    listbox = tk.Listbox(selector)
    listbox.pack(fill=tk.BOTH, expand=True)
    
    windows = gw.getAllTitles()
    for title in windows:
        if title:  # evita añadir títulos vacíos
            listbox.insert(tk.END, title)
    
    def on_select(evt):
        global window_focus_title
        window_focus_title = listbox.get(listbox.curselection())
        focus_window_label.config(text=f"Ventana enfocada: {window_focus_title}")
        selector.destroy()
    
    listbox.bind('<<ListboxSelect>>', on_select)

# UI Setup
status_label = tk.Label(app, text="Autorun: Desactivado")
status_label.pack(pady=10)

toggle_btn = tk.Button(app, text="Activar/Desactivar Autorun", command=toggle_autorun)
toggle_btn.pack(pady=10)

set_key_btn = tk.Button(app, text="Configurar Tecla para Autorun", command=set_hotkey)
set_key_btn.pack(pady=10)

hotkey_label = tk.Label(app, text="Ninguna tecla para autorun configurada")
hotkey_label.pack(pady=10)

focus_window_btn = tk.Button(app, text="Seleccionar Ventana", command=show_window_selector)
focus_window_btn.pack(pady=10)

focus_window_label = tk.Label(app, text="Ninguna ventana enfocada configurada")
focus_window_label.pack(pady=10)

app.mainloop()
