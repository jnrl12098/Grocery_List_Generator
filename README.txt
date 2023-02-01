20230201
Project Version 0.03
*made using "_Recipes.txt" to generate list of recipes obsolete by using os.scandir
*improved the edit_list function by passing if the user inputs "" to avoid adding blanks, removing the entire list, or replacing an item on the list with a blank

20230116
Project Version 0.02
*incorporated walrus operators and list comprehensions to shorten code
	*note that
		choice = ""
		while choice := input() not in ["y","n"] 
			pass 				
	results in choice as true or false but
		choice = ""
		while (choice := input()) not in ["y","n"]
			pass
	results in choice as "y" or "n" 
*implemented a function to edit (add, remove, replace items) a list e.g. ingredients of a recipe or the items of a grocery list
	*considers a scenario where the user has emptied the list
*implemented export of grocery list into a text file

20230113 
Project Version 0.02 (no commits yet)
*cleanup of boilerplate code
	*implemented a function to write the contents of a text file into a list
	*implemented a function to display the contents of a list with numbering
*changed while done_adding = False into while True; going to incorporate this style from now on

20230103 8:20PM - 20230104 12:18AM 
Project Version 0.01
*implemented search function 
	*user can input full recipe name or portion of the name and program will output list of recipes based on that input
	*user can choose to search for another recipe if they want
*implemented checking function 
	*program will check if the recipe's text file of ingredients exists 
	*it is possible that if the recipe "does not exist," the name of the text file for the recipe was just misspelled
*implemented grocery list function 
	*after choosing one or multiple recipes, the ingredients of the chosen recipe/s are added to the grocery list 
		*duplicate ingredients and ingredients that currently exist in inventory (in-stock) are not added
	*these ingredients are sorted by alphabetical order before being presented to the user