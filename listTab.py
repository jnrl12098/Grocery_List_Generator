from tkinter import *
from tkinter import filedialog, messagebox
# from tkinter import ttk
from searchWindow import SearchWindow
from abc import ABC, abstractmethod
from utilities import *
import time

class ListTab(Frame, ABC):

    def __init__(self):
        super().__init__()
        # WIDGETS
        self.listName = ""
        self.items = []
        self.oldItems = []
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
        # TODO figure out how to bind events to the frame itself!
        self.entrybox.bind("<Escape>", lambda event: self.clearListboxSelection())
        self.listbox.bind("<Escape>", lambda event: self.clearListboxSelection())
        self.entrybox.bind("<Control-s>", lambda event: self.exportList())
        self.listbox.bind("<Control-s>", lambda event: self.exportList())
        self.entrybox.bind("<Control-f>", lambda event: self.createSearchWindowFunction())
        self.listbox.bind("<Control-f>", lambda event: self.createSearchWindowFunction())
        self.entrybox.bind("<Control-z>", self.undo)
        self.listbox.bind("<Control-z>", self.undo)

    def undo(self, event):
        bufferList = []
        copyList(self.items, bufferList)
        copyList(self.oldItems, self.items)
        copyList(bufferList, self.oldItems)
        refreshListbox(self.items, self.listbox)

    def editItem(self):
        if len(self.listbox.curselection()) == 1:
            copyList(self.items, self.oldItems)
            item = self.entrybox.get()
            self.entrybox.delete(0, END)
            current = self.listbox.curselection()   # note: this is a tuple
            self.items.pop(current[0])
            self.items.insert(current[0], item)
            self.listbox.delete(current)
            self.listbox.insert(current, item)
            self.listbox.select_clear(current)
        else:
            pass

    def insertItem(self):
        copyList(self.items, self.oldItems)
        item = self.entrybox.get()
        if len(self.listbox.curselection()) == 1:
            # insert the new item ABOVE the highlighted item, then transfer the highlight to the new item
            curselection = self.listbox.curselection()[0]
            belowCurselection = curselection + 1
            # if belowCurselection == self.listbox.size():
            #     self.items.append(item)
            #     self.listbox.insert(END, item)
            # else:
            self.items.insert(curselection, item)
            self.listbox.insert(curselection, item)
            self.listbox.selection_clear(curselection)
            self.listbox.select_set(belowCurselection)
        else:
            # this allows inserting items below the last item
            self.items.append(item)
            self.listbox.insert(END, item)
        self.entrybox.delete(0, END)

    def deleteItem(self):        
        copyList(self.items, self.oldItems)
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
        fileDirectory = "C:\\Users\\jason\\Desktop\\"   # save to Desktop by default
        fileName = self.listName + " " + dateToday
        filePath = filedialog.asksaveasfile(confirmoverwrite = True,
                                            initialdir = fileDirectory,
                                            initialfile = fileName,
                                            defaultextension = ".txt",
                                            filetypes = [
                                                ("Text file", ".txt"),
                                                ("All files", ".*")
                                            ])
        if filePath is None:
            return
        else:
            for i in self.items:
                filePath.write(i + "\n")
            filePath.close()
            messagebox.showinfo(title = "Information", message = "Grocery List has been exported.")
            # print("Grocery List has been exported to \"" + fileName + ".txt\"")

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
            for i in self.items:
                file.write(i + "\n")
        messagebox.showinfo("File Saved", "The Inventory List was updated.")

class RecipeTab(ListTab):

    inventoryTab = None
    groceryListTab = None
    
    def __init__(self, notebook):
        super().__init__()
        self.notebook = notebook
        self.listName = "Custom Recipe"
        self.listLabel.configure(text = self.listName)
        self.exportButton.configure(text = "Save Recipe")

        # ADDITIONAL WIDGETS
        self.addRecipeToGroceryListButton = Button(self, text = "Recipe => Grocery List", command = self.addRecipeToGroceryList)
        self.resetRecipeButton = Button(self, text = "Build Recipe from Scratch", command = self.resetRecipe)
        self.renameRecipeButton = Button(self, text = "Rename Recipe", command = self.renameRecipe)

        self.addRecipeToGroceryListButton.grid(row = 7, column = 1)
        self.resetRecipeButton.grid(row = 8, column = 1)
        self.renameRecipeButton.grid(row = 9, column = 1)

    def createSearchWindowFunction(self):
        if SearchWindow.inactive:
            self.searchWindow = SearchWindow(getRecipeFunction = self.getRecipe)
        # elif SearchWindow.changed:
        #     self.searchWindow.destroy()
        #     self.searchWindow = SearchWindow(getRecipeFunction = self.getRecipe)
        #     SearchWindow.changed = False
        self.searchWindow.focus_set()

    def getRecipe(self, chosenRecipeName, chosenrecipeIngredients):
        copyList(self.items, self.oldItems)
        self.listName = chosenRecipeName
        self.items.clear()
        for i in chosenrecipeIngredients:
            self.items.append(i)
        refreshListbox(self.items, self.listbox)
        self.listLabel.configure(text = self.listName)
        self.notebook.select(2)  # hard-coded; recipeTab will always be 3rd tab
        self.focus_set()

    def exportList(self):
        dateToday = time.strftime("%Y-%m-%d", time.localtime())
        fileDirectory = "Recipes\\"   # save to Recipes folder
        fileName = self.listName + " " + dateToday
        filePath = filedialog.asksaveasfile(confirmoverwrite = True,
                                            initialdir = fileDirectory,
                                            initialfile = fileName,
                                            defaultextension = ".txt",
                                            filetypes = [
                                                ("Text file", ".txt"),
                                                ("All files", ".*")
                                            ])
        if filePath is None:
            return
        else:
            for i in self.items:
                filePath.write(i + "\n")
            filePath.close()
            messagebox.showinfo(title = "Information", message = "The recipe was saved.")
            if not SearchWindow.inactive:
                self.searchWindow.destroy()
                self.searchWindow = SearchWindow(getRecipeFunction = self.getRecipe)
            # print("This recipe has been exported to \"Recipes/" + fileName + "\"")

    def addRecipeToGroceryList(self):
        copyList(self.groceryListTab.items, self.groceryListTab.oldItems)
        for i in self.items:
            if (i not in self.groceryListTab.items) and (i not in self.inventoryTab.items):
                self.groceryListTab.items.append(i)
        refreshListbox(self.groceryListTab.items, self.groceryListTab.listbox)
        self.notebook.select(1)  # hard-coded; groceryListTab will always be 2nd tab

    def resetRecipe(self):
        copyList(self.items, self.oldItems)
        self.listName = "Custom Recipe"
        self.listLabel.configure(text = self.listName)
        self.items.clear()
        self.listbox.delete(0, END)

    def renameRecipe(self):
        if len(self.entrybox.get()) == 0:
            self.entrybox.insert(0, "Enter the recipe's name here")
        else:   
            self.listName = self.entrybox.get()
            self.listLabel.configure(text = self.listName)
            self.entrybox.delete(0, END)