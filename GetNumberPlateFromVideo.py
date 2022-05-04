import os.path

import cv2
import imageio
from GetNumberPlate import DetectNumberPlate

class DetectNumberPlateVideo:
    def __init__(self,video_path):
        self.video=video_path

    def get_detections(self):
        cap=cv2.VideoCapture(self.video)
        i=0
        while True:
            i=i+1
            img=cap.read()[1]
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            print(img)
            if not os.path.exists('Input_Video_Images'):
                os.mkdir('Input_Video_Images')
            cv2.imwrite(filename='Input_video_Images\\input{}.png'.format(i),img=img)
            number_plate=DetectNumberPlate(image_path='Input_video_Images\\input{}.png'.format(i))
            image_with_np_detections=number_plate.get_detections()[1]
            if not os.path.exists('Output_Video_Images'):
                os.mkdir('Output_Video_Images')
            number_plate.save_image(img=image_with_np_detections,filepath='Output_Video_Images/output{}.png'.format(i))
            if i==10:
                break
