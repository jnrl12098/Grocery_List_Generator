#GROCERY LIST GENERATOR
import os

def display_list(items):                                #function to display list with numbering
    counter = 1
    for i in items:
        print("[" + str(counter) + "] " + i)            #format is "[counter] item"
        counter += 1

def search_recipe(recipes_list):
    narrowed_list = []                                      #build a narrowed-down list of recipes based on the search word
    while len(narrowed_list) == 0:                          #keep searching for recipes if the narrowed-down list is empty (implying that the search word is ineffective)
        search_word = input("Enter recipe: ").lower()           #set to lower-case for flexibility
        for i in recipes_list:                                  #for each item in the list of recipes,
            if i.lower().find(search_word) != -1:                   #if the search word is found in the item,
                narrowed_list.append(i)                                 #add the item to the narrowed-down list
        if len(narrowed_list) == 0:                             #if the narrowed-down list is empty after all that,
            print("Try another word.")
            continue                                                #search again with a different search word
        display_list(narrowed_list)                             #display the narrowed-down list of recipes
        print("[" + str(len(narrowed_list)+1) + "] Try another word/phrase")    #at the end of the list, add an option to search for a different recipe
        number = -1                                         #set this variable to -1 for the while-loop
        while number not in range(0, len(narrowed_list)+2):         #while the input number is not found in the range of options,
            number = int(input("Enter number of choice: "))             #ask the user to enter a number corresponding to an option in the list
        if number == (len(narrowed_list) + 1):                  #if the user picked the last option,
            narrowed_list.clear()                                   #by clearing the list, the condition of the while-loop to continue is met as well
        else:                                                   #check if this recipe's text file exists
            recipe_path = "Recipes\\" + narrowed_list[number - 1] + ".txt"
            if os.path.exists(recipe_path):                         #if the text file of the recipe exists,
                return narrowed_list[number-1]                          #return the name of the recipe
            else:                                                   #else, choose another recipe
                print("This recipe doesn't exist!")
                narrowed_list.clear()                                   # by clearing the list, the condition of the while-loop to continue is met as well
#MAIN
recipes_text = open("Recipes\\_Recipe List.txt", "r")   #access "_Recipe List.txt" file
recipes_list = []                                       #build list of recipes using recipes found in text file
for i in recipes_text.readlines():
    recipes_list.append(i[slice(0,-1)])                 #slice to remove "\n" from name when generating the list
recipes_text.close()                                    #close "_Recipe List.txt" file

inventory_text = open("Inventory.txt", "r")             #build list of inventory of ingredients in the same fashion as above
inventory_list = []
for i in inventory_text.readlines():
    inventory_list.append(i[slice(0,-1)])
inventory_text.close()

yn_choices = ["y", "n"]
done_adding = False
grocery_list = []                                       #build the grocery list from scratch, append as needed
dummy_recipe = []                                       #build the list of ingredients for the recipe
while done_adding == False:
    recipe = open("Recipes\\" + search_recipe(recipes_list) + ".txt", "r")
    for i in recipe.readlines():
        dummy_recipe.append(i[slice(0,-1)])
    recipe.close()
    #insert section where user edits the recipe
    for i in dummy_recipe:
        if i not in grocery_list and i not in inventory_list:
            grocery_list.append(i)
    choice = None
    while choice not in yn_choices:
        choice = input("Add more recipes? (y/n) ")
    if choice == "n":
        done_adding = True
    else:
        dummy_recipe.clear()

grocery_list.sort()
print("\nGrocery List:")
for i in grocery_list:
    print(i)

#grocery_text = open("Grocery List.txt", "w")
#grocery_text.close()







