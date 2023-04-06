from listTab import GroceryListTab, InventoryTab, RecipeTab
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from utilities import *

def editTabItems(tab, items):
    tab.items.clear()
    for i in items:
        tab.items.append(i)
    refreshListbox(tab.items, tab.listbox)

def checkInventoryListOnClose(inventoryTab):
    oldInventory = []
    areDifferent = False
    # side effect: if the user has already saved right before exiting, all the checks below will return areDifferent = False
    fileAsList("Inventory.txt", oldInventory) 
    # compare oldInventoryList and inventoryList; 
    # consider unchanged if and only if: same size, same order, same items
    if len(inventoryTab.items) == len(oldInventory):
        for i in range(len(inventoryTab.items)):
            if inventoryTab.items[i] != oldInventory[i]:
                areDifferent = True
                break
    else:
        areDifferent = True
    
    if areDifferent == True:
        response = messagebox.askyesno("Warning!", "You have made changes to the Inventory List.\nDo you want to save these changes before exiting?")
        if response:
            inventoryTab.exportList()
            messagebox.showinfo("File Saved", "The changes have been saved.")

    mainWindow.destroy()

# MAIN FUNCTION
mainWindow = Tk()

notebook = ttk.Notebook(mainWindow)

recipeTab = RecipeTab(notebook)
inventoryTab = InventoryTab(notebook)
groceryListTab = GroceryListTab(notebook)

recipeTab.inventoryTab = inventoryTab
recipeTab.groceryListTab = groceryListTab
inventoryTab.recipeTab = recipeTab
groceryListTab.recipeTab = recipeTab

notebook.add(inventoryTab, text = "Inventory List")
notebook.add(groceryListTab, text = "Grocery List")
notebook.add(recipeTab, text = "Recipe")
notebook.pack(expand = True, fill = "both")

notebook.enable_traversal()
mainWindow.bind("<Alt-KeyPress-1>", lambda event: notebook.select(0))
mainWindow.bind("<Alt-KeyPress-2>", lambda event: notebook.select(1))
mainWindow.bind("<Alt-KeyPress-3>", lambda event: notebook.select(2))

# initialize the inventoryTab
inventoryList = []
fileAsList("Inventory.txt", inventoryList)
editTabItems(inventoryTab, inventoryList)

mainWindow.protocol("WM_DELETE_WINDOW", lambda: checkInventoryListOnClose(inventoryTab))

mainWindow.mainloop()