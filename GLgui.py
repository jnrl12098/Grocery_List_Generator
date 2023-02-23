from tkinter import *

mainWindow = Tk()

mode = 4

"""
modes:
1 - Edit Grocery List 
2 - Search Recipe
3 - Edit Recipe
4 - Edit Inventory List
"""

midList = []        # this list will act as the middle-man between the listbox and the other lists

groceryList = ["GL 1", "GL 2", "GL 3"]   # build the grocery list from scratch, append one recipe at a time
inventoryList = ["IL 1", "IL 2", "IL 3"]   # used to contain list of ingredients in inventory from text file
dummyRecipe = ["Ing 1", "Ing 2", "Ing 3"]
recipeName = ""

# TODO if changes to the inventory list was made, the user must be prompted to save before fully exiting the app
# TODO during the Search Recipe Mode, user should be prompted before confirming choices
    # choices: "Choose Recipe" "Add Recipe to Grocery List"
# TODO export function, specific to the mode
    # M1: "Export Grocery List"
    # M2: disabled
    # M3: "Export Recipe" - useful if the user likes to save these changes or make a new recipe
    # M4: "Update Inventory"

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

def insItem():
    # only one item should be selected and entrybox is not empty
    global midList
    if (len(listbox.curselection()) == 1) & (len(entrybox.get()) != 0):
        current = listbox.curselection()    # note this is a tuple containing indices
        midList.insert(current[0], entrybox.get())
        listbox.insert(current, entrybox.get())
        listbox.select_clear(0, current)
        entrybox.delete(0, END) 
    else:
        pass

def addItem():
    # add the current text in the entrybox to the bottom of the list and the listbox
    global midList
    if len(entrybox.get()) != 0:
        midList.append(entrybox.get())
        listbox.insert(END, entrybox.get())
        entrybox.delete(0, END)
    else:
        pass

def delItem():    
    # removes the selected item from the list and the listbox
    global midList
    if len(listbox.curselection()) == 1:
        midList.remove(listbox.get(listbox.curselection()))
        listbox.delete(listbox.curselection())
    else:
        pass

def refreshListbox():
    global midList
    listbox.delete(0, END)
    for i in range(len(midList)):
        listbox.insert(i, midList[i])

def switchToGL():
    global mode, midList, groceryList
    if mode == 1:
        pass
    else:
        mode = 1
        midList = groceryList
        refreshListbox()
        modeLabel.config(text = "Mode: Edit Grocery List")
        listLabel.config(text = "Grocery List")

def switchToIL():
    global mode, midList, inventoryList
    if mode == 4:
        pass
    else:
        mode = 4
        midList = inventoryList
        refreshListbox()
        modeLabel.config(text = "Mode: Edit Inventory List")
        listLabel.config(text = "Inventory List")

def switchToRecipe():
    global mode, midList, dummyRecipe, recipeName
    if mode == 3:
        pass
    else:
        mode = 3
        midList = dummyRecipe
        refreshListbox()
        modeLabel.config(text = "Mode: Edit Recipe")
        listLabel.config(text = "Recipe: " + recipeName)

# WIDGETS
# displays the current mode
modeLabel = Label(mainWindow, width = 30, justify = "left")
modeLabel.grid(row = 0, column = 0)

entrybox = Entry(mainWindow, width = 30)
entrybox.grid(row = 1, column = 0)

listLabel = Label(mainWindow, width = 30, justify = "left")
listLabel.grid(row = 2, column = 0)

listbox = Listbox(mainWindow, width = 30)
listbox.grid(row = 3, column = 0, rowspan = 9)

editItem_button = Button(mainWindow, text = "Edit Item", command = editItem)
editItem_button.grid(row = 3, column = 1)

insItem_button = Button(mainWindow, text = "Insert Item", command = insItem)
insItem_button.grid(row = 4, column = 1)

addItem_button = Button(mainWindow, text = "Add Item", command = addItem)
addItem_button.grid(row = 5, column = 1)

delItem_button = Button(mainWindow, text = "Remove Item", command = delItem)
delItem_button.grid(row = 6, column = 1)

editGL_button = Button(mainWindow, text = "Edit Grocery List", command = switchToGL)
editGL_button.grid(row = 8, column = 1)

editIL_button = Button(mainWindow, text = "Edit Inventory List", command = switchToIL)
editIL_button.grid(row = 9, column = 1)

editRecipe_button = Button(mainWindow, text = "Edit Current Recipe", command = switchToRecipe)
editRecipe_button.grid(row = 10, column = 1)

# initialize midList as the inventoryList to minimize re-edits to the inventory
mode = 4
midList = inventoryList
refreshListbox()
modeLabel.config(text = "Mode: Edit Inventory List")
listLabel.config(text = "Inventory List")
recipeName = "Custom Recipe"

mainWindow.mainloop()