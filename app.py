from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlFile
from pyforms.controls   import ControlText
from pyforms.controls   import ControlButton
from pyforms.controls   import ControlLabel

from pytesseract import Output
import pytesseract
import argparse
import cv2

#capture screen by mouse
import win32gui
import win32ui
import win32con
import win32api

class ComputerVisionAlgorithm(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Tiểu luận 2020 - Trần Hữu Hiền')

        self.set_margin(10)

        #Definition of the forms fields
        self._controlLabel = ControlLabel('Tiểu luận 2020 - Trần Hữu hiền')
        self._imgFile  = ControlFile('Chọn file')
        self._runbutton  = ControlButton('Chọn')
        self._outputfile = ControlText('Chữ trong hình')

        #Define the organization of the Form Controls
        self._formset = [
             '_controlLabel', ('_imgFile', '_runbutton'), '_outputfile'
        ]

        #Define the function that will be called when a file is selected
        self._runbutton.value = self.__runAction

    def __runAction(self):
        """Button action event"""
        #Empty output
        self._outputfile.value = ""

        #read input image
        image = cv2.imread(self._imgFile.value)

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang="jpn")

        for i in range(0, len(results["text"])):
            self._outputfile.value += results["text"][i]
            # extract the bounding box coordinates of the text region from
            # the current result
            x = results["left"][i]
            y = results["top"][i]
            w = results["width"][i]
            h = results["height"][i]

            # extract the OCR text itself along with the confidence of the
            # text localization
            text = results["text"][i]
            conf = int(results["conf"][i])

            # strip out non-ASCII text so we can draw the text on the image
            # using OpenCV, then draw a bounding box around the text along
            # with the text itself
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Image", image)

if __name__ == '__main__':

    from pyforms import start_app
    start_app(ComputerVisionAlgorithm)