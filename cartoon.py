import cv2
import easygui 
import numpy as np 
import imageio 

import sys 
import matplotlib.pyplot as plt
import os 
import tkinter as tk 
from tkinter import filedialog
from tkinter import *
from tkmacosx import *
from PIL import ImageTk, Image 

top=tk.Tk() 
top.geometry('400x400') 
top.title('Cartoonify Your Image!') 
top.configure(background='black')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)


def cartoonify(ImagePath):
    
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    

    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    ReSized1 = cv2.resize(originalmage, (2261, 2810))


    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (2261, 2810))


    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (2261, 2810))


    getEdge = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(getEdge)

    blur = cv2.GaussianBlur(invert, (21, 21), 50)
    invertedblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(getEdge, invertedblur, scale=256.0)

    ReSized4 = cv2.resize(sketch, (2261, 2810))


    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (2261, 2810))


    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (2261, 2810))


    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(top,text="Save resized image",command=lambda: save(ReSized1, ImagePath,button_val=1),padx=15,pady=5)
    save1.configure(background='cyan', foreground='black',font=('Times',12,'bold'))
    save1.pack(side=TOP,pady=10)
    
    save2=Button(top,text="Save Grayscale image",command=lambda: save(ReSized2, ImagePath, button_val=2),padx=15,pady=5)
    save2.configure(background='cyan', foreground='black',font=('Times',12,'bold'))
    save2.pack(side=TOP,pady=10)
    
    save3=Button(top,text="Save smoothened Grayscale image",command=lambda: save(ReSized3, ImagePath, button_val=3),padx=15,pady=5)
    save3.configure(background='cyan', foreground='black',font=('Times',12,'bold'))
    save3.pack(side=TOP,pady=10)
    
    save4=Button(top,text="Save Pencil Sketch image",command=lambda: save(ReSized4, ImagePath, button_val=4),padx=15,pady=5)
    save4.configure(background='cyan', foreground='black',font=('Times',12,'bold'))
    save4.pack(side=TOP,pady=10)
    
    save5=Button(top,text="Save bilateral filtered image",command=lambda: save(ReSized5, ImagePath, button_val=5),padx=15,pady=5)
    save5.configure(background='cyan', foreground='black',font=('Times',12,'bold'))
    save5.pack(side=TOP,pady=10)
    
    save6=Button(top,text="Save Beautify image",command=lambda: save(ReSized6, ImagePath, button_val=6),padx=15,pady=5)
    save6.configure(background='cyan', foreground='black',font=('Times',12,'bold'))
    save6.pack(side=TOP,pady=10)
    plt.show()
    
    
def save(ReSized, ImagePath, button_val):
    if button_val==1:
     newName="Resized image"
    if button_val==2:
     newName="Grayscale image"
    if button_val==3:
     newName="smoothened Grayscale image" 
    if button_val==4:
     newName="Pencil Sketch image"
    if button_val==5:
        newName="bilateral filtered image"
    if button_val==6:
        newName="Beautify image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized, cv2.COLOR_RGB2BGR))
    I= "Your image is with the name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)


upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='cyan', foreground='black',font=('Times',12,'bold'))
upload.pack(side=TOP,pady=50)

top.mainloop()