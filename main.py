import PySimpleGUI as sg
import glob
import os
import layouts
import mainMenu
import notebook
import page
from natsort import natsorted
#In cmd: pip install natsort

#Keep track of current page and notebook
currentNotebookNum = -1
currentPageNum = -1

#Main layout that establishes all layouts for the main window
baseLayout = [[sg.Col(layouts.mainMenuLayout, key='-MAINMENULAYOUT-', element_justification='center'), 
               sg.Col(layouts.notebookLayout, key='-NOTEBOOKLAYOUT-', visible=False),
               sg.Col(layouts.pageLayout, key='-PAGELAYOUT-', visible=False),
               sg.Col(layouts.newNotebookLayout, key='-NEWNOTEBOOKLAYOUT-', visible=False, element_justification='center'),
               sg.Col(layouts.readPageLayout, key='-READPAGELAYOUT-', visible=False)
               ]]

#Main app window (size ratio = 16:9 * 80 --> 1280:720)
sg.theme('lightbrown3')
window = sg.Window('JOURNEYSCAPE', baseLayout, size=(1280, 720), icon=os.path.join(os.curdir, f'assets/app_images/app_logo_fill.ico'))
currLayoutKey = '-MAINMENULAYOUT-'

#Changes the windows current layout to the desired layout
def updateLayout(newLayoutKey):
    global currLayoutKey
    window[currLayoutKey].update(visible=False)
    currLayoutKey = newLayoutKey
    window[currLayoutKey].update(visible=True)

#Initial file setup
if not os.path.exists(os.path.join(os.curdir, 'assets/notebooks')):
    os.makedirs(os.path.join(os.curdir, 'assets/notebooks'))

#Notebook and page numbers to be deleted
notebooksNumsToDelete = []

#Dictionary of notebook numbers with list of pages within to be deleted as the key, like so:
#{notebookNum}:[pageA, pageC, pageD, ..., pageN], {notebookNum}:[pageE, pageG, pageJ, ..., pageN], etc.
pageNumsToDelete = {}

#Tracking of Page Creation and Deletion
totalPages = []

'''
Finds the next available page in a single specified direction (1 for forward, -1 for backward)
and returns it. If there is no available page in the specified direction, returns -1.
'''
def getCurrentPageNum(currentNotebookNum, currentPageNum, direction):
    if currentNotebookNum in pageNumsToDelete.keys():
        pagesToDelete = pageNumsToDelete[currentNotebookNum]
        i = currentPageNum+direction
        while i <= len(totalPages) and i > 0:
            #i+=direction
            if i in pagesToDelete:
                i+=direction
            else:
                return i
        return -1
    currentPageNum+=direction
    if currentPageNum <= len(totalPages) and currentPageNum > 0:
        return currentPageNum
    return -1

#Master loop to handle all possible events
while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    
    #Main menu events
    #---------------------------------------------------------------------------------
    #Handle new notebook event
    elif event == '-NEWNOTEBOOKBUTTON-':
        window['-NEWNOTEBOOKLAYOUTTITLE-'].update('New Notebook')
        window['-NEWNOTEBOOKTITLEINPUT-'].update('')
        window['-COUNTRYCOMBO-'].update('')
        window['-STATE/CITY/ETCINPUT-'].update('')
        window['-STARTOFTRIPINPUT-'].update('')
        window['-ENDOFTRIPINPUT-'].update('')
        window['-COLOR-'].update('')
        updateLayout('-NEWNOTEBOOKLAYOUT-')
        
    elif event == ('-CANCELNEWNOTEBOOKBUTTON-'):
        updateLayout('-MAINMENULAYOUT-')

    #Create notebook files
    elif event == '-CREATENOTEBOOKBUTTON-':
        notebook.createNotebook(values['-NEWNOTEBOOKTITLEINPUT-'], values['-COUNTRYCOMBO-'], values['-STATE/CITY/ETCINPUT-'], values['-STARTOFTRIPINPUT-'], values['-ENDOFTRIPINPUT-'], values['-COLOR-'])
        #Update layouts
        window['-COUNTRYCOMBO-'].update('')
        updateLayout('-MAINMENULAYOUT-')
        notebookFiles = glob.glob(os.path.join(os.curdir, 'assets/notebooks') + "\*")
        #Redraw main menu to add new notebook
        window.extend_layout(window['-MAINMENUNOTEBOOKIMGS-'], [mainMenu.createNotebookRow(layouts.notebookIconPath, natsorted(notebookFiles), len(notebookFiles))])
        window.refresh()
        window['-MAINMENUNOTEBOOKIMGS-'].contents_changed()

    #Open notebook
    elif '-NOTEIMG' in event:
        noteNum = ''.join(filter(str.isdigit, event))
        currentNotebookNum = noteNum
        notebook.drawNotebookMenuInfo(window, currentNotebookNum)
        totalPages = glob.glob(os.path.join(os.curdir, f'assets/notebooks/notebook{currentNotebookNum}/pages/*'))
        updateLayout('-NOTEBOOKLAYOUT-')

    #Edit notebook button
    elif '-EDITNOTEBOOK' in event:
        #Display all current notebook information
        notebookInfoPath = os.path.join(os.curdir, f'assets/notebooks/notebook{mainMenu.getNumbers(event)}/notebook{mainMenu.getNumbers(event)}_info.txt')
        notebookInfoFile = open(notebookInfoPath, 'r')
        title = notebookInfoFile.readline().strip()
        country = notebookInfoFile.readline().strip()
        city = notebookInfoFile.readline().strip()
        tripStart = notebookInfoFile.readline().strip()
        tripEnd = notebookInfoFile.readline().strip()
        color = notebookInfoFile.readline().strip()
        notebookInfoFile.close()
        
        window['-NEWNOTEBOOKLAYOUTTITLE-'].update('Edit Notebook')
        window['-NEWNOTEBOOKTITLEINPUT-'].update(title)
        window['-COUNTRYCOMBO-'].update(country)
        window['-STATE/CITY/ETCINPUT-'].update(city)
        window['-STARTOFTRIPINPUT-'].update(tripStart)
        window['-ENDOFTRIPINPUT-'].update(tripEnd)
        window['-COLOR-'].update(color)
        updateLayout('-NEWNOTEBOOKLAYOUT-')
        #Switch buttons in layout
        window['-SAVENOTEBOOKEDITBUTTON-'].update(visible=True)
        window['-CREATENOTEBOOKBUTTON-'].update(visible=False)

    #Save edited notebook
    elif '-SAVENOTEBOOKEDITBUTTON-' == event:
        #Update notebook info file, update notebook color, update main menu, update layout
        color = notebook.editNotebook(notebookInfoPath, values['-NEWNOTEBOOKTITLEINPUT-'], values['-COUNTRYCOMBO-'], values['-STATE/CITY/ETCINPUT-'], values['-STARTOFTRIPINPUT-'], values['-ENDOFTRIPINPUT-'], values['-COLOR-'])
        window[f'-NOTEIMG{mainMenu.getNumbers(notebookInfoPath)}TEXT-'].update(f'Title: {values["-NEWNOTEBOOKTITLEINPUT-"]}\nCountry: {values["-COUNTRYCOMBO-"]}\nTrip Start: {values["-STARTOFTRIPINPUT-"]}\nTrip End: {values["-ENDOFTRIPINPUT-"]}')
        window[f'-NOTEIMG{mainMenu.getNumbers(notebookInfoPath)}-'].update(filename=os.path.join(os.curdir, f'assets/app_images/notebook_icon_{color}.png'), subsample=5)
        window['-SAVENOTEBOOKEDITBUTTON-'].update(visible=False)
        window['-CREATENOTEBOOKBUTTON-'].update(visible=True)
        updateLayout('-MAINMENULAYOUT-')

    #Delete notebook
    elif '-DELETENOTEBOOK' in event:
        #Confirmation window
        deleteAnswer = sg.PopupYesNo('WARNING: You are about to delete this notebook, are you sure you would like to continue?', title='WARNING')
        if deleteAnswer == 'Yes':
            #Add notebook to list to delete files later, hide notebook row to update layout
            notebooksNumsToDelete.append(mainMenu.getNumbers(event))
            window[f'-NOTEBOOKROW{mainMenu.getNumbers(event)}-'].update(visible=False)
    
    #Notebook menu events
    #---------------------------------------------------------------------------------
    #Open first page in notebook
    elif event == '-NOTEBOOKFIRSTPAGEBUTTON-':
        totalPages = glob.glob(os.path.join(os.curdir, f'assets/notebooks/notebook{currentNotebookNum}/pages/*'))
        if currentNotebookNum in pageNumsToDelete.keys():
            pagesToDelete = pageNumsToDelete[currentNotebookNum]
        else:
            pagesToDelete = []
        
        #Logic to determine which menu/page to display
        if len(totalPages) == 0 or len(totalPages) == len(pagesToDelete):
            sg.PopupOK('There are no pages in this notebook. Please write a new page.', title='Attention')
        elif 1 in pagesToDelete:
            num = getCurrentPageNum(currentNotebookNum, 1, 1)
            currentPageNum = num
            page.updateReadPageLayout(currentNotebookNum, currentPageNum, window)
            updateLayout('-READPAGELAYOUT-')
        else:
            page.updateReadPageLayout(currentNotebookNum, 1, window)
            currentPageNum = 1
            updateLayout('-READPAGELAYOUT-')

    #Open latest page in notebook
    elif event == '-NOTEBOOKLATESTPAGEBUTTON-':
        totalPages = glob.glob(os.path.join(os.curdir, f'assets/notebooks/notebook{currentNotebookNum}/pages/*'))
        if currentNotebookNum in pageNumsToDelete.keys():
            pagesToDelete = pageNumsToDelete[currentNotebookNum]
        else:
            pagesToDelete = []
        latestPage = page.getLatestPageNum(currentNotebookNum)

        #Logic to determine which menu/page to display
        if len(totalPages) == 0 or len(totalPages) == len(pagesToDelete):
            sg.PopupOK('There are no pages in this notebook. Please write a new page.', title='Attention')
        elif latestPage in pagesToDelete:
            num = getCurrentPageNum(currentNotebookNum, latestPage, -1)
            currentPageNum = num
            page.updateReadPageLayout(currentNotebookNum, currentPageNum, window)
            updateLayout('-READPAGELAYOUT-')
        else:
            page.updateReadPageLayout(currentNotebookNum, latestPage, window)
            currentPageNum = latestPage
            updateLayout('-READPAGELAYOUT-')

    #Create a new page
    elif event == '-NEWPAGEBUTTON-':
        currentPageNum = page.createNewPage(currentNotebookNum)
        page.loadEditView(currentNotebookNum, currentPageNum, window)
        updateLayout('-PAGELAYOUT-')

    #Exit notebook menu
    elif event == '-NOTEBOOKMENUEXITBUTTON-':
        currentNotebookNum = -1
        updateLayout('-MAINMENULAYOUT-')
    
    #Read Page view events
    #---------------------------------------------------------------------------------
    #Go to previous page
    elif event == '-PREVREADPAGEBUTTON-':
        totalPages = glob.glob(os.path.join(os.curdir, f'assets/notebooks/notebook{currentNotebookNum}/pages/*'))
        num = getCurrentPageNum(currentNotebookNum, currentPageNum, -1)
        if num != -1:
            currentPageNum = num
            page.updateReadPageLayout(currentNotebookNum, currentPageNum, window)
        else: 
            sg.popup_ok('This is the first page, you cannot go back any further.', title='Warning')

    #Go to next page
    elif event == '-NEXTREADPAGEBUTTON-':
        totalPages = glob.glob(os.path.join(os.curdir, f'assets/notebooks/notebook{currentNotebookNum}/pages/*'))
        num = getCurrentPageNum(currentNotebookNum, currentPageNum, 1)
        if num != -1:
            currentPageNum = num
            page.updateReadPageLayout(currentNotebookNum, currentPageNum, window)
        else:
            sg.popup_ok('This is the last page, you cannot continue any further.', title='Warning')

    #Edit a page
    elif event == '-EDITREADPAGEBUTTON-':
        page.loadEditView(currentNotebookNum, currentPageNum, window)
        window.refresh()
        window['-EDITPAGECOLUMN-'].contents_changed()
        updateLayout('-PAGELAYOUT-')

    #Delete a page
    elif event == '-DELETEPAGEBUTTON-':
        deleteAnswer = sg.PopupYesNo('WARNING: You are about to delete this page, are you sure you would like to continue?', title='WARNING')
        if deleteAnswer == 'Yes':
            #Add page number and notebook num to pages to delete dictionary
            if pageNumsToDelete.get(currentNotebookNum) == None:
                pageNumsToDelete[currentNotebookNum] = []
            pageList = pageNumsToDelete[currentNotebookNum]
            pageList.append(currentPageNum)
            pageNumsToDelete[currentNotebookNum] = pageList

            #Go to next available page in reader view, search forward first, then backwards
            num = getCurrentPageNum(currentNotebookNum, currentPageNum, 1)
            if num != -1:
                currentPageNum = num
                page.updateReadPageLayout(currentNotebookNum, currentPageNum, window)    
            else:
                num = getCurrentPageNum(currentNotebookNum, currentPageNum, -1)
                if num != -1:
                    currentPageNum = num
                    page.updateReadPageLayout(currentNotebookNum, currentPageNum, window)
                else:
                    updateLayout('-NOTEBOOKLAYOUT-')
                    sg.PopupOK('There are no pages left in this notebook. You have been returned to the notebook menu.', title='Attention')

    #Exit read page view
    elif event == '-EXITREADPAGEBUTTON-':
        updateLayout('-NOTEBOOKLAYOUT-')

    #Edit Page view menu events
    #---------------------------------------------------------------------------------
    #Add Image to Page
    elif event == '-IMAGE-':
        filename = sg.popup_get_file('Select an image', file_types=(("Image Files", "*.png"),))
        if filename:
            window['-IMAGE-'].metadata = filename
            window['-IMAGE-'].update(filename=filename, subsample=page.setImageSubsample(filename))
            window.refresh()
            window['-EDITPAGECOLUMN-'].contents_changed()

    
    #Add Food Image to Page
    elif event == '-FOODIMAGE-':
        filename = sg.popup_get_file('Select an image', file_types=(("Image Files", "*.png"),))
        if filename:
            window['-FOODIMAGE-'].metadata = filename
            window['-FOODIMAGE-'].update(filename=filename, subsample=page.setImageSubsample(filename))
            window.refresh()
            window['-EDITPAGECOLUMN-'].contents_changed()

    #Saves a page's content
    elif event == '-SAVEPAGEBUTTON-':
        sg.PopupOK('Page was successfully saved!', title='Page saved!')
        page.savePage(currentNotebookNum, currentPageNum, values, window['-IMAGE-'].metadata, window['-FOODIMAGE-'].metadata)
        page.updateReadPageLayout(currentNotebookNum, currentPageNum, window)
        updateLayout('-READPAGELAYOUT-')
        
    #Exit edit page view
    elif event == '-EXITEDITPAGEBUTTON-':
        exitAnswer = sg.PopupYesNo('WARNING: any unsaved changes will be discarded, are you sure you would like to continue?', title='WARNING')
        if exitAnswer == 'Yes':
            page.updateReadPageLayout(currentNotebookNum, currentPageNum, window)
            updateLayout('-READPAGELAYOUT-')

#Delete required notebooks and close window
mainMenu.deleteNotebooks(notebooksNumsToDelete)
mainMenu.deletePages(pageNumsToDelete)
window.close()
