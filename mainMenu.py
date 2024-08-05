import glob
import shutil
import PySimpleGUI as sg
from natsort import natsorted
#In cmd: pip install natsort
import os

'''
Creates and returns a string of the last unbroken set of digits found within a string in order of left to right.
'''
def getNumbers(string):
    nums = ''
    i = 1
    while i <= len(string) and string[-i].isdigit() == False:
        i += 1
    while i <= len(string) and string[-i].isdigit() == True:
        nums = nums + string[-i]
        i += 1
    
    return nums[::-1]

'''
Creates and returns a row containing the specified notebook number image with key='-NOTEIMG#-',
text displaying information related to the notebook, and an 'X' button to delete the notebook.
'''
def createNotebookRow(notebookIconPath, allNotebookFilesSorted, notebookNum):
    currNotebookInfo = open(f'{allNotebookFilesSorted[notebookNum-1]}/notebook{notebookNum}_info.txt').readlines()
    title = currNotebookInfo[0]
    country = currNotebookInfo[1]
    tripStart = currNotebookInfo[3]
    tripEnd = currNotebookInfo[4]
    color = currNotebookInfo[5].strip()
        

    notebookIconPath = os.path.join(os.curdir, f'assets/app_images/notebook_icon_{color}.png')

    rowLayout = [[sg.Image(notebookIconPath, key=f'-NOTEIMG{notebookNum}-', enable_events=True, subsample=3), 
                sg.Text(f'Title: {title}\nCountry: {country}\nTrip Start: {tripStart}\nTrip End: {tripEnd}', key=f'-NOTEIMG{notebookNum}TEXT-', size=(40, 0), font=(None, 12)),
                sg.Button('Edit', key=f'-EDITNOTEBOOK{notebookNum}-', pad=(5,0), font=(None, 16)), sg.Button('X', key=f'-DELETENOTEBOOK{notebookNum}-', pad=(5,0), font=(None, 16), tooltip='Delete this notebook')]
    ]

    row = [sg.pin(sg.Col(rowLayout, key=f'-NOTEBOOKROW{notebookNum}-'))]
    
    return row

'''
When the main menu is first drawn, this method is called to draw all notebooks
and their text information in numerical order (aka in oldest to newest).
'''
def drawNotebooks(allNotebookFiles, notebookIconPath):
    #Sort list of all notebook dirs in numerical order
    allNotebookFilesSorted = allNotebookFiles.copy()
    allNotebookFilesSorted = natsorted(allNotebookFilesSorted)
    numNotebooks = len(allNotebookFilesSorted)

    #Setup new layout
    newNotebookLayout = [[sg.Image(os.path.join(os.curdir, 'assets/app_images/new_notebook_icon.png'), key='-NEWNOTEBOOKBUTTON-', enable_events=True, subsample=3), sg.Text('New Notebook', font=(None, 12))]]
    for i in range(numNotebooks):
        newNotebookLayout.append([])

    #Add all notebook files indiviually into each row
    i = 1
    currRowIndex = 1
    while i <= numNotebooks:
        row = createNotebookRow(notebookIconPath, allNotebookFilesSorted, i)
        newNotebookLayout[currRowIndex] = row
        i+=1
        currRowIndex+=1
    
    return newNotebookLayout

'''
Deletes all notebook dirs according to number as specified in the list parameter, 
then renames all remaining files to retain correct numerical order.
'''
def deleteNotebooks(notebookNums):
    #Collect all paths of notebooks to be deleted, just for debug purposes
    paths = []
    for num in notebookNums:
        path = os.path.join(os.curdir, f'assets/notebooks/notebook{num}')
        paths.append(path)
    
    #Recursively delete all specified notebook dirs
    if len(paths) != 0:
        for path in paths:
            shutil.rmtree(path)

    #Rename all files as needed to correct notebook numbering
    notebookFiles = glob.glob(os.path.join(os.curdir, 'assets/notebooks') + "\*")
    i = 1
    for file in notebookFiles:
        #Replace all notebook#_info and notebook# #s with new number in sequential order
        newFileName = file.replace(getNumbers(file), str(i))
        os.rename(os.path.join(file, f'notebook{getNumbers(file)}_info.txt'), os.path.join(file, f'notebook{i}_info.txt'))
        os.rename(file, newFileName)
        i+=1

def deletePages(pageNums):
    #Collect all paths of pages and page images to be deleted, for debug purposes
    paths = []
    for key in pageNums.keys():
        for i in range(len(pageNums[key])):
            path = os.path.join(os.curdir, f'assets/notebooks/notebook{key}')
            imagePath = path
            foodImagePath = path
            path = os.path.join(path, f'pages/page{pageNums[key][i]}.txt')
            imagePath = os.path.join(imagePath, f'images/image{pageNums[key][i]}.png')
            foodImagePath = os.path.join(foodImagePath, f'images/food_image{pageNums[key][i]}.png')
            print(path)
            paths.append(path)
            paths.append(imagePath)
            paths.append(foodImagePath)
    
    #Delete all specified files
    if len(paths) != 0:
        for path in paths:
            os.remove(path)

    #Rename all files as to correct page numbering order
    for key in pageNums.keys():
        pages = glob.glob(os.path.join(os.curdir, f'assets/notebooks/notebook{key}/pages/*'))
        pages = natsorted(pages)
        i = 1
        for file in pages:
            newFileName = file.replace(f'page{getNumbers(file)}', f'page{str(i)}')
            os.rename(file, newFileName)
            i+=1

        images = glob.glob(os.path.join(os.curdir, f'assets/notebooks/notebook{key}/images/image*'))
        images = natsorted(images)
        i = 1
        for file in images:
            newFileName = file.replace(f'image{getNumbers(file)}', f'image{str(i)}')
            os.rename(file, newFileName)
            i+=1

        foodImages = glob.glob(os.path.join(os.curdir, f'assets/notebooks/notebook{key}/images/food_image*'))
        foodImages = natsorted(foodImages)
        i = 1
        for file in foodImages:
            newFileName = file.replace(f'food_image{getNumbers(file)}', f'food_image{str(i)}')
            os.rename(file, newFileName)
            i+=1
