from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk
from recipe_processor import XMLRecipeProcessor
from recipe_monitor import RecipeMonitor
from label_block import TitleBlock, LabelBlock, LabelBlockDict
from queue import Queue


class Tab(ABC, Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self._gui_elements = {}
        self._name = None
        self._content = {}
        self._special_content = None
        self._set = False
        self._visible = False

    def get_name(self):
        return self._name

    def set_content(self, name=None, content=None, special_content=None):
        self._clear_content()
        self._get_content(name, content, special_content)

        if not self._set:
            self._set_gui_elements()
        if not self._visible:
            self._print_gui_on_screen()

        self._process_content()

    def _clear_content(self):
        if self._content:
            self._content = None

    def _get_content(self, name, content, special_content):
        self._name = name
        self._content = content
        self._special_content = special_content

    def _process_content(self):
        pass

    def _set_gui_elements(self):
        self._create_gui_elements()
        self._bind_commands_to_gui_elements()
        self._set = True

    def _print_gui_on_screen(self):
        self._add_gui_elements_to_the_grid()
        self._calculate_rows_quantity()
        self._calculate_columns_quantity()
        self._arrange_rows()
        self._arrange_columns()
        self._visible = True

    @abstractmethod
    def _create_gui_elements(self):
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
        for i in range(1, self._rows_quantity):
            self.rowconfigure(i, weight=1)

    def _arrange_columns(self):
        for i in range(self._columns_quantity):
            self.columnconfigure(i, weight=1, uniform='column')


class RecipeTab(Tab):
    def __init__(self, parent):
        Tab.__init__(self, parent)

        self._name = 'Recipe'
        self.__queue = Queue()
        self.__recipe_detector = RecipeMonitor(XMLRecipeProcessor(), self, self.__queue)

        self._set_gui_elements()

    def _create_gui_elements(self):
        self._gui_elements['USER_SETTINGS'] = UserSettingsContainer(self)
        self._gui_elements['MISCS'] = ExtractedRecordsContainer(self)
        self._gui_elements['FERMENTABLES'] = ExtractedRecordsContainer(self)
        self._gui_elements['MASH_STEPS'] = ExtractedRecordsContainer(self)
        self._gui_elements['HOPS'] = ExtractedRecordsContainer(self)
        self._gui_elements['PARAMETERS'] = ExtractedParametersContainer(self)

    def _add_gui_elements_to_the_grid(self):
        self._gui_elements['USER_SETTINGS'].grid(row=0, column=0, columnspan=3, sticky=N + W + E)
        self._gui_elements['MISCS'].grid(row=1, column=0, sticky=NSEW)
        self._gui_elements['FERMENTABLES'].grid(row=1, column=1, sticky=NSEW)
        self._gui_elements['MASH_STEPS'].grid(row=2, column=0, sticky=NSEW)
        self._gui_elements['HOPS'].grid(row=2, column=1, sticky=NSEW)
        self._gui_elements['PARAMETERS'].grid(row=1, column=2, rowspan=2, sticky=NSEW)

    def _bind_commands_to_gui_elements(self):
        self.bind('<<processed_recipe>>', lambda event: self.set_content())

    def _get_content(self, name, content, special_content):
        self._content = self.__queue.get()
        self._special_content = self.__queue.get()

    def _process_content(self):
        for gui_element_name, gui_element in self._gui_elements.items():
            if gui_element_name in self._content:
                gui_element.set_content(gui_element_name,
                                        self._content[gui_element_name],
                                        self._special_content[gui_element_name],
                                        )


class UserSettingsContainer(Tab):
    def __init__(self, parent):
        Tab.__init__(self, parent)

        self._set_gui_elements()
        self._print_gui_on_screen()

    def _create_gui_elements(self):
        self._gui_elements['yos'] = ttk.Label(self, text='YOS')
        self._gui_elements['mlt_rinse'] = ttk.Label(self, text='MLT rinse')
        self._gui_elements['mlt_cip'] = ttk.Label(self, text='MLT CIP')
        self._gui_elements['bk_rinse'] = ttk.Label(self, text='BK rinse')
        self._gui_elements['bk_cip'] = ttk.Label(self, text='BK CIP')
        self._gui_elements['fermentation_program'] = ttk.Label(self, text='Fermentation program')
        self._gui_elements['fermentation_vessel'] = ttk.Label(self, text='Fermentation vessel')
        self._gui_elements['placeholder'] = ttk.Label(self)
        self._gui_elements['title'] = TitleBlock(self)

    def _add_gui_elements_to_the_grid(self):
        self._gui_elements['yos'].grid(row=1, column=0)
        self._gui_elements['mlt_rinse'].grid(row=1, column=1)
        self._gui_elements['mlt_cip'].grid(row=1, column=2)
        self._gui_elements['bk_rinse'].grid(row=1, column=3)
        self._gui_elements['bk_cip'].grid(row=1, column=4)
        self._gui_elements['fermentation_program'].grid(row=1, column=5)
        self._gui_elements['fermentation_vessel'].grid(row=1, column=6)
        self._gui_elements['placeholder'].grid(row=2)
        self._gui_elements['title'].grid(row=0, columnspan=self._calculate_columns_quantity())

    def _process_content(self):
        self._gui_elements['title'].set_content(special_content=self._special_content)


class ExtractedRecordsContainer(Tab):
    def __init__(self, parent):
        Tab.__init__(self, parent)

        self.config(borderwidth=4, relief=SOLID)

    def _create_gui_elements(self):
        for gui_element_name in self._content[0]:
            self._gui_elements[gui_element_name] = LabelBlock(self)
        self._gui_elements['title'] = TitleBlock(self)

    def _add_gui_elements_to_the_grid(self):
        for i, (gui_element_name, gui_element) in enumerate(self._gui_elements.items()):
            if not gui_element_name == 'title':
                gui_element.grid(row=1, column=i, sticky=N+W)

        self._gui_elements['title'].grid(row=0, columnspan=self._calculate_columns_quantity())

    def _arrange_columns(self):
        for i in range(self._columns_quantity):
            self.columnconfigure(i, weight=1)

    def _process_content(self):
        self._gui_elements['title'].set_content(name=self._name, special_content=self._special_content)

        for gui_element_name, gui_element in self._gui_elements.items():
            gui_element.set_content(name=gui_element_name, content=self._content)


class ExtractedParametersContainer(ExtractedRecordsContainer):
    def __init__(self, parent):
        ExtractedRecordsContainer.__init__(self, parent)

    def _create_gui_elements(self):
        self._gui_elements['PARAMETER'] = LabelBlockDict(self)
        self._gui_elements['VALUE'] = LabelBlockDict(self)
        self._gui_elements['title'] = TitleBlock(self)
