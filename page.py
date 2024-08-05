import os
import shutil
import PIL.Image
import layouts

'''
Returns a list of all information from a page#.txt file in the order of:

date, title, location, caption, body text, food name, food location, rating, food text, image path, food image path
'''
def getPageInfo(notebookNum, pageNum):
    pageInfoFile = open(os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/pages/page{pageNum}.txt'), 'r')
    pageInfoLines = pageInfoFile.readlines()
    date = pageInfoLines[0]
    title = pageInfoLines[1]
    location = pageInfoLines[2]
    caption = pageInfoLines[3]
    bodyText = pageInfoLines[4]
    foodName = pageInfoLines[5]
    foodLocation = pageInfoLines[6]
    rating = pageInfoLines[7]
    foodText = pageInfoLines[8]
    image = pageInfoLines[9]
    foodImage = pageInfoLines[10]
    pageInfoFile.close()

    info = [date, title, location, caption, bodyText, 
            foodName, foodLocation, rating, foodText, 
            image, foodImage]
    
    return info

'''
Updates the read page layout to display the selected page's 
information. 
'''
def updateReadPageLayout(notebookNum, pageNum, window):
    pageInfo = getPageInfo(notebookNum, pageNum)
    window['-READPAGEDATE-'].update(pageInfo[0])
    window['-READPAGETITLE-'].update(pageInfo[1])
    window['-READPAGELOCATION-'].update(pageInfo[2])
    window['-READPAGEIMAGECAPTION-'].update(pageInfo[3])
    window['-READPAGEBODYTEXTBOX-'].update(pageInfo[4])
    window['-READPAGEFOODNAME-'].update(pageInfo[5])
    window['-READPAGEFOODLOCATION-'].update(pageInfo[6])
    window['-READPAGEFOODRATING-'].update(pageInfo[7])
    window['-READPAGEFOODTEXT-'].update(pageInfo[8])
    imagePath = os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/image{pageNum}.png')
    
    #TODO: Add zoom function
    window['-READIMAGE-'].update(filename=imagePath, subsample=setImageSubsample(imagePath))
    foodImagePath = os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/food_image{pageNum}.png')

    #TODO: Add zoom function
    window['-READFOODIMAGE-'].update(filename=foodImagePath, subsample=setImageSubsample(foodImagePath))

'''
Creates a new page#.txt file in the current notebook directory as dictated by notebookNum.
Returns the number of the new page as specified by the numerical order of pages currently in the pages directory.
'''
def createNewPage(notebookNum):
    notebookPath = os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/pages')
    numOfPages = len(os.listdir(notebookPath))
    newNum = numOfPages + 1
    pageFile = open(os.path.join(notebookPath, f'page{newNum}.txt'), 'w')
    for i in range(11):
        pageFile.write('\n')
    pageFile.close()
    shutil.copy(os.path.join(os.curdir, f'assets/app_images/new_image_icon.png'), os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/image{newNum}.png'))
    shutil.copy(os.path.join(os.curdir, f'assets/app_images/new_image_icon.png'), os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/food_image{newNum}.png'))

    
    return newNum

'''
Returns the the number of the latest page in a given notebook.
'''
def getLatestPageNum(notebookNum):
    notebookPath = os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/pages')
    return  len(os.listdir(notebookPath))

'''
Loads all text saved in the page#.txt file as specified by pageNum in their appropriate input
locations in the page edit view layout.
'''
def loadEditView(notebookNum, pageNum, window):
    pageInfo = getPageInfo(notebookNum, pageNum)
    window['-EDITPAGEDATE-'].update(pageInfo[0])
    window['-EDITPAGETITLE-'].update(pageInfo[1])
    window['-EDITPAGELOCATION-'].update(pageInfo[2])
    window['-EDITPAGEIMAGECAPTION-'].update(pageInfo[3])
    window['-EDITPAGEBODYTEXTBOX-'].update(pageInfo[4])
    window['-EDITPAGEFOODNAME-'].update(pageInfo[5])
    window['-EDITPAGEFOODLOCATION-'].update(pageInfo[6])
    window['-EDITPAGEFOODRATING-'].update(pageInfo[7])
    window['-EDITPAGEFOODTEXT-'].update(pageInfo[8])
    imagePath = os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/image{pageNum}.png')

    #TODO: Add zoom function
    window['-IMAGE-'].update(filename=imagePath, subsample=setImageSubsample(imagePath))
    foodImagePath = os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/food_image{pageNum}.png')

    #TODO: Add zoom function
    window['-FOODIMAGE-'].update(filename=foodImagePath, subsample=setImageSubsample(foodImagePath))

'''
Overwrites the page#.txt file as specified by pageNum with the values read from
the edit page layout.
'''
def savePage(notebookNum, pageNum, values, imagePath, foodImagePath):
   date = values['-EDITPAGEDATE-'].strip()
   title = values['-EDITPAGETITLE-'].strip()
   location = values['-EDITPAGELOCATION-'].strip()
   imageCaption = values['-EDITPAGEIMAGECAPTION-'].strip()
   bodyText = values['-EDITPAGEBODYTEXTBOX-'].replace('\n', ' ')
   foodName = values['-EDITPAGEFOODNAME-'].strip()
   foodLocation = values['-EDITPAGEFOODLOCATION-'].strip()
   foodRating = values['-EDITPAGEFOODRATING-'].strip()
   foodText = values['-EDITPAGEFOODTEXT-'].replace('\n', ' ')
   image = imagePath
   foodImage = foodImagePath
   
   if imagePath != None:
        shutil.copy(image, os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/image{pageNum}.png'))
   else:
       shutil.copy(os.path.join(os.curdir, f'assets/app_images/new_image_icon.png'), os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/image{pageNum}.png'))
   if foodImagePath != None:
        shutil.copy(foodImage, os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/food_image{pageNum}.png'))
   else:
       shutil.copy(os.path.join(os.curdir, f'assets/app_images/new_image_icon.png'), os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/food_image{pageNum}.png'))

   pageFile = open(os.path.join(layouts.notebookDir, f'notebook{notebookNum}', 'pages', f'page{pageNum}.txt'), 'w')
   pageFile.write(date + '\n')
   pageFile.write(title + '\n')
   pageFile.write(location + '\n')
   pageFile.write(imageCaption + '\n')
   pageFile.write(bodyText + '\n')
   pageFile.write(foodName + '\n')
   pageFile.write(foodLocation + '\n')
   pageFile.write(foodRating + '\n')
   pageFile.write(foodText + '\n')
   pageFile.write(os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/image{pageNum}.png') + '\n')
   pageFile.write(os.path.join(os.curdir, f'assets/notebooks/notebook{notebookNum}/images/food_image{pageNum}.png') + '\n')
   pageFile.close()

'''
Takes an image file path, calculates and returns a integer for use of PySimpleGui's subsample parameter
to resize the image within the application display. If the image fits within the maximum width and height of
300 and 300 pixels, respectively, returns 1 (the image is not resized). 
'''
def setImageSubsample(imagePath):
    maxWidth = 300
    maxHeight = 300
    image = PIL.Image.open(imagePath)
    width, height = image.size

    if width <= maxWidth and height <= maxHeight:
        return 1
    
    i = 1
    newWidth = width
    newHeight = height
    while newWidth > maxWidth or newHeight > maxHeight:
        i += 1
        newWidth = width/i
        newHeight = height/i
    return i
