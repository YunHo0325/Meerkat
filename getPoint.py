from pynput.mouse import Controller
from pynput.mouse import Listener, Button


def on_move(x, y):
    return


def on_click(x, y, button, pressed):
    if pressed:
        print(x, y)
        return False


def on_scroll(x, y, dx, dy):
    return


with Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    listener.join()
