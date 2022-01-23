import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
# https://www.kaggle.com/tawsifurrahman/covid19-radiography-database
import random
from keras.models import load_model
import numpy as np
from PIL import Image
inputmodel = load_model('cov200.h5')
random.seed()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
databasefolder = 'static'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    txt = ''
    completeadd = ""
    b=""
    p=0
    if request.method == 'POST':
        file = request.files["file"]
        whichone = request.form["radiob"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
        filelist1 = os.listdir(databasefolder)

        if whichone == "rand":
            rand_image = random.choice(filelist1)
            completeadd = os.path.join(app.config['UPLOAD_FOLDER'], rand_image)
        if whichone == "upload":
            completeadd = os.path.join(app.config['UPLOAD_FOLDER'], "save.fil")
            file.save(completeadd)
        image1 = Image.open(completeadd)
        image2 = image1.resize((260, 260))
        image3=np.zeros((1,260,260,3))
        image3[0,:,:,0]=image2
        b = inputmodel.predict(image3)
        ind = np.argmax(b[0][:])
        p=round(b[0][ind]*100,1)

        predtex = ["COVID 19 symptom", "Lung Opacity symptom", " normal lung", "Viral Pneumonia symptom"]
        txt = "Based on the modeling, X-Ray images belongs to a patient who has " + predtex[ind] + " by the probability of " + str(p) + " percent"
    return render_template("index.html", outputtext=txt, image=completeadd,x=b)


if __name__ == '__main__':
    PORT = os.getenv("PORT", 5000)
    app.run("0.0.0.0", PORT)
