20230223
GUI Version 0.05
* implemented an "Insert" Button which felt necessary to maintain the intended structure of the Inventory List
	* i.e, having categories such as [MEAT], [VEGETABLES], etc. 

20230216
GUI Version 0.04
* added a list for custom recipes
	* this will also store any recipe the user chooses in a future search function
* for now, the purpose of the mode variable is to prevent unnecessarily refreshing the listbox if the mode is the same
* for now, the lists are independent of each other, but these relationships are kept in mind:
	* ideally, the grocery list should automatically change if changes to the inventory list affect it
	* if a recipe is added to the grocery list, the ingredients are first filtered
		* i.e., if the ingredient is present in the inventory list, it will not be added to the grocery list
* boilerplate for the switchToNthList function could allow for easier implementation of future lists
	* e.g. "must-haves" list
* design choice: it is the user's responsibility to reflect changes in the inventory list to the grocery list
		if, for example, a recipe was introduced to the grocery list,
         the ingredients are first filtered by checking with the inventory list before going to the grocery list;
        but if the inventory list has changed afterwards e.g. an ingredient was removed,
         this ingredient which was initially filtered off from the recipe 
		  will not be automatically added to the grocery list;
        this is the user's responsibility now
		likewise, if an item was added to the inventory list, this item is not automatically removed from the grocery list
	* this is more flexible for the user; say they still have Salt in their inventory but are running out, 
		they could still choose to put Salt in their grocery list without the program messing with that
GUI Version 0.03
* implemented use of multiple lists (2 for now) that share one listbox
* when switching between lists:
	* data within lists are preserved 
	* the listbox refreshes to reflect the current list
* note: 
	list_A = []
	list_B = []
	list_A = list_B 
		will give list_A the memory address of list_B; list_A.append is now the same as list_B.append
	=> this allows the use of a middle-man list when switching between lists
GUI Version 0.02
* implemented O(1) method to update the internal list
GUI Version 0.01
* started with an entrybox, listbox, and "Edit," "Add," and "Remove" buttons to manipulate listbox 
* O(n) method to update the internal list
	* each time one of the buttons is clicked, the list is cleared and rebuilt
	* TODO: specialize the update function for each button to achieve O(1) when updating the internal list
* internal list is called midList as this list acts as a middle-man between the listbox and the various lists
	* lists such as Grocery List, List of Ingredients, Inventory List

20230201
Project Version 0.03
* made using "_Recipes.txt" to generate list of recipes obsolete by using os.scandir
* improved the edit_list function by passing if the user inputs "" to avoid adding blanks, removing the entire list, or replacing an item on the list with a blank

20230116
Project Version 0.02
* incorporated walrus operators and list comprehensions to shorten code
	* note that
		choice = ""
		while choice := input() not in ["y","n"] 
			pass 				
	results in choice as true or false but
		choice = ""
		while (choice := input()) not in ["y","n"]
			pass
	results in choice as "y" or "n" 
* implemented a function to edit (add, remove, replace items) a list e.g. ingredients of a recipe or the items of a grocery list
	* considers a scenario where the user has emptied the list
* implemented export of grocery list into a text file

20230113 
Project Version 0.02 (no commits yet)
* cleanup of boilerplate code
	* implemented a function to write the contents of a text file into a list
	* implemented a function to display the contents of a list with numbering
* changed while done_adding = False into while True; going to incorporate this style from now on

20230103 8:20PM - 20230104 12:18AM 
Project Version 0.01
* implemented search function 
	*user can input full recipe name or portion of the name and program will output list of recipes based on that input
	*user can choose to search for another recipe if they want
* implemented checking function 
	*program will check if the recipe's text file of ingredients exists 
	*it is possible that if the recipe "does not exist," the name of the text file for the recipe was just misspelled
* implemented grocery list function 
	* after choosing one or multiple recipes, the ingredients of the chosen recipe/s are added to the grocery list 
		* duplicate ingredients and ingredients that currently exist in inventory (in-stock) are not added
	* these ingredients are sorted by alphabetical order before being presented to the user