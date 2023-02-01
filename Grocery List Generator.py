#GROCERY LIST GENERATOR
import os

def display_list(items):                                # function to display list with numbering
    counter = 1
    for i in items:
        print("[" + str(counter) + "] " + i)            # format is "[counter] item"
        counter += 1

def file_as_list(filename, list):                       # function to place contents of a file into a list
    with open(filename, "r") as file:
        for i in file.readlines():
            list.append(i[slice(0,-1)])                 # removes the "\n" at the end

def search_recipe(recipes_list):                        # function to search for a recipe from a list of recipes
    narrowed_list = []                                      # build a narrowed-down list of recipes based on the search word
    while len(narrowed_list) == 0:                          # keep searching for recipes if the narrowed-down list is empty (implying that the search word is ineffective)
        search_word = input("Enter recipe: ").lower()           # set to lower-case for flexibility
        narrowed_list = [i for i in recipes_list if i.lower().find(search_word) != -1]
        if len(narrowed_list) == 0:                             # if the resulting narrowed-down list is empty, loop again to try a different search word
            print("Try another word.")
            continue
        display_list(narrowed_list)                             # display the narrowed-down list of recipes
        print("[" + str(len(narrowed_list)+1) + "] Try another word/phrase")    # at the end of the list, add an option to search for a different recipe
        number = -1                                         #set this variable to -1 for the while-loop
        while number not in range(0, len(narrowed_list)+2):         #while the input number is not found in the range of options,
            number = int(input("Enter number of choice: ")) - 1          #ask the user to enter a number corresponding to an option in the list
        if number == len(narrowed_list):                    #if the user picked the last option, ( number = (len(narrowed_list) + 1) - 1 )
            narrowed_list.clear()                                   #by clearing the list, the condition of the while-loop to continue is met as well
        else:                                                   #check if this recipe's text file exists
            recipe_path = "Recipes\\" + narrowed_list[number] + ".txt"
            if os.path.exists(recipe_path):                         #if the text file of the recipe exists,
                return narrowed_list[number]                            #return the name of the recipe
            else:                                                   #else, choose another recipe
                print("This recipe's file does not exist.")
                narrowed_list.clear()                                   # by clearing the list, the condition of the while-loop to continue is met as well

def edit_list(dummy_recipe):                          # function to edit a list of items
    edit_choices = ["Add Items", "Remove Items", "Replace Items", "Done Editing"]
    while True:
        print("------------------\nEditing Menu:")
        display_list(edit_choices)  # display the choices for editing
        int_choice = 0
        while int_choice not in range(1, 5):                # use while-loop to make sure user only chooses among choices
            int_choice = int(input("Enter the number of your choice: "))
        if int_choice == 1:         # add items
            while (add_ingredient := input("One at a time, enter the items to add (or type \"Done\" to go back): ")).lower() != "done":
                # to prevent inputs of "" from adding blank entries
                if len(add_ingredient) == 0:
                    pass
                else:
                    dummy_recipe.append(add_ingredient)
            print("------------------\nUpdated list of items:")      # update the user on the list of ingredients
            display_list(dummy_recipe)
        elif int_choice == 2:       #remove items
            if len(dummy_recipe) == 0:
                print("There are no more items on the list.")   # if there are no ingredients in the recipe, user shouldn't be able to remove an ingredient
            else:
                while (remove_ingredient := input("Enter the item to remove (or type \"Done\" to go back): ")).lower() != "done":
                    # to prevent inputs of "" from removing all entries at once
                    if len(remove_ingredient) == 0:
                        pass
                    else:
                        dummy_recipe = [i for i in dummy_recipe if i.lower().find(remove_ingredient) == -1]  # if i.lower().find(remove_ingredient) = -1 then we don't want to remove the ingredient
                        if len(dummy_recipe) == 0:
                            print("There are no more items on the list.")
                            break
                        else:
                            print("------------------\nUpdated list of items:")
                            display_list(dummy_recipe)
        elif int_choice == 3:       #replace an ingredient with another ingredient
            if len(dummy_recipe) == 0:
                print("There are no more items on the list.")   # if there are no ingredients in the recipe, user shouldn't be able to place an ingredient
            else:
                while True:
                    print("------------------\nUpdated list of items:")
                    display_list(dummy_recipe)
                    print("[" + str(len(dummy_recipe) + 1) + "] Go back to previous menu.")
                    edit_index = -1
                    while edit_index not in range(0, len(dummy_recipe) + 1):
                        edit_index = int(input("Enter the number of the item to replace (or enter [" + str(len(dummy_recipe) + 1) + "] to go back): ")) - 1
                    if edit_index == len(dummy_recipe):
                        break
                    else:
                        edit_ingredient = ""
                        while len(edit_ingredient) == 0:
                            edit_ingredient = input("Enter the item to replace " + dummy_recipe[edit_index] + ": ")
                        dummy_recipe[edit_index] = edit_ingredient
        else:
            break
    return dummy_recipe

#MAIN
dummy_recipe = []                                       # used to generate an instance of a recipe
grocery_list = []                                       # build the grocery list from scratch, append one recipe at a time
recipes_list = []                                       # used to contain list of recipes
storage_list = []                                       # used to contain list of ingredients in inventory from text file

# import list of recipes
# with this method, there is no need for a separate text file with the list of recipes
recipes_folder = os.scandir("Recipes")
for recipe in recipes_folder:
    if recipe.is_file():
        recipes_list.append(recipe.name[slice(0,-4)])
# import list of ingredients in inventory
file_as_list("Inventory.txt", storage_list)
# add recipes to the grocery list
while True:
    dummy_recipe.clear()                                                            # clear the dummy list before starting each iteration
    file_as_list("Recipes\\" + search_recipe(recipes_list) + ".txt", dummy_recipe)  # generate an instance of the recipe
    print("These are the ingredients for the recipe:")                              # display the ingredients of the recipe
    display_list(dummy_recipe)
    while (choice := input("Edit the recipe? (y/n) ")) not in ["y", "n"]:           # ask the user if they want to edit the recipe
        pass
    if choice == "y":                                                               # if yes, enter editing recipe mode; else, continue
        dummy_recipe = edit_list(dummy_recipe)                                        # update instance of recipe
        if len(dummy_recipe) == 0:                                                      # in the case where there are no more ingredients, update the user
            print("All of the ingredients for this recipe have been removed.")
        else:
            print("------------------\nUpdated list of ingredients for the recipe:")
            display_list(dummy_recipe)
    for i in dummy_recipe:                                                          # add the ingredients of this instance of the recipe to the grocery list
        if i not in grocery_list and i not in storage_list:
            grocery_list.append(i)
    while (choice := input("Add more recipes? (y/n) ")) not in ["y", "n"]:          # ask the user if they want to add more recipes
        pass
    if choice == "n":                                                               # if the user doesn't want to add more recipes, proceed to finalizing grocery list
        break
# organize and edit the grocery list directly
grocery_list.sort()                                                             # sort the grocery list before displaying to the user
print("\nGrocery List:")
display_list(grocery_list)
while (choice := input("Edit the grocery list? (y/n) ")) not in ["y","n"]:      # ask the user if they want to edit the grocery list
    pass
if choice == "y":
    grocery_list = edit_list(grocery_list)
    if len(grocery_list) == 0:
        print("All of the items in the grocery list have been removed.")
    else:
        print("------------------\nUpdated grocery list:")
        display_list(grocery_list)
if len(grocery_list) > 0:
    grocery_list.sort()                                                             # sort the grocery list before exporting
    print("The grocery list has been sorted and exported to \"Grocery List.txt\"")  # export the list to a text file
    with open("Grocery List.txt", "w") as file:
        for i in grocery_list:
            file.write(i + "\n")
else:
    print("There's no grocery list to export.")