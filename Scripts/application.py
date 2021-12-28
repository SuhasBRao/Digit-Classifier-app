'''
This file creates the GUI of the app and allows the
User to draw any numbers from 0 to 9 and to predict it.

Note: - The app only recognizes digits from 0 to 9
      - Make sure to install Tensorflow before running 
        this script.
'''

from tkinter import *
from PIL import Image
root = Tk()
root.title("Digit Classifier")
root.geometry("500x350")

def paint(event):
    # get x1, y1, x2, y2 co-ordinates
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)
    color = "black"
    # display the mouse movement inside canvas
    wn.create_oval(x1, y1, x2, y2, fill=color, outline=color)

def save():
    filepath = 'Canvas/'
    filename = 'drawing'
    wn.postscript(file=filepath + filename + '.eps', colormode="color")
    image = Image.open(filepath + filename + '.eps')
    image.resize((28,28))
    image.save(filepath + filename +'.png', 'png')
    
# def predict:  

quitButton = Button(root, text='Quit',command=root.quit, bg='white',width=5, height=1 )            
quitButton.place(x=5, y = 10)

saveButton = Button(root, text='Save', command = save, bg = 'white', width=5, height=1)
saveButton.place(x = 5, y = 50)

predictButton = Button(root, text = 'Predict', )
# create canvas
wn=Canvas(root, width=500, height=350, bg='white')

# bind mouse event with canvas(wn)
wn.bind('<B1-Motion>', paint)
wn.place(x = 100)



root.mainloop()