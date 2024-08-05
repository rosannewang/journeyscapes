import glob
import os
import PySimpleGUI as sg
import mainMenu

sg.theme('lightbrown3')
notebookIconPath = os.path.join(os.curdir, 'assets/app_images/notebook_icon_red.png') 
notebookDir = os.path.join(os.curdir, 'assets/notebooks')
notebookDirFiles = glob.glob(notebookDir + "\*")

mainMenuLayout = [
    [sg.Frame('', [[sg.VPush()],
        [sg.Push(), sg.Image(os.path.join(os.curdir, 'assets/app_images/app_logo.png'), background_color='#C1D7AE', subsample=3, pad=(0, 50)), sg.Push()],
        [sg.Push(), sg.Text('JOURNEYSCAPE', font=("Calibri", 60)), sg.Push()],
        [sg.VPush()]], border_width=0, size=(560, 720)),  
    sg.Push(), sg.Column(mainMenu.drawNotebooks(notebookDirFiles, notebookIconPath), key='-MAINMENUNOTEBOOKIMGS-', scrollable=True, vertical_scroll_only=True, size=(720, 720), pad=(0, 50))],
]

countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", 
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", 
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", 
    "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", 
    "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the", 
    "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", 
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", 
    "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", 
    "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", 
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", 
    "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", 
    "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", 
    "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", 
    "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", 
    "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", 
    "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", 
    "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", 
    "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", 
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", 
    "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", 
    "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", 
    "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", 
    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", 
    "Zambia", "Zimbabwe"
]
#NOT TO BE USED ANYWHERE ELSE, ONLY IN NEWNOTEBOOKLAYOUT, CREATED FOR READABILITY PURPOSES
newNotebookBody = [
    [sg.Text("New Notebook", key='-NEWNOTEBOOKLAYOUTTITLE-', size=(20, 1), font=("Calibri", 20), justification='center', pad=(150, 20))],
    [sg.Text("Title", size=(15, 1)), sg.InputText(key='-NEWNOTEBOOKTITLEINPUT-', do_not_clear=True, pad=(0, 10))],
    [sg.Text("Country", size=(15, 1)), sg.Combo(countries, key='-COUNTRYCOMBO-', pad=(0, 10))],
    [sg.Text("State/City/Etc.", size=(15, 1)), sg.InputText(key='-STATE/CITY/ETCINPUT-', do_not_clear=True, pad=(0, 10))],
    [sg.Text("Start of Trip", size=(15, 1)), sg.InputText(key='-STARTOFTRIPINPUT-', do_not_clear=True, pad=(0, 10)), sg.CalendarButton("Calendar", target='-STARTOFTRIPINPUT-')],
    [sg.Text("End of Trip", size=(15, 1)), sg.InputText(key='-ENDOFTRIPINPUT-', do_not_clear=True, pad=(0, 10)), sg.CalendarButton("Calendar", target='-ENDOFTRIPINPUT-')],
    [sg.Text("Notebook Color", size=(15, 1)), sg.Combo(['black', 'blue', 'brown', 'green', 'orange', 'pink', 'purple', 'red', 'white', 'yellow'], default_value='red', key='-COLOR-', readonly=True, pad=(0, 10))],
    [sg.Button("Cancel", key='-CANCELNEWNOTEBOOKBUTTON-', size=(10, 1), pad=(3, 25)), sg.Button("Create", key='-CREATENOTEBOOKBUTTON-', size=(10, 1), pad=(20, 30)), sg.Button("Save", key='-SAVENOTEBOOKEDITBUTTON-', visible=False, size=(15, 1), pad=(20, 30))]
]

newNotebookLayout = [
    [sg.VPush()],
    [sg.Push(), sg.Column(newNotebookBody, pad=(350, 100), element_justification='left'), sg.Push()],
    [sg.VPush()]
]

notebookTitle = [
     [sg.Text('Notebook Title', key='-NOTEBOOKTITLE-', justification= 'c', background_color= '#C1D7AE', font=('Calibiri',35, 'bold'))]

]

addPage = os.path.join(os.curdir, 'assets/app_images/add_page.png')

coreNotebookLayout = [
    [sg.Frame('', [[sg.VPush()]]  + notebookTitle + [[sg.VPush()]], size=(600,100), border_width=1, element_justification='c', background_color='#C1D7AE')],
    [sg.Text('Country: ', key = '-NOTEBOOKCOUNTRY-', size= (22,1), justification = 'c', font=('Calibiri', 18, 'bold'))],
    [sg.Text('State/City/Province:', key='-NOTEBOOKSTATE/CITY/ETC-', size = (22,2), justification = 'c', font=('Calibiri', 18, 'bold'))],
    [sg.Text('Start:', key='-NOTEBOOKSTARTOFTRIP-', size = (25,1), justification = 'c', font=('Calibiri',18, 'bold'))], 
    [sg.Text('End:', key='-NOTEBOOKENDOFTRIP-', size = (25,1), justification = 'c', font=('Calibiri',18, 'bold'), pad=(5,(0,30)))],
    [sg.Text('Open Notebook', size = (40,1), justification='center', font=('Calibiri',22, 'bold'))],
    [sg.Button('First Page', key='-NOTEBOOKFIRSTPAGEBUTTON-', size = (10,1), font = ('Calibiri',15, 'bold')), sg.Button('Latest Page', key='-NOTEBOOKLATESTPAGEBUTTON-',size = (10,1), font=('Calibiri',15, 'bold')) ],
    [sg.Button('', key='-NEWPAGEBUTTON-', image_filename= addPage, size = (10, 1), font=('Calibiri',15, 'bold'))],
    [sg.Button("Back", key='-NOTEBOOKMENUEXITBUTTON-', size=(10, 1), font=('Calibiri',15, 'bold'), pad=(1, (75,0)))]
]

notebookLayout = [[sg.Frame('', [[sg.VPush()]]  + coreNotebookLayout + [[sg.VPush()]], size=(1280, 720), border_width=10, element_justification='c')]]

#SINGLE PAGE LAYOUT UPDATED
#Column saves the date
pageCol = [
    [sg.Push(), sg.Text("Date",font=("Calibri", 18)), sg.InputText(key='-EDITPAGEDATE-',size=(30, 30)), sg.CalendarButton('Calendar', target='-EDITPAGEDATE-'), sg.Push()],
]
#First column saves page title and location
pageCol1 = [
    [sg.InputText("Page Title", key='-EDITPAGETITLE-', size=(270, 160), font=("Calibri", 80))],
    [sg.Text('Location',font=("Calibri", 18)), sg.InputText(key='-EDITPAGELOCATION-')],
]
#Column holds first image and caption feature
pageCol2 = [
    [sg.Push(), sg.Image(filename='assets/app_images/new_image_icon.png', key='-IMAGE-', subsample=3, enable_events=True), sg.Push()],
    [sg.Push(), sg.Text('Image Caption',font=("Calibri", 18)), sg.InputText(key='-EDITPAGEIMAGECAPTION-')]
]

#Column holds food image
pageCol3 = [
    [sg.Image(filename='assets/app_images/new_image_icon.png', key='-FOODIMAGE-', subsample=3, enable_events=True)],
]
#Food review column
pageCol4 = [
    [sg.Push(), sg.Text("Food Name",font=("Calibri", 15)), sg.InputText(key='-EDITPAGEFOODNAME-', size=(35, 1)), sg.Text("Location",font=("Calibri", 15)), sg.InputText(key='-EDITPAGEFOODLOCATION-', size=(35, 1)), sg.Text("Rating",font=("Calibri", 15),size=(5, 1)), sg.Combo(['5 stars', '4 stars', '3 stars', '2 stars', '1 star'], key='-EDITPAGEFOODRATING-')],
    [sg.Multiline(size=(120, 15), key='-EDITPAGEFOODTEXT-')]
]

#Main Layout
singlePageLayout = [
    [sg.Column(pageCol)],
    [sg.Text('', size=(200, 0))],
    [sg.Column(pageCol1, size=(640, 200), element_justification='left'),sg.Column(pageCol2,element_justification='center'),sg.Push()],
    [sg.Multiline(size=(168, 20), key='-EDITPAGEBODYTEXTBOX-')],
    [sg.Text("Food of the Day", size=(90, 1), justification='center', font=("Calibri", 20, 'bold'))],
    [sg.Column(pageCol3, vertical_alignment='center'),sg.Column(pageCol4, vertical_alignment='top')],
]

pageLayout = [
    [sg.Column(singlePageLayout, scrollable=True, vertical_scroll_only=True, size=(1280, 640), key='-EDITPAGECOLUMN-')], 
    [sg.Push(), sg.Button("Save Page", key='-SAVEPAGEBUTTON-'), sg.Button("Exit", key='-EXITEDITPAGEBUTTON-'), sg.Push()]
]


#NOT TO BE USED ANYWHERE, ONLY IN READPAGELAYOUT, CREATED FOR READABILITY PURPOSES

readPageCol = [
    [sg.Push(), sg.Text("Date:",font=("Calibri", 30, 'bold')), sg.Text("",key='-READPAGEDATE-',font=("Calibri", 30),size=(30, 1)),sg.Push()],
]
#First column saves page title and location
readPageCol1 = [
    [sg.Text("", key='-READPAGETITLE-', size=(270), font=("Calibri", 80))],
    [sg.Text('Location:',font=("Calibri", 18, 'bold')), sg.Text("",key='-READPAGELOCATION-',font=("Calibri", 18),size=(50, 1))]
]
#Column holds first image and caption feature
readPageCol2 = [
    [sg.Push(), sg.Image(filename='assets/app_images/new_image_icon.png', key='-READIMAGE-', subsample=3), sg.Push()],
    [sg.Push(), sg.Text('Image Caption:',font=("Calibri", 18, 'bold')), sg.Text(key='-READPAGEIMAGECAPTION-',font=("Calibri", 18),size=(None, 1)), sg.Push()]
]

#Column holds food image
readPageCol3 = [
    [sg.Image(filename='assets/app_images/new_image_icon.png', key='-READFOODIMAGE-', subsample=3)]
]
#Food review column
readPageCol4 = [
    [sg.Push(), sg.Text("Food Name:",font=("Calibri", 15, 'bold')), sg.Text("",key='-READPAGEFOODNAME-',font=("Calibri", 15), size=(None, 1)), sg.Text("Location:",font=("Calibri", 15, 'bold')), sg.Text("",key='-READPAGEFOODLOCATION-',font=("Calibri", 15), size=(None, 1)), sg.Text("Rating:",font=("Calibri", 15, 'bold')), sg.Text('', key='-READPAGEFOODRATING-',font=("Calibri", 15), size=(None, 1)), sg.Push()],
    [sg.Multiline(size=(120, 15), key='-READPAGEFOODTEXT-', disabled=True)]
]

#Main Layout
finalPageLayout = [
    [sg.Column(readPageCol)],
    [sg.Column(readPageCol1,size=(640, 200), element_justification='left'),sg.Push(), sg.Column(readPageCol2,element_justification='center', size=(400, 340)),sg.Push()],
    [sg.Multiline(size=(168, 20), key='-READPAGEBODYTEXTBOX-', disabled=True)],
    [sg.Text("Food of the Day", size=(90, 1), font=("Calibri", 20, 'bold'), justification='center')],
    [sg.Column(readPageCol3, vertical_alignment='center'),sg.Column(readPageCol4, vertical_alignment='center')]
]

readPageLayout = [
    [sg.Column(finalPageLayout, scrollable=True, vertical_scroll_only=True, size=(1280, 640))], 
    [sg.Button("Previous Page", key='-PREVREADPAGEBUTTON-'), sg.Push(), sg.Button("Edit", key='-EDITREADPAGEBUTTON-'), sg.Button('Delete', key='-DELETEPAGEBUTTON-'), sg.Button("Back", key='-EXITREADPAGEBUTTON-'), sg.Push(), sg.Button("Next Page", key='-NEXTREADPAGEBUTTON-')]
]
