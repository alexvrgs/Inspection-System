from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2, imutils, numpy as np

class myGUI():
    def __init__(self, master):
        global cap

        wFull_value = master.winfo_screenwidth()
        hFull_value = master.winfo_screenheight()

        self.master = master
        self.master.title('Inspection System')
        self.master.geometry('{}x{}+0+0'.format(str(wFull_value), str(hFull_value)))
        
        self.frame = Frame(self.master, bg = 'white')
        self.frame.pack()

        #--> Window Interface Setting <----------------------------------------------------------------- 

        self.leftPanelFrame = Frame(self.frame, width = 350, height = hFull_value, relief = 'groove', bd = 2, bg = 'white')
        self.leftPanelFrame.grid(column = 0, row = 0)

        self.rightPanelFrame = Frame(self.frame, width = 2350, height = hFull_value, relief = 'groove', bd = 2, bg = 'white')
        self.rightPanelFrame.grid(column = 1, row = 0)

        # --> GUI Setting <-----------------------------------------------------------------------------
        # Button START
        self.btnIniciar = Button(self.leftPanelFrame, text = 'Iniciar', width = 15)
        self.btnIniciar.grid(column = 0, row = 0, padx = 5, pady = 5)

        # Button STOP
        self.btnDetener = Button(self.leftPanelFrame, text = 'Detener', width = 15)
        self.btnDetener.grid(column = 0, row = 1, padx = 5, pady = 5)

        # Camera
        self.lblVideo = Label(self.rightPanelFrame, bg = 'white')
        self.lblVideo.grid(column = 0, row = 2, columnspan = 2, padx = 5, pady = 5) 

        cap = cv2.VideoCapture(0)
        self.videoStream()  
        
        # IMPUT IMAGE
        self.lblInputImage = Label(self.rightPanelFrame, bd = 2, relief = 'groove', bg = 'white')
        self.lblInputImage.grid(column = 1, row = 1)
          
        self.imageShow()

        self.lblInputImage.configure(image = self.img)
        self.lblInputImage.image = self.img     

        # Label IMPUT IMAGE
        lblInfo1 = Label(self.rightPanelFrame, text = 'IMAGEN DE ENTRADA')
        lblInfo1.grid(column = 1, row = 0, padx = 5, pady = 5)

    def imageShow(self):
        path_image = 'C:/VS_Code/Inspection_System/resource/img.jpg'

        # Read imput image
        self.image = (cv2.imread(path_image))
        self.image = imutils.resize(self.image, height = 300)

        # Show input image on GUI
        imageToShow = imutils.resize(self.image, width = 180)
        self.im = Image.fromarray(imageToShow)
        self.img = ImageTk.PhotoImage(image = self.im)

        return self.im, self.img
    
    def videoStream(self):
        global cap
        if cap is not None:
            ret, fram = cap.read()

            if ret == True:
                fram = imutils.resize(fram, width = 640)
                fram = cv2.cvtColor(fram, cv2.COLOR_BGR2RGB)

                im = Image.fromarray(fram)
                img = ImageTk.PhotoImage(image = im)
                
                self.lblVideo.configure(image = img)
                self.lblVideo.image = img
                self.lblVideo.after(10, self.videoStream)

            else:
                self.lblVideo.image = ''
                cap.release()

    def videoStart(self, camNum):
        global cap
        
        cap = cv2.VideoCapture(camNum)
        self.videoStream()

    def videoStop(self):
        global cap
        cap.release()

