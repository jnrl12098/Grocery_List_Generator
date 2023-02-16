from tkinter import *

mainWindow = Tk()

mode = 1

midList = []        # this list will act as the middle-man between the listbox and the other lists

groceryList = ["GL 1", "GL 2", "GL 3"]   # build the grocery list from scratch, append one recipe at a time
storageList = ["IL 1", "IL 2", "IL 3"]   # used to contain list of ingredients in inventory from text file

# FUNCTIONS
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
    else:
        pass

def addItem():
    # add the current text in the entrybox to the bottom of the list
    global midList
    if len(entrybox.get()) != 0:
        midList.append(entrybox.get())
        listbox.insert(END, entrybox.get())
        entrybox.delete(0, END)
    else:
        pass

def delItem():    
    # removes the selected item from listbox
    global midList
    if len(listbox.curselection()) == 1:
        midList.remove(listbox.get(listbox.curselection()))
        listbox.delete(listbox.curselection())
    else:
        pass

def switchToGL():
    # print("You pressed the Edit Grocery List Button")
    global mode, midList, groceryList
    if mode == 1:
        print("You're still in Grocery List Mode")
        pass
    else:
        prevMode = mode
        mode = 1
        print("Switched to Grocery List Mode", end = " ")
        if prevMode == 4:
            # TODO update the grocery after the inventory was changed
            # keep an internal unfiltered grocery list; only the filtered list is shown and exported
            print("from Inventory Mode")
            midList = groceryList
            refreshListbox()

def switchToIL():
    # print("You pressed the Edit Inventory List Button")
    global mode, midList, storageList
    if mode == 4:
        print("You're still in Inventory List Mode")
        pass
    else:
        prevMode = mode
        mode = 4
        print("Switched to Inventory List Mode", end = " ")
        if prevMode == 1:
            print("from Grocery List Mode")
            midList = storageList
            refreshListbox()

def updateList():
    global midList
    print("---------------")
    for i in midList:
        print(i)

def refreshListbox():
    global midList
    listbox.delete(0, END)
    for i in range(len(midList)):
        listbox.insert(i, midList[i])

# WIDGETS
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

editGL_button = Button(mainWindow, text = "Edit Grocery List", command = switchToGL)
editGL_button.grid(row = 7, column = 1)

editIL_button = Button(mainWindow, text = "Edit Inventory List", command = switchToIL)
editIL_button.grid(row = 8, column = 1)

# initialize midList as the groceryList
midList = groceryList
refreshListbox()

mainWindow.mainloop()