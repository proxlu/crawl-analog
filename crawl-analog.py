#!/bin/python3
from pynput import keyboard
from pynput.keyboard import Controller, Key
import time
import subprocess
import re

# Controlador de teclado para enviar teclas
keyboard_controller = Controller()

# Variáveis para armazenar o estado das teclas
key_state = {
    'w': False,
    'a': False,
    's': False,
    'd': False
}

def on_press(key):
    try:
        if key.char in key_state:
            key_state[key.char] = True
    except AttributeError:
        pass

def on_release(key):
    try:
        if key.char in key_state:
            key_state[key.char] = False
    except AttributeError:
        pass

def get_analog_input():
    x, y = 0, 0
    if key_state['w']:
        y += 1
    if key_state['s']:
        y -= 1
    if key_state['a']:
        x -= 1
    if key_state['d']:
        x += 1
    return x, y

def press_key_by_analog(x, y):
    # Mapeamento para teclas numéricas
    if x == 0 and y == 1:
        keyboard_controller.press(Key.up)
        keyboard_controller.release(Key.up)
    elif x == 0 and y == -1:
        keyboard_controller.press(Key.down)
        keyboard_controller.release(Key.down)
    elif x == -1 and y == 0:
        keyboard_controller.press(Key.left)
        keyboard_controller.release(Key.left)
    elif x == 1 and y == 0:
        keyboard_controller.press(Key.right)
        keyboard_controller.release(Key.right)
    elif x == -1 and y == 1:
        keyboard_controller.press(Key.home)
        keyboard_controller.release(Key.home)
    elif x == 1 and y == 1:
        keyboard_controller.press(Key.page_up)
        keyboard_controller.release(Key.page_up)
    elif x == -1 and y == -1:
        keyboard_controller.press(Key.end)
        keyboard_controller.release(Key.end)
    elif x == 1 and y == -1:
        keyboard_controller.press(Key.page_down)
        keyboard_controller.release(Key.page_down)

def is_crawl_active():
    """Verifica se a janela do jogo 'dungeon crawl stone soup 0' está em primeiro plano."""
    try:
        # Obtém o título da janela ativa
        active_window = subprocess.run(['xdotool', 'getwindowfocus', 'getwindowname'], stdout=subprocess.PIPE)
        return re.search(r"dungeon crawl stone soup [0-9]", active_window.stdout.decode().lower())
    except Exception as e:
        print(f"Erro ao verificar a janela: {e}")
        return False

def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while True:
            if is_crawl_active():
                x, y = get_analog_input()
                press_key_by_analog(x, y)
            time.sleep(0.1)  # Evita sobrecarga de CPU

if __name__ == "__main__":
    main()
