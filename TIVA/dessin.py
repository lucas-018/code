from math import *
from tkinter import *


fenetre = Tk()
label = Label(fenetre, text = "Dessin")
label.pack()
canvas = Canvas(fenetre, width=150, height=120, background='white')
ligne1 = canvas.create_line(30, 10, 30, 100)
ligne2 = canvas.create_line(30, 100, 100, 100)
canvas.pack()


fenetre.mainloop()

