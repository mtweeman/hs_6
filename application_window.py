from tkinter import *
from ctypes import windll


class ApplicationWindow(Tk):
    def __init__(self):
        self.__set_taskbar_icon()  # needs to be set before creating any windows
        self.__set_dpi_awareness()  # needs to be set before creating any windows

        Tk.__init__(self)

        self.name = 'Hajle Silesia Homebrewing System'
        self.version = 6
        self.icon_path = 'images/icon.ico'

        self.__set_window()

    def __set_taskbar_icon(self):
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')

    def __set_dpi_awareness(self):
        windll.shcore.SetProcessDpiAwareness(1)

    def __set_window(self):
        self.__set_title()
        self.__set_window_icon()
        self.__set_size()

    def __set_title(self):
        self.title(self.name + ' ' + str(self.version))

    def __set_window_icon(self):
        self.iconbitmap(self.icon_path)

    def __set_size(self):
        self.state('zoomed')
