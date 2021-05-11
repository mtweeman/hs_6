from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk
from recipe_processor import XMLRecipeProcessor
from recipe_monitor import RecipeMonitor
from queue import Queue


class Tab(ABC, Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._name = None
        self._gui_elements = {}
        self._content = None
        self._special_content = None

        self._set_gui()

    def get_name(self):
        return self._name

    def _set_gui(self):
        self._create_gui_elements()
        self._add_text_to_gui_elements()
        self._add_gui_elements_to_the_grid()
        self._bind_commands_to_gui_elements()
        self._calculate_rows_quantity()
        self._calculate_columns_quantity()
        self._arrange_rows()
        self._arrange_columns()

    @abstractmethod
    def _create_gui_elements(self):
        pass

    def _add_text_to_gui_elements(self):
        pass

    @abstractmethod
    def _add_gui_elements_to_the_grid(self):
        pass

    def _bind_commands_to_gui_elements(self):
        pass

    def _calculate_rows_quantity(self):
        self._rows_quantity = self.grid_size()[1]
        return self._rows_quantity

    def _calculate_columns_quantity(self):
        self._columns_quantity = self.grid_size()[0]
        return self._columns_quantity

    def _arrange_rows(self):
        for i in range(self._rows_quantity):
            self.rowconfigure(i, weight=1, uniform='row')

    def _arrange_columns(self):
        for i in range(self._columns_quantity):
            self.columnconfigure(i, weight=1, uniform='column')

    def update(self, name, content, special_content):
        pass


class RecipeTab(Tab):
    def __init__(self, parent):
        Tab.__init__(self, parent)
        self._name = 'Recipe'
        self.__queue = Queue()
        self.__recipe_detector = RecipeMonitor(XMLRecipeProcessor(), self, self.__queue)

    def _create_gui_elements(self):
        self._gui_elements['USER_SETTINGS'] = UserSettingsContainer(self)
        self._gui_elements['RECIPE_NAME'] = ExtractedRecipeNameContainer(self)
        self._gui_elements['MISCS'] = ExtractedRecordsContainer(self)
        self._gui_elements['FERMENTABLES'] = ExtractedRecordsContainer(self)
        self._gui_elements['MASH_STEPS'] = ExtractedRecordsContainer(self)
        self._gui_elements['HOPS'] = ExtractedRecordsContainer(self)
        self._gui_elements['PARAMETERS'] = ExtractedParametersContainer(self)

    def _add_gui_elements_to_the_grid(self):
        self._gui_elements['USER_SETTINGS'].grid(row=0, column=0, columnspan=3, sticky=N + W + E)
        self._gui_elements['RECIPE_NAME'].grid(row=1, column=1)
        self._gui_elements['MISCS'].grid(row=2, column=0, sticky=NSEW)
        self._gui_elements['FERMENTABLES'].grid(row=2, column=1, sticky=NSEW)
        self._gui_elements['MASH_STEPS'].grid(row=3, column=0, sticky=NSEW)
        self._gui_elements['HOPS'].grid(row=3, column=1, sticky=NSEW)
        self._gui_elements['PARAMETERS'].grid(row=2, column=2, rowspan=2, sticky=NSEW)

    def _bind_commands_to_gui_elements(self):
        self.bind('<<processed_recipe>>', self.__update_content)

    def _arrange_rows(self):
        for i in range(2, self._rows_quantity):
            self.rowconfigure(i, weight=1)

    def __update_content(self, event):
        if not self.__queue.empty():
            if self._content:
                self._content = None
            self._content = self.__queue.get()
            self._special_content = self.__queue.get()
            self.__process_content()

    def __process_content(self):
        for gui_element_name, gui_element in self._gui_elements.items():
            if gui_element_name in self._content:
                gui_element.update(gui_element_name, self._content[gui_element_name],
                                   self._special_content[gui_element_name])


class UserSettingsContainer(Tab):
    def __init__(self, tab):
        Tab.__init__(self, tab)

    def _create_gui_elements(self):
        self._gui_elements['yos'] = ttk.Label(self, text='YOS')
        self._gui_elements['mlt_rinse'] = ttk.Label(self, text='MLT rinse')
        self._gui_elements['mlt_cip'] = ttk.Label(self, text='MLT CIP')
        self._gui_elements['bk_rinse'] = ttk.Label(self, text='BK rinse')
        self._gui_elements['bk_cip'] = ttk.Label(self, text='BK CIP')
        self._gui_elements['fermentation_program'] = ttk.Label(self, text='Fermentation program')
        self._gui_elements['fermentation_vessel'] = ttk.Label(self, text='Fermentation vessel')

    def _add_gui_elements_to_the_grid(self):
        self._gui_elements['yos'].grid(row=0, column=0)
        self._gui_elements['mlt_rinse'].grid(row=0, column=1)
        self._gui_elements['mlt_cip'].grid(row=0, column=2)
        self._gui_elements['bk_rinse'].grid(row=0, column=3)
        self._gui_elements['bk_cip'].grid(row=0, column=4)
        self._gui_elements['fermentation_program'].grid(row=0, column=5)
        self._gui_elements['fermentation_vessel'].grid(row=0, column=6)


class ExtractedRecordsContainer(Tab):
    def __init__(self, tab):
        Tab.__init__(self, tab)
        self.config(borderwidth=4, relief=SOLID)
        self._title = None

    def _create_gui_elements(self):
        if self._content:
            self._create_title()
            for gui_element_name in self._content[0]:
                self._gui_elements[gui_element_name] = ttk.Label(self, text=gui_element_name)

    def _add_text_to_gui_elements(self):
        if self._content:
            for record in self._content:
                for gui_element_name, value in record.items():
                    self._gui_elements[gui_element_name].config(
                        text=self._gui_elements[gui_element_name].cget('text') + '\n' + str(value))

    def _add_gui_elements_to_the_grid(self):
        if self._content:
            for i, gui_element in enumerate(self._gui_elements.values()):
                gui_element.grid(row=1, column=i, sticky=N+W)
            self._title.grid(row=0, column=0, columnspan=self._calculate_columns_quantity())

    def _arrange_rows(self):
        for i in range(1, self._rows_quantity):
            self.rowconfigure(i, weight=1, uniform='row')

    def _arrange_columns(self):
        for i in range(self._columns_quantity):
            self.columnconfigure(i, weight=1)

    def update(self, name, content, special_content):
        self._content = None
        self._special_content = None
        self._name = name
        self._content = content
        self._special_content = special_content
        self._remove_gui_elements()
        self._set_gui()

    def _remove_gui_elements(self):
        for element in self._gui_elements.values():
            element.destroy()
        self._gui_elements.clear()
        if self._title:
            self._title.destroy()

    def _create_title(self):
        self._title = ttk.Label(self, font=(None, 20, 'bold'), text=self._name + ': ' + str(self._special_content))


class ExtractedParametersContainer(ExtractedRecordsContainer):
    def __init__(self, tab):
        ExtractedRecordsContainer.__init__(self, tab)

    def _create_gui_elements(self):
        if self._content:
            self._create_title()
            self._gui_elements['PARAMETER'] = ttk.Label(self, text='PARAMETER')
            self._gui_elements['VALUE'] = ttk.Label(self, text='VALUE')

    def _add_text_to_gui_elements(self):
        if self._content:
            for parameter, value in self._content.items():
                self._gui_elements['PARAMETER'].config(
                    text=self._gui_elements['PARAMETER'].cget('text') + '\n' + str(parameter))
                self._gui_elements['VALUE'].config(text=self._gui_elements['VALUE'].cget('text') + '\n' + str(value))

    def _add_gui_elements_to_the_grid(self):
        if self._content:
            for i, gui_element in enumerate(self._gui_elements.values()):
                gui_element.grid(row=1, column=i, sticky=N+W)
            self._title.grid(row=0, column=0, columnspan=self._calculate_columns_quantity())


class ExtractedRecipeNameContainer(ExtractedRecordsContainer):
    def __init__(self, tab):
        ExtractedRecordsContainer.__init__(self, tab)
        self.config(borderwidth=0, relief=SOLID)

    def _create_gui_elements(self):
        if self._special_content:
            self._create_title()

    def _add_gui_elements_to_the_grid(self):
        if self._special_content:
            self._title.grid(row=0, column=0)

    # def _arrange_rows(self):
    #     for i in range(1, self._rows_quantity):
    #         self.rowconfigure(i, weight=1, uniform='row')
    #
    # def _arrange_columns(self):
    #     for i in range(self._columns_quantity):
    #         self.columnconfigure(i, weight=1)

    def update(self, name, content, special_content):
        self._special_content = None
        self._name = name
        self._content = content
        self._special_content = special_content
        self._remove_gui_elements()
        self._set_gui()

    def _remove_gui_elements(self):
        if self._title:
            self._title.destroy()

    def _create_title(self):
        self._title = ttk.Label(self, font=(None, 20, 'bold'), text=str(self._special_content))
