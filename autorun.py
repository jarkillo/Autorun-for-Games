import tkinter as tk
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
    """ Activa o desactiva el autorun, actualizando la etiqueta de estado. """
    if autorun_active.get():
        autorun_active.set(False)
        keyboard.release('w')
        app.after(100, lambda: status_label.config(text="Autorun: Desactivado"))
    else:
        autorun_active.set(True)
        app.after(100, lambda: status_label.config(text="Autorun: Activado"))
        threading.Thread(target=run_autorun, daemon=True).start()

def set_hotkey():
    """ Captura la combinación de teclas en un hilo separado para no bloquear la GUI. """
    def capture_hotkey():
        global hotkey
        app.after(100, lambda: hotkey_label.config(text="Pulsa la combinación de teclas y luego Enter para finalizar..."))
        recorded = keyboard.record(until='enter')
        hotkey_events = [event for event in recorded if event.event_type == 'down' and event.name != 'enter']
        hotkey = '+'.join({event.name for event in hotkey_events})
        keyboard.add_hotkey(hotkey, toggle_autorun)
        app.after(100, lambda: hotkey_label.config(text=f"Tecla configurada para autorun: {hotkey}"))
        app.after(100, lambda: status_label.config(text="Autorun: Desactivado"))
    
    threading.Thread(target=capture_hotkey, daemon=True).start()

def show_window_selector():
    """ Muestra una ventana nueva con una lista de ventanas abiertas. """
    selector = tk.Toplevel(app)
    selector.title("Seleccionar Ventana")
    
    listbox = tk.Listbox(selector)
    listbox.pack(fill=tk.BOTH, expand=True)
    
    windows = gw.getAllTitles()
    for title in windows:
        if title:
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

set_key_btn = tk.Button(app, text="Configurar Tecla para Autorun", command=set_hotkey)
set_key_btn.pack(pady=10)

hotkey_label = tk.Label(app, text="Ninguna tecla para autorun configurada")
hotkey_label.pack(pady=10)

focus_window_btn = tk.Button(app, text="Seleccionar Ventana", command=show_window_selector)
focus_window_btn.pack(pady=10)

focus_window_label = tk.Label(app, text="Ninguna ventana enfocada configurada")
focus_window_label.pack(pady=10)

app.mainloop()
