from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlFile
from pyforms.controls   import ControlText
from pyforms.controls   import ControlButton

from pytesseract import Output
import pytesseract
import argparse
import cv2

#capture screen
import pyscreenshot as ImageGrab

#capture screen by mouse
import win32gui
import win32ui
import win32con
import win32api

class ComputerVisionAlgorithm(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Computer vision algorithm example')

        self.set_margin(10)

        #Definition of the forms fields
        self._imgFile  = ControlFile('File')
        self._runbutton  = ControlButton('Run')
        self._outputfile = ControlText('Results output file')

        #Define the organization of the Form Controls
        self._formset = [
            ('_imgFile', '_runbutton'), '_outputfile'
        ]

        #Define the function that will be called when a file is selected
        self._runbutton.value = self.saveScreenShot

    def __runAction(self):

        # part of the screen
        im = ImageGrab.grab(bbox=(10, 10, 510, 510))  # X1,Y1,X2,Y2

        # save image file
        im.save('box.png')

        """Button action event"""
        self._outputfile.value = ""
        # load the input image, convert it from BGR to RGB channel ordering,
        # and use Tesseract to localize each area of text in the input image
        image = cv2.imread('box.png')
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang="eng")

        for i in range(0, len(results["text"])):
            self._outputfile.value += results["text"][i]

    def saveScreenShot(self, x,y,width,height,path):
        # grab a handle to the main desktop window
        hdesktop = win32gui.GetDesktopWindow()

        # create a device context
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)

        # create a memory based device context
        mem_dc = img_dc.CreateCompatibleDC()

        # create a bitmap object
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, width, height)
        mem_dc.SelectObject(screenshot)


        # copy the screen into our memory device context
        mem_dc.BitBlt((0, 0), (width, height), img_dc, (x, y),win32con.SRCCOPY)

        # save the bitmap to a file
        screenshot.SaveBitmapFile(mem_dc, path)
        # free our objects
        mem_dc.DeleteDC()
        win32gui.DeleteObject(screenshot.GetHandle())

if __name__ == '__main__':

    from pyforms import start_app
    start_app(ComputerVisionAlgorithm)