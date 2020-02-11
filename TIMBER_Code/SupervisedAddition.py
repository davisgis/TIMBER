from tkinter import *
import pickle
from updateTensor import update, view

def supervisedAddition(a):


    root = Tk()

    topFrame = Frame(root)
    #topFrame.pack()
    label1 = Label(root, text = "a[X, ,]")
    label2 = Label(root, text = "a[,X ,]")
    label3 = Label(root, text = "a[, ,]")
    label4 = Label(root, text = "Value")

    entry1 = Entry(root)
    entry2 = Entry(root)
    entry3 = Entry(root)
    entry4 = Entry(root)

    label1.grid(row=0)
    label2.grid(row=1)
    label3.grid(row=2)
    label4.grid(row=3)

    entry1.grid(row=0, column = 1)
    entry2.grid(row=1, column = 1)
    entry3.grid(row=2, column = 1)
    entry4.grid(row=3, column = 1)
    #bottomFrame = Frame(root)
    #bottomFrame.pack(side = BOTTOM)

    button1 = Button(root, text = "Update Tensor", command = lambda: update(a, float(entry1.get()), float(entry2.get()), float(entry3.get()), float(entry4.get())))
    button2 = Button(root, text="View Tensor", command=lambda: view(a, float(entry1.get()), float(entry2.get()), float(entry3.get())))
    button1.grid(row=4, column = 1)
    button2.grid(row=5, column = 1)

    #button1.pack()

    root.mainloop()


    print("Supervised additions complete")