import os
import shutil
from flask import Flask,request,jsonify,render_template,redirect
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename



from GetNumberPlate import DetectNumberPlate
from GetNumberPlateFromVideo import DetectNumberPlateFromVideo
from GetTheText import get_text


app=Flask(__name__)
app.config['IMAGE_UPLOADS']='Input_Images'

@app.route('/',methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
@cross_origin()
def predict_route():
    print(request)
    image=request.files['file']
    if image.filename == '':
        return redirect(request.url)
    filename=secure_filename(image.filename)
    basedir=os.path.abspath(os.path.dirname(__file__))
    image.save(os.path.join(basedir,app.config['IMAGE_UPLOADS'],filename))
    img='Input_Images'+'/'+filename
    print(img)
    if img.split('.')[1]!='mp4':
        number_plate=DetectNumberPlate(img)
        region=number_plate.get_cropped_image()
        if not os.path.exists('Output_Images'):
            os.mkdir('Output_Images')
        number_plate.save_image(img=region,filepath='Output_Images/output.png')
        text=get_text(region)
        result=text.filter_text()
        print('The number of the car is', result)
        return render_template('results.html',prediction=result)
    else:
        video=DetectNumberPlateFromVideo(img)
        video.save_frame()
        result=video.save_numberplate()
        print('The number of the car is', result)
        shutil.rmtree('Input_Video_Images')
        return render_template('results.html', prediction=result)

if __name__=='__main__':
    app.run()


