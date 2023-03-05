from tkinter import *
import os
from utilities import *

class SearchWindow(Toplevel):
    
    def __init__(self):
        super().__init__()
        self.entrybox = Entry(self)
        self.listLabel = Label(self)
        self.listbox = Listbox(self)
        self.printButton = Button(self, text = "I do something", command = self.printRecipes)
        self.filterSearchButton = Button(self, text = "Filter Search", command = self.filterSearch)
        self.displayRecipeButton = Button(self, text = "Display Ingredients of Recipe", command = self.displayRecipe)

        self.recipeName = ""
        self.recipesList = []
        self.narrowedList = []
        self.displayedRecipe = []

        self.entrybox.grid(row = 0, column = 0)
        self.listLabel.grid(row = 1, column = 0)
        self.listbox.grid(row = 2, column = 0, rowspan = 10)
        self.filterSearchButton.grid(row = 0, column = 1)
        self.displayRecipeButton.grid(row = 2, column = 1)
        self.printButton.grid(row = 3, column = 1)
        
        self.entrybox.bind("<Return>", lambda event: self.filterSearch())
        self.listbox.bind("<Return>", lambda event: self.displayRecipe())

        self.enlistRecipes()
    
    def enlistRecipes(self):
        self.recipesFolder = os.scandir("Recipes\\")
        for recipe in self.recipesFolder:
            if recipe.is_file():
                self.recipesList.append(recipe.name[slice(0,-4)])   # remove ".txt"

    def filterSearch(self):
        if len(self.entrybox.get()) == 0:
            pass
        else:
            self.searchWord = self.entrybox.get()
            self.entrybox.delete(0, END)
            self.narrowedList.clear()
            self.narrowedList = [i for i in self.recipesList if i.lower().find(self.searchWord.lower()) != -1]
            refreshListbox(self.narrowedList, self.listbox)
            self.listLabel.config(text = "Search Results for \"" + self.searchWord + "\"")

    def displayRecipe(self):
        if len(self.listbox.curselection()) == 0:
            pass
        else:
            self.recipeName = self.listbox.get(self.listbox.curselection())
            self.displayedRecipe.clear()
            fileAsList("Recipes\\" + self.recipeName + ".txt", self.displayedRecipe)
            self.createDisplayRecipeWindow(self.recipeName, self.displayedRecipe)

    def createDisplayRecipeWindow(self, anyName, anyList):
        displayRecipeWindow = Toplevel()
        displayRecipeWindow.title("Recipe " + anyName)
        displayListbox = Listbox(displayRecipeWindow)
        displayListbox.grid(row = 0, column = 0)
        refreshListbox(anyList, displayListbox)
        displayRecipeWindow.bind("<Escape>", lambda event: displayRecipeWindow.destroy())

    def printRecipes(self):
        for i in self.recipesList:
            print(i)

def createSearchWindow():
    searchWindow = SearchWindow()


mainWindow = Tk()

searchButton = Button(mainWindow, text = "Search for a Recipe", command = createSearchWindow)
searchButton.pack()

mainWindow.mainloop()