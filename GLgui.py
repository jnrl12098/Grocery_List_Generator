from tkinter import *
from tkinter import messagebox
import os, time
from utilities import *
from searchWindow import SearchWindow

mainWindow = Tk()

mode = 0
midList = []        # this list will act as the middle-man between the listbox and the other lists
groceryList = []   # build the grocery list from scratch, append one recipe at a time
inventoryList = []   # used to contain list of ingredients in inventory from text file
dummyRecipe = []
recipeName = ""
narrowedList = []
recipesList = []

# FUNCTIONS
def editItem():
    # only one item should be selected and entrybox is not empty
    global midList
    if (len(listbox.curselection()) == 1):
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
    if (len(listbox.curselection()) == 1):
        belowCurselection = listbox.curselection()[0] + 1    
        if belowCurselection == listbox.size():
            midList.append(entrybox.get())
        else:
            midList.insert(belowCurselection, entrybox.get())
        listbox.insert(belowCurselection, entrybox.get())
        listbox.selection_clear(belowCurselection - 1)
        listbox.select_set(belowCurselection)
        entrybox.delete(0, END) 
    else:
        pass

def addItem():
    # add the current text in the entrybox to the bottom of the list and the listbox
    global midList
    midList.append(entrybox.get())
    listbox.insert(END, entrybox.get())
    entrybox.delete(0, END)

def delItem():    
    # removes the selected item from the list and the listbox
    global midList
    if len(listbox.curselection()) == 1:
        midList.pop(listbox.curselection()[0])
        listbox.delete(listbox.curselection())
    else:
        pass

def backspaceListbox(event):
    if len(listbox.curselection()) == 0:
        pass
    else:
        current = listbox.curselection()[0]
        delItem()
        if current == 0:
            listbox.select_set(0)
        else:
            listbox.select_set(current - 1)

def deleteListbox(event):
    if len(listbox.curselection()) == 0:
        pass
    else:
        current = listbox.curselection()[0]
        delItem()
        if current == listbox.size():
            listbox.select_set(END)
        else:
            listbox.select_set(current)

def clearListboxSelection():
    if len(listbox.curselection()) == 1: 
        listbox.select_clear(listbox.curselection())
    else:
        pass

def bringToEntrybox(event):
    entrybox.delete(0, END)
    entrybox.insert(0, listbox.get(listbox.curselection()))
    entrybox.focus_set()

# switch to Grocery List (GL) mode
def switchToGroceryList():
    global mode, midList, groceryList
    if mode == 1:
        pass
    else:
        if mode == 3:
            # reset the Context Button
            contextButton.configure(text = "Search For A Recipe", command = createSearchWindow)
        mode = 1
        midList = groceryList
        refreshListbox(midList, listbox)
        modeLabel.config(text = "Mode: Edit Grocery List")
        listLabel.config(text = "Grocery List")
        exportButton.config(text = "Export Grocery List")

# switch to Inventory List (IL) mode
def switchToInventoryList():
    global mode, midList, inventoryList
    if mode == 4:
        pass
    else:
        if mode == 3:
            # reset the Context Button
            contextButton.configure(text = "Search For A Recipe", command = createSearchWindow)
        mode = 4
        midList = inventoryList
        refreshListbox(midList, listbox)
        modeLabel.config(text = "Mode: Edit Inventory List")
        listLabel.config(text = "Inventory List")
        exportButton.config(text = "Update Inventory List")

# switch to Edit (Current) Recipe mode
def switchToEditRecipe():
    global mode, midList, dummyRecipe, recipeName
    if mode == 3:
        pass
    else:
        mode = 3
        midList = dummyRecipe
        refreshListbox(midList, listbox)
        modeLabel.config(text = "Mode: Edit Recipe")
        listLabel.config(text = "Recipe: " + recipeName)
        exportButton.config(text = "Save this Recipe")

def createSearchWindow():
    if SearchWindow.inactive:
        searchWindow = SearchWindow(getRecipe)
        searchWindow.focus_set()

def contextM2List(event):
    global mode, narrowedList
    if mode == 3:
        contextButton.config(text = "Recipe => GL", command = addRecipeToGroceryList)
        # note, for now this will not let the user search for a recipe during edit reecipe mode
    else:
        pass

def getRecipe(chosenRecipeName, chosenIngredientsList):
    global recipeName, dummyRecipe
    recipeName = chosenRecipeName
    dummyRecipe.clear()
    for i in chosenIngredientsList:
        dummyRecipe.append(i)
    switchToEditRecipe()
    contextButton.config(text = "Recipe => GL", command = addRecipeToGroceryList)
    entrybox.delete(0, END)
    mainWindow.focus_set()

def addRecipeToGroceryList():
    global mode, midList, dummyRecipe, groceryList, inventoryList
    # transfer contents of dummyRecipe to groceryList but filtered from inventoryList and current groceryList
    for i in dummyRecipe:
        if (i not in groceryList) and (i not in inventoryList):
            groceryList.append(i)
    switchToGroceryList()
    entrybox.delete(0, END)

def exportList():
    # TODO implement a message box to confirm export choices
    global mode, groceryList, inventoryList, dummyRecipe
    dateToday = time.strftime("%Y-%m-%d", time.localtime())
    fileName = ""
    if mode == 1:
        fileName = "Grocery List " + dateToday + ".txt"
        with open(fileName, "w") as file:
            for i in groceryList:
                file.write(i + "\n")
        print("Grocery List has been exported to \"" + fileName + "\"")
    elif mode == 3:
        if len(entrybox.get()) == 0:
            entrybox.insert(0, "Enter recipe name here")
        else:
            fileName = entrybox.get() + " " + dateToday + ".txt"
            with open("Recipes\\" + fileName, "w") as file:
                for i in dummyRecipe:
                    file.write(i + "\n")
            print("This recipe has been exported to \"Recipes/" + fileName + "\"")
    elif mode == 4:
        fileName = "Inventory.txt"
        with open(fileName, "w") as file:
            for i in inventoryList:
                file.write(i + "\n")
        print("The Inventory List Text File has been updated.")
    else:
        pass

def checkInventoryListOnClose():
    global inventoryList
    oldInventoryList = []
    areDifferent = False
    # side effect: if the user has already saved right before exiting, the two lists are automatically the same
    fileAsList("Inventory.txt", oldInventoryList) 
    # compare oldInventoryList and inventoryList; consider unchanged if and only if: same size, same order, same items
    if len(inventoryList) == len(oldInventoryList):
        for i in range(len(inventoryList)):
            if inventoryList[i] != oldInventoryList[i]:
                areDifferent = True
                break
    else:
        areDifferent = True
    
    if areDifferent == True:
        response = messagebox.askyesno("Warning!", "You have made changes to the Inventory List.\nDo you want to save these changes before exiting?")
        if response:
            fileName = "Inventory.txt"
            with open(fileName, "w") as file:
                for i in inventoryList:
                    file.write(i + "\n")
            messagebox.showinfo("File Saved", "The changes have been saved.")
            mainWindow.destroy()
        else:
            mainWindow.destroy()
    else:
        mainWindow.destroy()

# WIDGETS
# displays the current mode
modeLabel = Label(mainWindow, width = 30, justify = "left")
modeLabel.grid(row = 0, column = 0)

entrybox = Entry(mainWindow, width = 30)
entrybox.grid(row = 1, column = 0)

listLabel = Label(mainWindow, width = 30, justify = "left")
listLabel.grid(row = 2, column = 0)

listbox = Listbox(mainWindow, width = 30, height = 20)
listbox.grid(row = 3, column = 0, rowspan = 20)

editItem_button = Button(mainWindow, text = "Edit Item", command = editItem)
editItem_button.grid(row = 3, column = 1)

insItem_button = Button(mainWindow, text = "Insert Item", command = insItem)
insItem_button.grid(row = 4, column = 1)

addItem_button = Button(mainWindow, text = "Add Item", command = addItem)
addItem_button.grid(row = 5, column = 1)

delItem_button = Button(mainWindow, text = "Remove Item", command = delItem)
delItem_button.grid(row = 6, column = 1)

editGL_button = Button(mainWindow, text = "Edit Grocery List", command = switchToGroceryList)
editGL_button.grid(row = 9, column = 1)

editIL_button = Button(mainWindow, text = "Edit Inventory List", command = switchToInventoryList)
editIL_button.grid(row = 10, column = 1)

editRecipe_button = Button(mainWindow, text = "Edit Current Recipe", command = switchToEditRecipe)
editRecipe_button.grid(row = 11, column = 1)

contextButton = Button(mainWindow, text = "Search For A Recipe", command = createSearchWindow)
contextButton.grid(row = 1, column = 1)

exportButton = Button(mainWindow, text = "Update Inventory List", command = exportList)
exportButton.grid(row = 13, column = 1)

clearSelectionButton = Button(mainWindow, text = "Clear Selection", command = clearListboxSelection)
clearSelectionButton.grid(row = 7, column = 1)

# MOUSE AND KEYBOARD BINDS
listbox.bind("<Button-1>", contextM2List)

entrybox.bind("<Return>", lambda event: addItem() if (len(listbox.curselection()) == 0) else insItem())
entrybox.bind("<Control-Return>", lambda event: editItem())
entrybox.bind("<Control-BackSpace>", lambda event: entrybox.delete(0, END))
listbox.bind("<BackSpace>", backspaceListbox)
listbox.bind("<Delete>", deleteListbox)
listbox.bind("<Control-Return>", bringToEntrybox)
mainWindow.bind("<Escape>", lambda event: clearListboxSelection())

# MAIN FUNCTION
# initialize whole list of available pre-built recipes
recipesFolder = os.scandir("Recipes\\")
for recipe in recipesFolder:
    if recipe.is_file():
        recipesList.append(recipe.name[slice(0,-4)])   # remove ".txt"

# initialize the inventory list
fileAsList("Inventory.txt", inventoryList)

# initialize the app with Inventory List Mode to minimize re-edits to the inventory
mode = 4
midList = inventoryList
refreshListbox(midList, listbox)
modeLabel.config(text = "Mode: Edit Inventory List")
listLabel.config(text = "Inventory List")
recipeName = "Custom Recipe" 

mainWindow.protocol("WM_DELETE_WINDOW", checkInventoryListOnClose)

mainWindow.mainloop()