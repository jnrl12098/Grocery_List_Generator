from tkinter import *

mainWindow = Tk()

midList = []        # this list will act as the middle-man between the listbox and the other lists


def editItem():
    # only one item should be selected and entrybox is not empty
    global midList
    if (len(listbox.curselection()) == 1) & (len(entrybox.get()) != 0):
        current = listbox.curselection()    # note this is a tuple containing indices
        midList.remove(listbox.get(current))
        midList.insert(current[0], entrybox.get())
        listbox.delete(current)
        listbox.insert(current, entrybox.get())
        listbox.select_clear(0, current)
        entrybox.delete(0, END)        
        updateList()
    else:
        pass

def addItem():
    # add the current text in the entrybox to the bottom of the list
    global midList
    if len(entrybox.get()) != 0:
        midList.append(entrybox.get())
        listbox.insert(END, entrybox.get())
        entrybox.delete(0, END)
        updateList()
    else:
        pass

def delItem():    
    # removes the selected item from listbox
    global midList
    if len(listbox.curselection()) == 1:
        midList.remove(listbox.get(listbox.curselection()))
        listbox.delete(listbox.curselection())
        updateList()
    else:
        pass

def updateList():
    global midList
    print("---------------")
    for i in midList:
        print(i)

# displays the current mode
modeLabel = Label(mainWindow, width = 30, text = "Mode: Label", justify = "left")
modeLabel.grid(row = 0, column = 0)

entrybox = Entry(mainWindow, width = 30)
entrybox.grid(row = 1, column = 0)

listLabel = Label(mainWindow, width = 30, text = "List Label", justify = "left")
listLabel.grid(row = 2, column = 0)

listbox = Listbox(mainWindow, width = 30)
listbox.grid(row = 3, column = 0, rowspan = 9)

# edits the selected item in the listbox into the text on the entrybox
editItem_button = Button(mainWindow, text = "Edit Item", command = editItem)
editItem_button.grid(row = 3, column = 1)

# adds the current text on the entrybox to the bottom of the list
addItem_button = Button(mainWindow, text = "Add Item", command = addItem)
addItem_button.grid(row = 4, column = 1)

# removes the selected item/s from the listbox
delItem_button = Button(mainWindow, text = "Remove Item", command = delItem)
delItem_button.grid(row = 5, column = 1)

mainWindow.mainloop()