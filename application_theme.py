from tkinter.ttk import Style


class ApplicationTheme(Style):
    def __init__(self):
        Style.__init__(self)

        self.__name = 'hs_theme'
        self.__parent = 'classic'
        self.__settings = {'TNotebook': {'configure': {'background': '#888888'}},
                           'TNotebook.Tab': {'configure': {'background': '#555555',
                                                           'foreground': 'white',
                                                           'padding': [10, 10],
                                                           'font': (None, 14)},
                                             'label': {'side': ''},
                                             'map': {'background': [
                                                 ('selected', '#ffffff')],
                                                 'foreground': [
                                                     ('selected', 'black')]}},
                           'TCombobox': {'configure': {'arrowsize': 50}},
                           'TButton': {'configure': {'font': (None, 14),
                                                     'background': '#F0F0F0',
                                                     'padding': [10, 10]},
                                       'map': {'relief': [('pressed', 'sunken'),
                                                          ('!pressed', 'raised')]}},
                           'TLabel': {'configure': {'font': (None, 14),
                                                    'background': '#F0F0F0'}}}

        self.__set_theme()

    def __set_theme(self):
        self.theme_create(self.__name, self.__parent, self.__settings)
        self.theme_use(self.__name)
