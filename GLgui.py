from tkinter import *

mainWindow = Tk()

midList = [] # this list will act as the middle-man between the listbox and the other lists

def editItem():
    # only one item should be selected and entrybox is not empty
    if (len(listbox.curselection()) == 1) & (len(entrybox.get()) != 0):
        current = listbox.curselection()
        listbox.delete(current)
        listbox.insert(current, entrybox.get())
        listbox.select_clear(0, current)
        entrybox.delete(0, END)        
        # TODO update the current list with the contents of the listbox
        updateList()
    else:
        pass

def addItem():
    # add the current text in the entrybox to the bottom of the list
    if len(entrybox.get()) != 0:
        listbox.insert(END, entrybox.get())
        entrybox.delete(0, END)
        print(listbox.size())
        # TODO update the current list with the contents of the listbox
        updateList()
    else:
        pass

def delItem():    
    # removes the selected item from listbox
    if len(listbox.curselection()) == 1:
        listbox.delete(listbox.curselection())
        # TODO update the current list with the contents of the listbox
        updateList()
    else:
        pass

def updateList():
    global midList
    # this method with O(n) complexity will clear and rebuild the entire list each time edit/add/del is clicked
    # TODO replace with O(1) complexity where it's more specific to each button press
    midList.clear()
    for i in range(listbox.size()):
        midList.append(listbox.get(i))
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
listbox.grid(row = 3, column = 0, rowspan = 7)

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