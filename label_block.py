from tkinter import ttk


class LabelBlock(ttk.Label):
    def __init__(self, parent):
        ttk.Label.__init__(self, parent)

    def set_content(self, name=None, content=None, special_content=None):
        self.config(text=name)

        for record in content:
            self.config(text=self.cget('text') + '\n' + str(record[name]))


class LabelBlockDict(LabelBlock):
    def __init__(self, parent):
        LabelBlock.__init__(self, parent)

    def set_content(self, name=None, content=None, special_content=None):
        self.config(text=name)

        if name == 'PARAMETER':
            for parameter_name in content:
                self.config(text=self.cget('text') + '\n' + str(parameter_name))
        elif name == 'VALUE':
            for parameter_value in content.values():
                self.config(text=self.cget('text') + '\n' + str(parameter_value))


class TitleBlock(LabelBlock):
    def __init__(self, parent):
        LabelBlock.__init__(self, parent)

        self.config(font=(None, 20, 'bold'))

    def set_content(self, name=None, content=None, special_content=None):
        if name and special_content:
            self.config(text=str(name) + ': ' + str(special_content))
        elif special_content:
            self.config(text=special_content)
