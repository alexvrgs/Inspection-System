from re import L
from tkinter import *
from tkinter import filedialog,ttk  
from PIL import ImageTk, Image
from configparser import *
import imutils
import numpy as np
import cv2


class Window_Log():
    def __init__(self, master):
        self.master = master
        self.master.title('Inspection System')
        self.master.resizable(0,0)
        
        self.frame = Frame(self.master, bg = 'white')
        self.frame.pack()

        self.menuBar = Menu(self.master, bg = 'white')
        self.master.config(menu = self.menuBar)

        # >>> Variables
        self.Password = StringVar()
        self.cb_text = StringVar()

        # >>> Menu Settings 

        self.helpMenu = Menu(self.menuBar, tearoff = 0)
        self.helpMenu.add_command(label = 'Configuration', command = lambda: config_Win(self.master))
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label = 'About')

        self.menuBar.add_cascade(label = 'Help', menu = self.helpMenu)

        # >>> Frame Setting 

        self.logoFrame = Frame(self.frame, width = 500, height = 100, relief = 'flat', bd = 5, bg = 'white')
        self.logoFrame.grid(column = 0, row = 0, padx = 25)

        self.loginFrame = Frame(self.frame, width = 500, height = 100, relief = 'groove', bd = 5, bg = 'white')
        self.loginFrame.grid(column = 0, row = 1, padx = 50, pady = 10)

        self.btnFrame = Frame(self.frame, width = 500, height = 100, relief = 'groove', bd = 5, bg = 'white')
        self.btnFrame.grid(column = 0, row = 2, padx = 50, pady = 10)

        # >>> Window Interface Setting 

        self.original_image = Image.open('C:/VS_Code/Inspection_System/resource/carbon_icon.png')
        self.original_image = self.original_image.resize((70, 70), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.original_image)

        self.lblTitle = Label(self.logoFrame, image = self.image, bd = 20, bg = 'white')
        self.lblTitle.grid(column = 0, row = 0, rowspan = 2)

        self.lblTitle = Label(self.logoFrame, text = 'Carbon Inspection', font = ('Helvetica', 24, 'bold'), bg = 'white')
        self.lblTitle.grid(column = 1, row = 0)

        self.lblTitle = Label(self.logoFrame, text = 'System', font = ('Helvetica', 24, 'bold'), bg = 'white')
        self.lblTitle.grid(column = 1, row = 1)

        self.lblUser = Label(self.loginFrame, text = 'Username:', font = ('Helvetica', 14, 'bold'), bd = 22, bg = 'white')
        self.lblUser.grid(column = 0, row = 0)

        self.comboUser = ttk.Combobox(self.loginFrame, textvariable = self.cb_text,font = ('Helvetica', 11), state = 'readonly')
        self.comboUser.grid(column = 1, row = 0, padx = 20)
        
        self.comboValues()
        self.comboUser['values'] = (self.users[:,1])

        self.lblPW = Label(self.loginFrame, text = 'Password: ', font = ('Helvetica', 14, 'bold'), bd = 22, bg = 'white')
        self.lblPW.grid(column = 0, row = 1)

        self.entryPW = Entry(self.loginFrame, font = ('Helvetica', 12, 'bold'), width = 20, relief = 'groove', bd = 5, show = '*', textvariable = self.Password)
        self.entryPW.grid(column = 1, row = 1, padx = 20 )

        self.btnLog = Button(self.btnFrame, text = 'Log in', width = 15, font = ('Helvetica', 14, 'bold'), relief = 'flat', bg = 'white', activebackground = 
        'white', command = self.loginSystem)
        self.btnLog.grid(column = 0, row = 0)

        self.master.bind('<Return>', self.loginSystem)

    def comboValues(self):
        file = 'C:/VS_Code/Inspection_System/resource/Carbon_Inspection_Users.ini'
        config = ConfigParser()
        config.read(file)
        self.users = np.array(config.items('Users'))

    def loginSystem(self, event = None):
        self.comboValues()
     

class Config_Win():
    def __init__(self, master):
        self.master = master
        self.master.title('Inspection System - Configuration')
        self.master.geometry('485x475+400+100')
        self.master.resizable(0,0)
        
        self.frame = Frame(self.master, bg = 'white')
        self.frame.pack()

        # >>> Variables

        global cap
        self.cameraSelected = StringVar()
        self.camNum = None


        # >>> Frame Setting

        self.generalFrame = Frame(self.frame, width = 500, height = 75, relief = 'groove', bd = 2, bg = 'white')
        self.generalFrame.grid(column = 0, row = 0, padx = 5, pady = 5)
        
        self.snFrame = Frame(self.frame, width = 500, height = 75, relief = 'groove', bd = 2, bg = 'white')
        self.snFrame.grid(column = 0, row = 1, padx = 5, pady = 5)

        self.cameraFrame = Frame(self.frame, width = 500, height = 75, relief = 'groove', bd = 2, bg = 'white')
        self.cameraFrame.grid(column = 0, row = 2, padx = 5, pady = 5)

        self.btnFrame = Frame(self.frame, width = 500, height = 50, relief = 'flat', bd = 2, bg = 'white')
        self.btnFrame.grid(column = 0, row = 3, padx = 5, pady = 5)

        # >>> Window Interface Setting 
        
        # General Frame
        self.lblGeneral = Label(self.generalFrame, text = 'General', font = ('Helvetica', 10), bg = 'white')
        self.lblGeneral.grid(column = 0, row = 0, sticky = 'w')
 
        # > Input Entry
        self.lblInput = Label(self.generalFrame, text = 'Input CSV File: ', font = ('Helvetica', 10), bg = 'white')
        self.lblInput.grid(column = 0, row = 1, sticky = 'w') 
        
        self.entryFile = Entry(self.generalFrame, width = 40, font = ('Helvetica', 10), bg = 'white')
        self.entryFile.grid(column = 1, row = 1, padx = 5, pady = 5)
        
        self.btnSelect = Button(self.generalFrame, text = 'Select', font = ('Helvetica', 10), bg = 'white')
        self.btnSelect.grid(column = 2, row = 1, padx = 10, pady = 10)
        
        # > Output Entry
        self.lblOutput = Label(self.generalFrame, text = 'Output Path: ', font = ('Helvetica', 10), bg = 'white')
        self.lblOutput.grid(column = 0, row = 2, sticky = 'w')
        
        self.entryOutput = Entry(self.generalFrame, width = 40, font = ('Helvetica', 10), bg = 'white')
        self.entryOutput.grid(column = 1, row = 2, padx = 5, pady = 5)

        # Serial Number Frame
        self.lblSN = Label(self.snFrame, text = 'Serial Number', font = ('Helvetica', 10), bg = 'white')
        self.lblSN.grid(column = 0, row = 0, sticky = 'w')

        # > Prefix Lenght Checkbox
        self.prefixCheck = Checkbutton(self.snFrame, text = 'Validate Prefix and Lenght', bg = 'white')
        self.prefixCheck.grid(column = 0, row = 1, pady = 5)
        
        # > Prefix Entry
        self.lblPrefix = Label(self.snFrame, text = 'Prefix: ', font = ('Helvetica', 10), bg = 'white', state = 'disabled')
        self.lblPrefix.grid(column = 0, row = 2, sticky = 'w')

        self.prefixEntry = Entry(self.snFrame, width = 40, font = ('Helvetica', 10), bg = 'white', state = 'readonly')
        self.prefixEntry.grid(column = 1, row = 2, pady = 5, padx = 5)

        # > Lenght Combobox
        self.lblLenght = Label(self.snFrame, text = 'Lenght: ', font = ('Helvetica', 10), bg = 'white', state = 'disabled')
        self.lblLenght.grid(column = 0, row = 3, sticky = 'w')

        self.lengthCombo = ttk.Combobox(self.snFrame, state = 'disabled')
        self.lengthCombo.grid(column = 1, row = 3, padx = 5, pady = 5)

        # Camera Frame
        self.lblCamera = Label(self.cameraFrame, text = 'Camera', font = ('Helvetica', 10), bg = 'white')
        self.lblCamera.grid(column = 0, row = 0, sticky = 'w')

        # > Select Camera
        self.btnSelectCam = Button(self.cameraFrame, text = 'Select', width = 15, font = ('Helvetica', 10), bg = 'white', command = lambda: cameraSelect_Win(self.master))
        self.btnSelectCam.grid(column = 0, row = 1, padx = 5, pady = 5)

        self.cameraSelected.set('Not Configured')
        self.lblCameraSelected = Label(self.cameraFrame, textvariable = self.cameraSelected, bg = 'white')
        self.lblCameraSelected.grid(column = 0, row = 2, padx = 10, pady = 5)

        # > Preview Camera
        self.lblPreview = Label(self.cameraFrame, text = 'Preview: ', font = ('Helvetica', 10), bg = 'white')
        self.lblPreview.grid(column = 1, row = 1, padx = 30, pady = 5)
                        
        if self.camNum is not None:
            cap = cv2.VideoCapture(self.camNum)

            self.lblVideoCam = Label(self.cameraFrame, bg = 'black', width = 150, height = 100)
            self.lblVideoCam.grid(column = 1, row = 2, padx = 5, pady = 5)

            self.videoStream()

        else:
            self.lblVideoCam = Label(self.cameraFrame, bg = 'black', width = 20, height = 5)
            self.lblVideoCam.grid(column = 1, row = 2, padx = 5, pady = 5)   
        
        # Buttons Save / Cancel
        self.btnSave = Button(self.btnFrame, text = 'Save', width = 20, font = ('Helvetica', 10), bg = 'white')
        self.btnSave.grid(column = 0, row = 0, padx = 10, pady = 5)

        self.btnCancel = Button(self.btnFrame, text = 'Cancel', width = 20, font = ('Helvetica', 10), bg = 'white')
        self.btnCancel.grid(column = 1, row = 0, padx = 10, pady = 5)
        

    def videoStream(self):
        global cap

        if cap is not None:
            ret, fram = cap.read()

            if ret == True:
                fram = imutils.resize(fram,width = 150, height = 95)
                fram = cv2.cvtColor(fram, cv2.COLOR_BGR2RGB)

                im = Image.fromarray(fram)
                img = ImageTk.PhotoImage(image = im)

                self.lblVideoCam.configure(image = img)
                self.lblVideoCam.img = img
                self.lblVideo.after(10, self.videoStream)
            
            else:
                self.lblVideoCam.img = ''
                cap.release()





class CameraSelect_Win():
    def __init__(self, master):
        self.master = master
        self.master.title('Inspection System - Configuration')

        self.frame = Frame(self.master, bg = 'white')
        self.frame.pack()

        # >>> Variables
        
        self.returnCameraIndexes()
        self.varlist = StringVar(value = self.items)

        # >>> GUI Settings

        self.lblInstruction = Label(self.frame, text = 'Please select your camera', font = ('Helvetica', 14), bg = 'white')
        self.lblInstruction.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)

        self.mylistbox = Listbox(self.frame, listvariable = self.varlist, width = 50)
        self.mylistbox.bind('<<ListboxSelect>>', self.curSelect)
        self.mylistbox.grid(column = 0, row = 1, padx = 5, pady = 5, rowspan = 2)
        self.varlist.set(self.items)

        self.btnSelect = Button(self.frame, text = 'Select', font = ('Helvetica', 10), bg = 'white')
        self.btnSelect.grid(column = 1, row = 1, padx = 5, pady = 5)

        self.btnRefresh = Button(self.frame, text = 'Refresh', font = ('Helvetica', 10), bg = 'white')
        self.btnRefresh.grid(column = 1, row = 2, padx = 5, pady = 5, sticky = 'n')

        self.btnCancel = Button(self.frame, text = 'Cancel', font = ('Helvetica', 10), bg = 'white')
        self.btnCancel.grid(column = 1, row = 3, padx = 5, pady = 5)



    def returnCameraIndexes(self):
        # Checks the first 10 indexes.
        index = 0
        self.items = []
        i = 10

        while i > 0:
            cap = cv2.VideoCapture(index)
            
            if cap.read()[0]:
                self.items.append(index)
                cap.release() 
            
            index += 1
            i -= 1
        return self.items

    def curSelect(self, event):
        self.value = self.mylistbox.get(self.mylistbox.curselection())
        print(self.value)
        return self.value


def config_Win(master):
    newWindow = Toplevel(master)
    app = Config_Win(newWindow)


def cameraSelect_Win(master):
    newWindow = Toplevel(master)
    app = CameraSelect_Win(newWindow)