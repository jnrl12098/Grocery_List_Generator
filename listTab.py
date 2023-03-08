from tkinter import *
from tkinter import ttk
from searchWindow import SearchWindow
from abc import ABC, abstractmethod
from utilities import *
import time

recipeName = ""
recipeIngredients = []

class ListTab(Frame):

    listName = ""
    items = []
    
    def __init__(self):
        super().__init__()
        # WIDGETS
        self.listLabel = Label(self, width = 30, text = self.listName)
        self.entrybox = Entry(self, width = 30)
        self.listbox = Listbox(self, width = 30, height = 20)
        self.searchButton = Button(self, text = "Search for a recipe", command = self.createSearchWindowFunction)
        self.editItemButton = Button(self, text = "Edit Item", command = self.editItem)
        self.insertItemButton = Button(self, text = "Insert Item", command = self.insertItem)
        self.deleteItemButton = Button(self, text = "Remove Item", command = self.deleteItem)
        self.clearSelectionButton = Button(self, text = "Clear Selection", command = self.clearListboxSelection)
        self.exportButton = Button(self, text = "", command = self.exportList)

        # WIDGET LOCATIONS
        self.listLabel.grid(row = 0, column = 0)
        self.entrybox.grid(row = 1, column = 0)
        self.listbox.grid(row = 2, column = 0, rowspan = 20)
        self.searchButton.grid(row = 1, column = 1)
        self.editItemButton.grid(row = 2, column = 1)
        self.insertItemButton.grid(row = 3, column = 1)
        self.deleteItemButton.grid(row = 4, column = 1)
        self.clearSelectionButton.grid(row = 5, column = 1)
        self.exportButton.grid(row = 21, column = 1)
        
        # KEYBOARD SHORTCUTS
        self.entrybox.bind("<Return>", lambda event: self.insertItem())
        self.entrybox.bind("<Control-Return>", lambda event: self.editItem())
        self.entrybox.bind("<Control-BackSpace>", lambda event: self.entrybox.delete(0, END))
        self.listbox.bind("<BackSpace>", self.backspaceKeyListbox)
        self.listbox.bind("<Delete>", self.deleteKeyListbox)
        self.listbox.bind("<Control-Return>", self.bringToEntrybox)
        self.listbox.bind("<Alt-Return>", lambda event: self.entrybox.focus_set())
        # TODO figure out how to bind events to the frame!
        self.bind("<Escape>", lambda event: self.clearListboxSelection())
        self.bind("<Control-S>", lambda event: self.exportList())

    def editItem(self):
        if len(self.listbox.curselection()) == 1:
            current = self.listbox.curselection()   # note: this is a tuple
            self.items.remove(self.listbox.get(current))
            self.items.insert(current[0], self.entrybox.get())
            self.listbox.delete(current)
            self.listbox.insert(current, self.entrybox.get())
            self.listbox.select_clear(current)
            self.entrybox.delete(0, END)
        else:
            pass

    def insertItem(self):
        if len(self.listbox.curselection()) == 1:
            # insert the input BELOW the highlighted item, 
            # then transfer the highlight to the input
            belowCurselection = self.listbox.curselection()[0] + 1
            if belowCurselection == self.listbox.size():
                self.items.append(self.entrybox.get())
            else:
                self.items.insert(belowCurselection, self.entrybox.get())
            self.listbox.insert(belowCurselection, self.entrybox.get())
            self.listbox.selection_clear(belowCurselection - 1)
            self.listbox.select_set(belowCurselection)
        else:
            self.items.append(self.entrybox.get())
            self.listbox.insert(END, self.entrybox.get())
        self.entrybox.delete(0, END)

    def deleteItem(self):
        if len(self.listbox.curselection()) == 1:
            self.items.pop(self.listbox.curselection()[0])
            self.listbox.delete(self.listbox.curselection())
        else:
            pass

    def clearListboxSelection(self):
        if len(self.listbox.curselection()) == 1:
            self.listbox.select_clear(self.listbox.curselection())
        else:
            pass

    def backspaceKeyListbox(self, event):
        if len(self.listbox.curselection()) == 1:
            current = self.listbox.curselection()[0]
            self.deleteItem()
            # highlight backward
            if current == 0:
                self.listbox.select_set(0)
            else:
                self.listbox.select_set(current - 1)
        else:
            pass

    def deleteKeyListbox(self, event):
        if len(self.listbox.curselection()) == 1:
            current = self.listbox.curselection()[0]
            self.deleteItem()
            # highlight forward
            if current == self.listbox.size():
                self.listbox.select_set(END)
            else:
                self.listbox.select_set(current)
        else:
            pass

    def bringToEntrybox(self, event):
        self.entrybox.delete(0, END)
        self.entrybox.insert(0, self.listbox.get(self.listbox.curselection()))
        self.entrybox.focus_set()

    @abstractmethod
    def createSearchWindowFunction(self):
        pass

    @abstractmethod
    def exportList(self):
        pass
        
class GroceryListTab(ListTab):

    recipeTab = None
    
    def __init__(self, notebook):
        super().__init__()
        self.listName = "Grocery List"
        self.listLabel.configure(text = self.listName)
        self.exportButton.configure(text = "Export Grocery List")

    def createSearchWindowFunction(self):
        self.recipeTab.searchButton.invoke()

    def exportList(self):
        dateToday = time.strftime("%Y-%m-%d", time.localtime())
        fileName = self.listName+ " " + dateToday + ".txt"
        with open(fileName, "w") as file:
            for i in self.items:
                file.write(i + "\n")
        print("Grocery List has been exported to \"" + fileName + "\"")

class InventoryTab(ListTab):
    
    recipeTab = None

    def __init__(self, notebook):
        super().__init__()
        self.listName = "Inventory"
        self.listLabel.configure(text = self.listName)
        self.exportButton.configure(text = "Update Inventory")

    def createSearchWindowFunction(self):
        self.recipeTab.searchButton.invoke()

    def exportList(self):
        fileName = "Inventory.txt"
        with open(fileName, "w") as file:
            for i in inventoryList:
                file.write(i + "\n")
        print("The Inventory List Text File has been updated.")

class RecipeTab(ListTab):

    inventoryTab = None
    groceryListTab = None
    
    def __init__(self, notebook):
        super().__init__()
        self.listName = "Custom Recipe"
        self.listLabel.configure(text = self.listName)
        self.exportButton.configure(text = "Save Recipe")

        self.addRecipeToGroceryListButton = Button(self, text = "Recipe => Grocery List", command = self.addRecipeToGroceryList)

        self.addRecipeToGroceryListButton.grid(row = 7, column = 1)

    def createSearchWindowFunction(self):
        if SearchWindow.inactive:
            self.searchWindow = SearchWindow(getRecipeFunction = self.getRecipe)
            self.searchWindow.focus_set()
        else:
            self.searchWindow.focus_set()

    def getRecipe(self, chosenRecipeName, chosenrecipeIngredients):
        self.listName = chosenRecipeName
        self.items.clear()
        for i in chosenrecipeIngredients:
            self.items.append(i)
        refreshListbox(self.items, self.listbox)
        self.listLabel.configure(text = self.listName)
        notebook.select(2)  # hard-coded; recipeTab will always be 3rd tab
        self.focus_set()

    def exportList(self):
        dateToday = time.strftime("%Y-%m-%d", time.localtime())
        if len(self.entrybox.get()) == 0:
            self.entrybox.insert(0, "Enter recipe name here")
        else:
            fileName = self.entrybox.get() + " " + dateToday + ".txt"
            with open("Recipes\\" + fileName, "w") as file:
                for i in self.items:
                    file.write(i + "\n")
            print("This recipe has been exported to \"Recipes/" + fileName + "\"")

    def addRecipeToGroceryList(self):
        for i in self.items:
            if (i not in self.groceryListTab.items) and (i not in self.inventoryTab.items):
                self.groceryListTab.items.append(i)
        refreshListbox(self.groceryListTab.items, self.groceryListTab.listbox)
        notebook.select(1)

# def createSearchWindow():
#     if SearchWindow.inactive:
#         searchWindow = SearchWindow(getRecipeFunction = getRecipe)
#         searchWindow.focus_set()

# def getRecipe(chosenRecipeName, chosenrecipeIngredients):
#     global recipeName, recipeIngredients
#     recipeName = chosenRecipeName
#     recipeIngredients.clear()
#     for i in chosenrecipeIngredients:
#         recipeIngredients.append(i)
#     # decided to use global variables instead of needing to call recipe details from each frame

def editTabItems(tab, items):
    tab.items.clear()
    for i in items:
        tab.items.append(i)
    refreshListbox(tab.items, tab.listbox)

# MAIN FUNCTION
mainWindow = Tk()

notebook = ttk.Notebook(mainWindow)

# inventoryTab = ListTab(notebook, createSearchWindow)
# groceryListTab = ListTab(notebook, createSearchWindow)
# recipeTab = ListTab(notebook, createSearchWindow)

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

# initialize the inventoryTab
inventoryList = []
fileAsList("Inventory.txt", inventoryList)
editTabItems(inventoryTab, inventoryList)

mainWindow.mainloop()