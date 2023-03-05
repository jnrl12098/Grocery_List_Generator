from tkinter import *
import os
from utilities import *

class SearchWindow(Toplevel):
    
    inactive = True
    recipeName = ""
    recipesList = []
    narrowedRecipesList = []
    recipeIngredients = []
    
    def __init__(self, getRecipeFunction = None):
        super().__init__()
        self.getRecipeFunction = getRecipeFunction  # a callback function
        self.entrybox = Entry(self)
        self.listLabel = Label(self)
        self.listbox = Listbox(self)
        self.filterSearchButton = Button(self, text = "Filter Search", command = self.filterSearch)
        self.displayRecipeButton = Button(self, text = "Display Ingredients", command = self.displayRecipe)
        self.displayAllRecipesButton = Button(self, text = "Display All Recipes", command = self.displayAllRecipes)
        self.chooseRecipeButton = Button(self, text = "Choose this Recipe", command = self.chooseRecipe)

        # WIDGET LOCATIONS
        self.entrybox.grid(row = 0, column = 0)
        self.listLabel.grid(row = 1, column = 0)
        self.listbox.grid(row = 2, column = 0, rowspan = 10)
        self.filterSearchButton.grid(row = 0, column = 1)
        self.displayRecipeButton.grid(row = 2, column = 1)
        self.displayAllRecipesButton.grid(row = 3, column = 1)
        self.chooseRecipeButton.grid(row = 4, column = 1)
        # TODO improve style
        
        # KEYBINDS
        self.entrybox.bind("<Return>", lambda event: self.filterSearch())
        self.entrybox.bind("<Control-BackSpace>", lambda event: self.entrybox.delete(0, END))
        self.listbox.bind("<Return>", lambda event: self.displayRecipe())
        self.listbox.bind("<Control-Return>", lambda event: self.chooseRecipe())

        # INITIALIZE SEARCH WINDOW
        self.__class__.inactive = False
        self.enlistRecipes()
        self.displayAllRecipes()

        self.protocol("WM_DELETE_WINDOW", self.closeSearchWindow)
    
    def enlistRecipes(self):
        self.recipesFolder = os.scandir("Recipes\\")
        for recipe in self.recipesFolder:
            if recipe.is_file():
                self.recipesList.append(recipe.name[slice(0,-4)])   # removes ".txt"
    # this way, the Recipes List refreshes each time the window is opened; 
    # useful when recipes are made using the Main Window and the user wants to see them on the Search Window

    def filterSearch(self):
        if len(self.entrybox.get()) == 0:
            pass
        else:
            self.searchWord = self.entrybox.get()
            self.entrybox.delete(0, END)
            self.narrowedRecipesList.clear()
            self.narrowedRecipesList = [i for i in self.recipesList if i.lower().find(self.searchWord.lower()) != -1]
            refreshListbox(self.narrowedRecipesList, self.listbox)
            self.listLabel.config(text = "Search Results for \"" + self.searchWord + "\"")
            if len(self.narrowedRecipesList) == 0:
                self.displayRecipeButton["state"] = DISABLED
                self.chooseRecipeButton["state"] = DISABLED
            else:
                self.displayRecipeButton["state"] = NORMAL
                self.chooseRecipeButton["state"] = NORMAL

    def displayRecipe(self):
        if len(self.listbox.curselection()) == 0:
            pass
        else:
            self.recipeName = self.listbox.get(self.listbox.curselection())
            fileAsList("Recipes\\" + self.recipeName + ".txt", self.recipeIngredients)
            self.createDisplayRecipeWindow(self.recipeName, self.recipeIngredients)

    def displayAllRecipes(self):
        if self.listbox.size() != len(self.recipesList):
            refreshListbox(self.recipesList, self.listbox)
            if self.displayRecipeButton["state"] == DISABLED:
                self.displayRecipeButton["state"] = NORMAL
            if self.chooseRecipeButton["state"] == DISABLED:
                self.chooseRecipeButton["state"] = NORMAL
        else:
            pass

    def createDisplayRecipeWindow(self, recipeName, recipeIngredients):
        displayRecipeWindow = Toplevel()
        displayRecipeWindow.title(recipeName)
        displayListbox = Listbox(displayRecipeWindow)
        displayListbox.pack()
        refreshListbox(recipeIngredients, displayListbox)
        displayListbox.focus_set()
        displayRecipeWindow.bind("<Escape>", lambda event: displayRecipeWindow.destroy())
        # TODO configure dimensions

    def chooseRecipe(self):
        if len(self.listbox.curselection()) == 0:
            pass
        else:
            self.recipeName = self.listbox.get(self.listbox.curselection())
            fileAsList("Recipes\\" + self.recipeName + ".txt", self.recipeIngredients)
            self.getRecipeFunction(self.recipeName, self.recipeIngredients)
    
    def closeSearchWindow(self):
        self.__class__.inactive = True
        self.destroy()


# def createSearchWindow():
#     if SearchWindow.inactive:
#         searchWindow = SearchWindow()
#         searchWindow.focus_set()

# def printRecipe(recipeName, ingredientsList):
#     print(recipeName)
#     for i in ingredientsList:
#         print(i)


# mainWindow = Tk()

# recipeName = ""
# ingredientsList = []

# searchButton = Button(mainWindow, text = "Search for a Recipe", command = createSearchWindow)
# searchButton.pack()
# printButton = Button(mainWindow, text = "Print Recipe", command = printRecipe(recipeName, ingredientsList))
# printButton.pack()

# mainWindow.mainloop()