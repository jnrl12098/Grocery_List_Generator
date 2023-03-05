Current GUI Version: 0.10
* functional enough to deliver the minimum expected features:
	* create a grocery list from scratch with Edit, Insert, Add, Remove
	* edit and update (export) an inventory of ingredients; data persists after closing the program
	* create (even from scratch), edit, and update own recipes; data persists after closing the program
	* search for a recipe from a defined list of recipes
	* display ingredients for a recipe
	* add the ingredients of a recipe to the grocery list while also filtering the ingredients
		that are still present in the inventory

* NEW Quality of Life (but necessary) update:
	* the search function is now done on a separate window

* keyboard shortcuts:
	* on Main Window:
			* Escape:			clear current listbox selection
		* on Entrybox:
			* Enter:			if no item is selected, add item; else, insert item
			* Ctrl + Enter: 	edit the highlighted item on the listbox with the contents of the entrybox
			* Ctrl + BackSpace:	clear the entire entrybox
		* on Listbox:
			* BackSpace:		delete the selected item, then select the item before it
			* Delete:			delete the selected item, then select the item after it
			* Ctrl + Enter:		copy the selected item to the entrybox 
				* useful for editing items; just remember to use Ctrl + Enter again to finalize editing the item
	* on Search Window:
		* on Entrybox:
			* Enter: 			filter search results
			* Ctrl + BackSpace:	clear the entire entrybox
		* on Listbox:
			* Enter:			display the ingredients of the highlighted recipe
			* Ctrl + Enter: 	choose the highlighted recipe; its contents are copied to the Recipe Tab of the Main Window
	* on Display Ingredients Window:
		* Escape: 				closes the window
