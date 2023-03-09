from listTab import GroceryListTab, InventoryTab, RecipeTab
from tkinter import *
from tkinter import ttk
from utilities import *

def editTabItems(tab, items):
    tab.items.clear()
    for i in items:
        tab.items.append(i)
    refreshListbox(tab.items, tab.listbox)

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

mainWindow.mainloop()