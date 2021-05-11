from tkinter.ttk import Notebook
from tab import *


class TabBar(Notebook):
    def __init__(self, application_window):
        Notebook.__init__(self, application_window)

        self.__tabs = []

        self.__set_tab_bar()

    def __set_tab_bar(self):
        self.__create_tabs()
        self.__add_tabs_to_tab_bar()
        self.__position_tab_bar()

    def __create_tabs(self):
        self.__tabs.append(RecipeTab(self))

    def __add_tabs_to_tab_bar(self):
        for tab in self.__tabs:
            self.add(tab, text=tab.get_name())

    def __position_tab_bar(self):
        self.pack(fill=BOTH, expand=1)
