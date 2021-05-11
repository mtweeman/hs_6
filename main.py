from application_window import ApplicationWindow
from application_theme import ApplicationTheme
from tab_bar import TabBar


window = ApplicationWindow()
tab_bar = TabBar(window)
theme = ApplicationTheme()

window.mainloop()
