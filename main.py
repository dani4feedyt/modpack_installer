import view
import ctypes
import os


def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


window = view.Window()

if __name__ == '__main__':
    window.is_admin = isAdmin()
    window.start()


