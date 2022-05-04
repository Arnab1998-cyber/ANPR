import easyocr
import numpy as np
from GetNumberPlate import DetectNumberPlate


class get_text:
    def __init__(self,image_path):
        self.image=image_path

    def get_ocr(self):
        reader=easyocr.Reader(['en'])
        ocr_result=reader.readtext(self.image)
        return ocr_result

    def get_area(self,l):
        a = np.sqrt((l[0][0] - l[1][0])** 2 + (l[0][1] - l[1][1])** 2)
        b = np.sqrt((l[0][0] - l[3][0]) ** 2 + (l[0][1] - l[3][1]) ** 2)
        return a*b

    def filter_text(self):
        result=self.get_ocr()
        print(result)
        if len(result)==2:
            area_of_first=self.get_area(l=result[0][0])
            area_of_second=self.get_area(l=result[1][0])
            if area_of_second >= area_of_first :
                if area_of_first/area_of_second <= 0.4:
                    return result[1][1]
                else:
                    return result[0][1]+''+result[1][1]
            else:
                if area_of_second/area_of_first <=0.4:
                    return result[0][1]
                else:
                    return result[0][1]+result[1][1]
        elif len(result)==1:
            return result[0][1]

