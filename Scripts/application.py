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
from PIL import Image, ImageOps
import numpy as np
import cv2
import tensorflow as tf

def predict():
    
    model = tf.keras.models.load_model('Digit_classifier.h5')
    labels = {0:'0',1:'1',2:'2',3:'3', 4:'4', 5:'5', 6:'6', 7:'7',8:'8',9:'9'}

    save_drawing_as_grayscale_png()
    
    imgWhiteOnBlack = convert_drawing_to_white_on_black()

    image_tensor = convert_img_to_tensor(imgWhiteOnBlack)
    
    prediction = model.predict(image_tensor)
    
    prediction_label = labels[np.argmax(prediction)]
    wn.create_text(150, 50, text='Prediction: {}'.format(prediction_label), 
                   fill="white", font=('Helvetica 15 bold'))
    wn.place()

def paint(event):
    # get x1, y1, x2, y2 co-ordinates
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)
    color = "red"
    # display the mouse movement inside canvas
    wn.create_oval(x1, y1, x2, y2, fill=color, outline=color, width=10)

def clear_the_screen():
    wn.delete('all')
    pass
    
def save_drawing_as_grayscale_png():
    filepath = 'Canvas/'
    filename = 'drawing'
    # we need to save drawing as postscript before saving as
    # PNG image
    wn.postscript(file=filepath + filename + '.eps')
    image = Image.open(filepath + filename + '.eps')

    # saving grayscale image instead of color
    image = ImageOps.grayscale(image)
    image.save(filepath + filename +'.png', 'png')
    
def convert_drawing_to_white_on_black():
    im_gray = cv2.imread('Canvas/drawing.png', cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 250, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('Canvas/bw_image.png', im_bw)
    return im_bw
    
def convert_img_to_tensor(image):
    image = cv2.resize(image, (28,28))
    # adding dummy axes to convert to tensor
    image = image[...,np.newaxis]
    image_tensor = tf.convert_to_tensor(image, dtype=tf.float32)
    image_tensor = image_tensor[np.newaxis, ...]

    return image_tensor

# {
# Driver Code starts
if __name__ == "__main__":
    
    root = Tk()
    root.title("Digit Classifier")
    root.geometry("500x350")

    wn = Canvas(root, width=500, height=350, bg='black')
    wn.bind('<B1-Motion>', paint)
    wn.place(x = 100)

    # Creating buttons on the UI 
    quitButton = Button(root, text='Quit',command = root.quit, bg='white',width=5, height=1 )            
    quitButton.place(x=5, y = 10)

    saveButton = Button(root, text='Clear', command = clear_the_screen, bg = 'white', width=5, height=1)
    saveButton.place(x = 5, y = 50)

    predictButton = Button(root, text = 'Predict',command= predict, bg='white', width=5, height=1 )
    predictButton.place(x=5, y = 90)

    root.mainloop()

# } Driver Code ends