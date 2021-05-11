from tkinter import *


def destroy(event):
    el = event.widget
    print(buttons)
    el.destroy()
    print(buttons)

def create(event):
    for button in buttons:
        button.grid()


root = Tk()
b1 = Button(root, text='b1')
b2 = Button(root, text='b2')
b3 = Button(root, text='b3')

buttons = [b1, b2, ]

b1.bind('<Button-1>', lambda event: destroy(event))
b2.bind('<Button-1>', lambda event: destroy(event))
b3.bind('<Button-1>', create)

b1.grid()
b2.grid()
b3.grid()

root.mainloop()
