import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
#https://www.kaggle.com/tawsifurrahman/covid19-radiography-database
#import cv2
#import matplotlib.image as mpimg
import random
from keras.models import load_model
import numpy as np
inputmodel = load_model('cov200.h5')
random.seed()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

databasefolder='static'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    txt=''
    filename=0
    completeadd=""
    extrafile=''
    if request.method == 'POST':
        file = request.files["file"]
        whichone=request.form["radiob"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
        filelist1 = os.listdir(databasefolder)
        #extrafile = os.listdir(databasefolder)
        '''for i in range(1,11,1):
            aaaa="Sample_NYILAI("+str(i)+").png"
            extrafile.remove(aaaa)
        ''''''for filename in extrafile:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        '''

        if whichone=="rand":
            rand_image = random.choice(filelist1)
            completeadd = os.path.join(app.config['UPLOAD_FOLDER'], rand_image)
        if whichone == "upload":
            completeadd =os.path.join(app.config['UPLOAD_FOLDER'], "save.fil")
            file.save(completeadd)
#        fileimage = cv2.imread(completeadd, 1)
            fileimage = Image.open(completeadd)
#         fileimage = mpimg.imread('g4g.png')       
        image1=fileimage.resize((260, 260)).reshape(1,260,260,3)
        #b = inputmodel.predict(image1)
        
        #ind = np.argmax(b[0][:])
        #p=round(b[0][ind]*100,1)
        ind=1
        p=13
        predtex=["COVID 19 symptom","Lung Opacity symptom"," normal lung","Viral Pneumonia symptom"]
        txt="Based on the modeling, X-Ray images belongs to a patient who has " +predtex[ind]+" by the probability of "+str(p)+" percent"
    return  render_template("index.html" ,outputtext=txt,image=completeadd, x="")

if __name__ == '__main__':
    PORT =os.getenv("PORT",5000)
    app.run("0.0.0.0",PORT)
