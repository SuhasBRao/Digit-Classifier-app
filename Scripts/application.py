'''
This file creates the GUI of the app and allows the
User to draw any numbers from 0 to 9 and to predict it.

Note: - The app only recognizes digits from 0 to 9
      - Make sure to install Tensorflow before running 
        this script.

IF YOU GET OSError while running this script follow below link:
->https://www.tutorialexample.com/fix-oserror-unable-to-locate-ghostscript-on-paths-for-python-beginners-python-tutorial/
'''

from tkinter import *
from PIL import Image, EpsImagePlugin,ImageGrab
import numpy as np
import cv2
from numpy.lib.type_check import imag
import tensorflow as tf
root = Tk()
root.title("Digit Classifier")
root.geometry("500x350")

def paint(event):
    # get x1, y1, x2, y2 co-ordinates
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)
    color = "red"
    # display the mouse movement inside canvas
    wn.create_oval(x1, y1, x2, y2, fill=color, outline=color, width=10)

def clear():
    wn.delete('all')
    pass
    

def predict():
    ### the drawing on canvas is saved ###
    filepath = 'Canvas/'
    filename = 'drawing'
    wn.postscript(file=filepath + filename + '.eps', colormode="color")
    image = Image.open(filepath + filename + '.eps')
    # image.show()
    image.save(filepath + filename +'.png', 'png')

    ### Prediction part ###
    model = tf.keras.models.load_model('Digit_classifier.h5')
    # image = cv2.imread('Canvas/drawing.png')
    # image.show()
    #convert black on white to white to black 
    im_gray = cv2.imread('Canvas/drawing.png', cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 250, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('Canvas/bw_image.png', im_bw)

    print(im_bw.shape)
    image = cv2.resize(im_bw, (28,28))
    print(image.shape)

    # cv2.imshow('img',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    #convert image to grayscale
    # image = np.mean(image, -1, keepdims= True)
    # print(image.shape)

    image = image[...,np.newaxis]
    print(image.shape)
    
    image_tensor = tf.convert_to_tensor(image, dtype=tf.float32)
    image_tensor = image_tensor[np.newaxis, ...]
    print(image_tensor.shape)

    prediction = model.predict(image_tensor)
    print(prediction)
    labels = {0:'0',1:'1',2:'2',3:'3', 4:'4', 5:'5', 6:'6', 7:'7',8:'8',9:'9'}

    prediction_label = labels[np.argmax(prediction)]
    wn.create_text(150, 50, text='Prediction: {}'.format(prediction_label), fill="white", font=('Helvetica 15 bold'))
    wn.place()

    # print(labels[np.argmax(prediction)])
    pass

wn=Canvas(root, width=500, height=350, bg='black')
wn.bind('<B1-Motion>', paint)
wn.place(x = 100)

quitButton = Button(root, text='Quit',command=root.quit, bg='white',width=5, height=1 )            
quitButton.place(x=5, y = 10)

saveButton = Button(root, text='clear', command = clear, bg = 'white', width=5, height=1)
saveButton.place(x = 5, y = 50)

predictButton = Button(root, text = 'Predict',command= predict, bg='white', width=5, height=1 )
predictButton.place(x=5, y = 90)
# create canvas


# bind mouse event with canvas(wn)


root.mainloop()