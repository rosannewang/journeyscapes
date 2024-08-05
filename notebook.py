import glob
import layouts
import os

'''
Creates a notebook dir containing all necessary child dirs and writes a 'notebook#_info.txt'
file to store all user inputted notebook infomation in the format of (exluding brackets):

[title]
[country]
[state/city/etc]
[start of trip]
[end of trip]
[notebook color]
'''
def createNotebook(title, country, city, tripStart, tripEnd, color):
    if not color:  # Set default color if none provided
        color = 'red'
    numNotebooks = len(glob.glob(os.path.join(os.curdir, 'assets/notebooks') + "\*"))
    newNotebookNum = numNotebooks + 1
    #Add all necessary folders
    os.mkdir(os.path.join(layouts.notebookDir, f'notebook{newNotebookNum}'))
    os.mkdir(os.path.join(layouts.notebookDir, f'notebook{newNotebookNum}/pages'))
    os.mkdir(os.path.join(layouts.notebookDir, f'notebook{newNotebookNum}/images'))

    #Make and write notebook info file
    notebookInfoFile = open(os.path.join(layouts.notebookDir, f'notebook{newNotebookNum}', f'notebook{newNotebookNum}_info.txt'), 'w')
    notebookInfoFile.write(title + '\n')
    notebookInfoFile.write(country + '\n')
    notebookInfoFile.write(city + '\n')
    notebookInfoFile.write(tripStart + '\n')
    notebookInfoFile.write(tripEnd + '\n')
    notebookInfoFile.write(color + '\n')
    notebookInfoFile.close()

'''
Overwrites the notebook#_info.txt file with new information.
'''
def editNotebook(infoPath, title, country, city, tripStart, tripEnd, color):
    notebookInfoFile = open(infoPath, 'w')
    notebookInfoFile.write(title + '\n')
    notebookInfoFile.write(country + '\n')
    notebookInfoFile.write(city + '\n')
    notebookInfoFile.write(tripStart + '\n')
    notebookInfoFile.write(tripEnd + '\n')
    notebookInfoFile.write(color + '\n')
    notebookInfoFile.close()
    return color

'''
Display the selected notebook's information in the notebook menu.
'''
def drawNotebookMenuInfo(window, notebookNum):
    notebookInfoFile = open(os.path.join(layouts.notebookDir, f'notebook{notebookNum}', f'notebook{notebookNum}_info.txt'))
    info = notebookInfoFile.readlines()
    window['-NOTEBOOKTITLE-'].update(f'{info[0]}')
    window['-NOTEBOOKCOUNTRY-'].update(f'Country: {info[1]}')
    window['-NOTEBOOKSTATE/CITY/ETC-'].update(f'State/City/Etc.: {info[2]}')
    window['-NOTEBOOKSTARTOFTRIP-'].update(f'Start of Trip: {info[3]}')
    window['-NOTEBOOKENDOFTRIP-'].update(f'End of Trip: {info[4]}')