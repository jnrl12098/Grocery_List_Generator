from tkinter import *

def fileAsList(filename, anyList):  
    anyList.clear()                    
    with open(filename, "r") as file:
        for i in file.readlines():
            if i[-1] == "\n":
                anyList.append(i[slice(0,-1)])                
            else:
                anyList.append(i)

def refreshListbox(anyList, anyListbox):
    anyListbox.delete(0, END)
    for i in range(len(anyList)):
        anyListbox.insert(i, anyList[i])

def copyList(sourceList, destinationList):
    destinationList.clear()
    for i in sourceList:
        destinationList.append(i)