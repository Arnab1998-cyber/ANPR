import os
import re
import cv2
import shutil
from GetNumberPlate import DetectNumberPlate
from GetTheText import get_text

class DetectNumberPlateFromVideo:
    def __init__(self,video_path):
        self.video=video_path

    def save_frame(self):
        cap=cv2.VideoCapture(self.video)
        i=0
        while True:
            i=i+1
            ret,img=cap.read()
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if not os.path.exists('Input_Video_Images'):
                os.mkdir('Input_Video_Images')
            if ret == False:
                break
            if i >= 70 and (i%10==0):
                cv2.imwrite(filename='Input_video_Images\\input{}.png'.format(i),img=img)


    def extract_number_plate_from_frame(self, image):
        region=cv2.imread(image)
        text=get_text(region)
        ocr_result=text.get_ocr()
        result=text.filter_text()
        print(result)
       # result = result.replace('\n', '').replace(' ', '')
       # result = re.sub('\W+', '', result)
        #if len(result) > 0:
         #   mystates = ['AP', 'AR', 'AS', 'BR', 'CG', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'MP',
          #              'MH',
           #             'MN', 'ML', 'MZ', 'NL', 'OD', 'PB', 'RJ', 'SK', 'TN', 'TS', 'TR', 'UA', 'UK', 'UP',
            #            'WB',
             #           'AN', 'CH', 'DN', 'DD', 'DL', 'LD', 'PY']
          #  for word in mystates:
           #     if (word in result):
            #        res = re.findall(word + "[0-9]{1,2}\s*[A-Z]{1,2}\s*[0-9]{1,4}\s*]?", result)
             #       if (len(res) > 0):
              #          return (res[0])
        return result




    def save_numberplate(self):
        l=[]
        i=0
        for image in os.listdir('Input_Video_Images'):
            print('process image', image)
            obj=DetectNumberPlate(os.path.join('Input_Video_Images',image))
            detections,image_np_with_detections=obj.get_detections()
            score=list(filter(lambda x: x > 0.6, detections['detection_scores']))
            print(score)
            if len(score) > 0:
                region=obj.get_cropped_image()
                if not os.path.exists('Output_Video_Images'):
                    os.mkdir('Output_Video_Images')
                path=os.path.join('Output_Video_Images',image)
                obj.save_image(img=region, filepath=path)
                os.remove(os.path.join('Input_Video_Images',image))
                result=self.extract_number_plate_from_frame(image=path)
                print(i,result,len(result))
                if len(result)>= 6:
                    i=i+1
                    if '@' in result:
                        result.replace('@','O')
                    l.append(result)
                if i==3:
                    l.sort(key=len)
                    return l[-1]
            else:
                os.remove(os.path.join('Input_Video_Images',image))






