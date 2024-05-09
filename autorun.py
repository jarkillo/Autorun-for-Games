import keyboard
import time
import pygetwindow as gw
import sys

def elegir_ventana():
    ventanas = gw.getAllWindows()
    print("Selecciona la ventana del juego:")
    for i, ventana in enumerate(ventanas):
        print(f"{i + 1}: {ventana.title}")
    eleccion = int(input("Introduce el número de la ventana: ")) - 1
    return ventanas[eleccion]

window = elegir_ventana()

autorun = False

def toggle_autorun():
    global autorun, window
    if window and window.isActive:
        autorun = not autorun
        if autorun:
            keyboard.press('w')
            print("Autorun activado.")
        else:
            keyboard.release('w')
            print("Autorun desactivado.")
    else:
        print("El juego no está activo o el título de la ventana no coincide.")

def exit_program():
    global running
    print("Cerrando el programa...")
    keyboard.release('w')  # Libera la tecla en caso de que esté presionada
    running = False  # Establece running a False para detener el bucle


def configurar_teclas():
    global toggle_key, exit_key
    
    print("Presiona y suelta la combinación de teclas para alternar el autorun:")
    toggle_key = leer_combinacion()
    print(f"Combinación registrada para alternar autorun: {toggle_key}")
    
    while True:
        print("Presiona y suelta la combinación de teclas para salir del programa:")
        exit_key = leer_combinacion()
        if exit_key != toggle_key:
            print(f"Combinación registrada para salir del programa: {exit_key}")
            break
        else:
            print("Error: La combinación de teclas para salir no puede ser la misma que para alternar el autorun. Intenta otra combinación.")


def leer_combinacion():
    combinacion = keyboard.read_hotkey(suppress=False)
    while any([keyboard.is_pressed(key) for key in combinacion.split('+')]):
        time.sleep(0.1)  # Pequeña pausa para evitar uso excesivo del CPU
    return combinacion


try:
    configurar_teclas()
    keyboard.add_hotkey(toggle_key, toggle_autorun)
    keyboard.add_hotkey(exit_key, exit_program)

    running = True
    print("Programa iniciado.")
    while running:
        time.sleep(1)
    print("Saliendo del bucle principal...")
except Exception as e:
    print(f"Error detectado: {str(e)}")
finally:
    keyboard.unhook_all_hotkeys()
    print("Teclas liberadas y programa cerrado correctamente.")






# Para crear el instalador

# pyinstaller --onefile autorun.py