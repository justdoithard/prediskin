from ast import Pass
# from crypt import methods #untuk di OS non window aja
from unittest import result
from app import app
from flask import render_template, request, session, redirect, url_for
import pymysql
# from app.admin_views import admin_dashboard
import os
from werkzeug.utils import secure_filename
import time
import shutil

from flask import Flask, Response
import cv2
from datetime import datetime, date
import sys
import numpy as np
from threading import Thread
from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

from os import path
import sys
# print(sys.version)
from wheel.pep425tags import get_abbr_impl, get_impl_ver, get_abi_tag
platform = '{}{}-{}'.format(get_abbr_impl(), get_impl_ver, get_abi_tag)

accelerator = 'cu80' if path.exists('/opt/bin/nvidia-smi') else 'cpu'

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
import sklearn

from PIL import Image
from sklearn.metrics import accuracy_score

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from skimage.io import imsave, imread
from skimage.transform import resize
import numpy as np
from keras.utils import to_categorical


connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'prediskin')
cursor = connection.cursor()
app.secret_key = 'mysecretkey'

isCapture = 0

global username
print(os.listdir)

filepath = "D:\FILE\KULIAH\PPTI BCA\CAWU 4\Software Engineering\Final Project\Datasets\my_model"
model = tf.keras.models.load_model(filepath)

app.config['IMAGE_UPLOADS'] = 'D:/FILE/KULIAH/PPTI BCA/CAWU 4/Software Engineering/Final Project/app/static/img/uploads'
app.config['ALLOWED_IMAGE_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
cameraOn = 0
successCapture = 0

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

camera = None
def runcam():
    global camera
    camera = cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    global out, capture, successCapture
    while True:
        success, frame = camera.read() 
        if success:   
            if(capture == 1):
                capture=0
                basedir = os.path.abspath(os.path.dirname(__file__))
                p = os.path.join(basedir, app.config["IMAGE_UPLOADS"], 'cameraCompare.png')
                cv2.imwrite(p, frame)
                print("Captured saved!")
                successCapture = 1
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            pass

def allowed_image(filename):
    if not '.' in filename:
        return False

    ext = filename.rsplit('.', 1)[1]

    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        return False

def stopcamera():
    global camera
    camera.release()
    cv2.destroyAllWindows()

def compares(directories):
    X_test = []
    labels = ['Melanocytic Nevi', 'Melanoma', 'Normal', 'Ringworm', 'Vitiligo']
    
    image = imread(directories)/255.
    image = resize(image,(224,224))
    X_test.append(image)

    X_test = np.array(X_test)
    Y_pred = model.predict(X_test)
    y_pred = np.argmax(Y_pred, axis=1)
    print(labels[y_pred[0]])

    return  labels[y_pred[0]]

def allowed_image(filename):
    if not '.' in filename:
        return False

    ext = filename.rsplit('.', 1)[1]

    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        return False

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/task',methods=['POST','GET'])
def tasks():
    if "username" in session:
        username = session['username']
        global switch, camera
        if request.method == 'POST':
            if request.form.get('click') == 'Ambil Gambar':
                global capture
                capture=1
            elif  request.form.get('stop') == 'Stop/Start':
                if(switch==1):
                    switch = 0
                    camera.release()
                    cv2.destroyAllWindows()
                else:
                    camera = cv2.VideoCapture(0)
                    switch=1
            elif  request.form.get('rec') == 'Start/Stop Recording':
                global rec, out
                rec = not rec
        elif request.method=='GET':
            return redirect(url_for('camera_confirm'))
        return redirect(url_for('camera_confirm'))
    else:
        return redirect(url_for('login'))

@app.route('/prediction/camera/confirm', methods=['GET', 'POST'])
def camera_confirm():
    if "username" in session:
        username = session['username']
        global cameraOn, successCapture
        # if cameraOn == 1:
        # time.sleep(5)
        cameraOn = 0
        # while successCapture == 0:
        #     print('masih nyoba')
        #     pass
        # time.sleep(10)
        successCapture = 0
        stopcamera()
        return render_template('public/camera-confirm.html', usernames = username, role = session['role'])
    else:
        return redirect(url_for('login'))

@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    if cameraOn == 1:
        stopcamera()

    if "username" in session:
        return render_template('public/prediction.html', username = session['username'], role = session['role'])
    else:
        return redirect(url_for('login'))

@app.route('/prediction/upload', methods=["GET", "POST"])
def upload():
    
    if "username" in session:
        return render_template('public/upload.html', username = session['username'], role = session['role'])
    else:
        return redirect(url_for('login'))

@app.route('/prediction/camera', methods=["GET", "POST"])
def camera():
    if "username" in session:
        global cameraOn
        cameraOn = 1
        if cameraOn == 1:
            runcam()
        return render_template('public/camera.html', username = session['username'], role = session['role'])
    else:
        return redirect(url_for('login'))

@app.route('/upload_result', methods=["GET", "POST"])
def get_upload_result():
    if "username" in session:
        msg = ''
        if request.method == "POST":
            basedir = os.path.abspath(os.path.dirname(__file__))

            image = request.files['image']
            filename = 'uploadCompare.png'
            directories = os.path.join(basedir, app.config["IMAGE_UPLOADS"], filename)
            image.save(directories)
            print("Image saved")
            results = compares(directories) 
            res = results
            img = ''

            print(res)

            diseaseID = cursor.execute('SELECT diseaseID FROM disease WHERE diseaseName = %s', (res))
            diseaseID = cursor.fetchone()
            diseaseID = diseaseID[0]

            userID = session['id']
            accuracy = 81
            # predicted_at = datetime.now()

            cursor.execute("INSERT INTO prediction (diseaseID, userID, img, accuracy) VALUES (%s, %s, %s, %s)", (diseaseID, userID, img, accuracy))
            connection.commit()

            prediction_id = cursor.execute("SELECT predictionID FROM prediction ORDER BY predictionID DESC LIMIT 1")
            prediction_id = cursor.fetchone()
            prediction_id = prediction_id[0]

            predicted_at = cursor.execute("SELECT predicted_at FROM prediction WHERE predictionID = %s", prediction_id)
            predicted_at = cursor.fetchone()
            predicted_at = str(predicted_at[0])
            to_remov = ["-",":","_"," "]
            for char in to_remov:
                predicted_at = predicted_at.replace(char, "")

            img = "user_"+str(userID)+"_"+predicted_at+".png"
            directories2 = os.path.join(basedir, app.config["IMAGE_UPLOADS"], img)
            shutil.copyfile(directories, directories2)
            # os.rename(directories, directories2)
            # img_pred = str("url_for( 'static', filename='img/uploads/"+img+"')")
            img_pred = "./static/img/uploads/"+img

            cursor.execute("UPDATE prediction SET img = %s WHERE predictionID = %s", (img, prediction_id))
            connection.commit()

            disease_data = cursor.execute('SELECT * FROM disease WHERE diseaseID = %s', (diseaseID))
            disease_data = cursor.fetchone()

            return render_template('public/result.html', res = res, img_pred = img_pred, accuracy = accuracy, username = session['username'], role = session['role'], disease_data = disease_data)
        return render_template('public/prediction.html', msg = "Upload File Error!", username = session['username'], role = session['role'])
    return redirect(url_for('login'))

@app.route('/camera_result', methods=["GET", "POST"])
def get_camera_result():
    if "username" in session:
        msg = ''
        if request.method == "POST":
            basedir = os.path.abspath(os.path.dirname(__file__))

            filename = 'cameraCompare.png'
            directories = os.path.join(basedir, app.config["IMAGE_UPLOADS"], filename)
            results = compares(directories)
            res = results
            img = ''
            print(res)

            diseaseID = cursor.execute('SELECT diseaseID FROM disease WHERE diseaseName = %s', (res))
            diseaseID = cursor.fetchone()
            diseaseID = diseaseID[0]

            userID = session['id']
            accuracy = 81
            # predicted_at = datetime.now()

            cursor.execute("INSERT INTO prediction (diseaseID, userID, img, accuracy) VALUES (%s, %s, %s, %s)", (diseaseID, userID, img, accuracy))
            connection.commit()

            prediction_id = cursor.execute("SELECT predictionID FROM prediction ORDER BY predictionID DESC LIMIT 1")
            prediction_id = cursor.fetchone()
            prediction_id = prediction_id[0]

            predicted_at = cursor.execute("SELECT predicted_at FROM prediction WHERE predictionID = %s", prediction_id)
            predicted_at = cursor.fetchone()
            predicted_at = str(predicted_at[0])
            to_remov = ["-",":","_"," "]
            for char in to_remov:
                predicted_at = predicted_at.replace(char, "")

            img = "user_"+str(userID)+"_"+predicted_at+".png"
            directories2 = os.path.join(basedir, app.config["IMAGE_UPLOADS"], img)
            shutil.copyfile(directories, directories2)
            # os.rename(directories, directories2)
            # img_pred = str("url_for( 'static', filename='img/uploads/"+img+"')")
            img_pred = "./static/img/uploads/"+img
            

            cursor.execute("UPDATE prediction SET img = %s WHERE predictionID = %s", (img, prediction_id))
            connection.commit()
            
            disease_data = cursor.execute('SELECT * FROM disease WHERE diseaseID = %s', (diseaseID))
            disease_data = cursor.fetchone()

            return render_template('public/result.html', res = res, img_pred = img_pred, accuracy = accuracy, username = session['username'], role = session['role'], disease_data = disease_data)
        return render_template('public/prediction.html', msg = "Upload File Error!", username = session['username'], role = session['role'])
    return redirect(url_for('login'))

@app.route('/information', methods=["GET", "POST"])
def information():
    if "username" in session :
        return render_template('public/information.html', username = session['username'], role = session['role'])
    else:
        return render_template('public/information.html')

@app.route('/information/detail', methods=["GET", "POST"])
def infodetails():
    if request.method == "POST":
        diseaseID = request.form['diseaseID']
        if diseaseID == 0 :
            return render_template('public/infodetails_def.html')

        disease_data = cursor.execute('SELECT * FROM disease WHERE diseaseID = %s', (diseaseID))
        disease_data = cursor.fetchone()

        if "username" in session :
            return render_template('public/infodetails.html', username = session['username'], role = session['role'], disease_data = disease_data)
        else:
            return render_template('public/infodetails.html', disease_data = disease_data)
        
    else:
        return render_template('public/infodetails_def.html')

@app.route('/data/prediction/verify', methods=["GET", "POST"])
def verify():
    if "username" in session :
        if session['role'] == "doctor":
            doctorID = cursor.execute('SELECT doctorID FROM doctor d JOIN user u ON u.userID = d.doctorID WHERE d.userID = %s', (session['id']))
            doctorID = cursor.fetchone()
            doctorID = doctorID[0]
            predictionID = request.form['predictionID']
            result = request.form['result']
            diseaseID = request.form['diseaseID']

            cursor.execute('INSERT INTO verification (predictionID, doctorID, result, disease_verID) VALUES (%s, %s, %s, %s)', (predictionID, doctorID, result, diseaseID))
            connection.commit()
            cursor.execute('UPDATE prediction SET verified = 1 WHERE predictionID = %s', (predictionID))
            connection.commit()

        return redirect(url_for('show_prediction'))
    else :
        return redirect(url_for('login'))

@app.route('/data/verification', methods=["GET", "POST"])
def show_verification():
    if "username" in session :
        if session['role'] == "patient":
            page =  request.args.get(get_page_parameter(), type=int, default=1)
            limit = 10 #perpage
            offset = page*limit - limit

            predictions = cursor.execute('SELECT DISTINCT p.predictionID, p.diseaseID, p.userID, p.img, p.accuracy, p.predicted_at, p.verified FROM prediction p JOIN verification v ON v.predictionID = p.predictionID WHERE p.userID = %s ORDER BY p.predictionID DESC LIMIT %s OFFSET %s', (session['id'], limit, offset))
            predictions = cursor.fetchall()

            pred_diseases = cursor.execute('SELECT DISTINCT d.diseaseName, p.predictionID FROM disease d JOIN prediction p ON p.diseaseID = d.diseaseID JOIN verification v ON p.predictionID = v.predictionID  WHERE p.userID = %s ORDER BY p.predictionID DESC LIMIT %s OFFSET %s', (session['id'], limit, offset))
            pred_diseases = cursor.fetchall()

            results = cursor.execute('SELECT DISTINCT p.predictionID, p.diseaseID, p.userID, p.img, p.accuracy, p.predicted_at, p.verified FROM prediction p JOIN verification v ON v.predictionID = p.predictionID WHERE p.userID = %s ORDER BY p.predictionID DESC', (session['id']))
            results = cursor.fetchall()
            total = len(results)

            ver_doctors = cursor.execute('SELECT u.name, di.diseaseName, p.predictionID, v.result FROM user u JOIN doctor d ON d.userID = u.userID JOIN verification v ON v.doctorID = d.doctorID JOIN prediction p ON p.predictionID = v.predictionID JOIN disease di ON v.disease_verID = di.diseaseID WHERE p.userID = %s ORDER BY p.predictionID DESC', (session['id']))
            ver_doctors = cursor.fetchall()

            pagination = Pagination(page=page, per_page=limit, total=total, record_name='verifikasi', css_framework='bootstrap4' ,bs_version=5 , show_single_page=False, anchor='result', link_size=30)

            return render_template('public/verification-patient.html', username = session['username'], role = session['role'], predictions = predictions, lenPredictions = len(predictions), ver_doctors = ver_doctors, pred_diseases = pred_diseases, pagination = pagination)
        elif session['role'] == "doctor":
            page =  request.args.get(get_page_parameter(), type=int, default=1)
            limit = 10 #perpage
            offset = page*limit - limit

            doctorID = cursor.execute('SELECT doctorID FROM doctor d JOIN user u ON u.userID = d.doctorID WHERE d.userID = %s', (session['id']))
            doctorID = cursor.fetchone()
            doctorID = doctorID[0]
            
            predictions = cursor.execute('SELECT p.predictionID, p.diseaseID, p.userID, p.img, p.accuracy, p.predicted_at, p.verified FROM prediction p JOIN verification v ON v.predictionID = p.predictionID WHERE v.doctorID = %s ORDER BY v.verificationID DESC LIMIT %s OFFSET %s', (doctorID, limit, offset))
            predictions = cursor.fetchall()

            pred_diseases = cursor.execute('SELECT d.diseaseName FROM disease d JOIN prediction p ON p.diseaseID = d.diseaseID JOIN verification v ON p.predictionID = v.predictionID WHERE v.doctorID = %s ORDER BY v.verificationID DESC LIMIT %s OFFSET %s', (doctorID, limit, offset))
            pred_diseases = cursor.fetchall()

            results = cursor.execute('SELECT p.predictionID, p.diseaseID, p.userID, p.img, p.accuracy, p.predicted_at, p.verified FROM prediction p JOIN verification v ON v.predictionID = p.predictionID WHERE v.doctorID = %s ORDER BY v.verificationID DESC', (doctorID))
            results = cursor.fetchall()
            total = len(results)

            ver_doctors = cursor.execute('SELECT u.name, di.diseaseName, p.predictionID, v.result FROM user u JOIN doctor d ON d.userID = u.userID JOIN verification v ON v.doctorID = d.doctorID JOIN prediction p ON p.predictionID = v.predictionID JOIN disease di ON v.disease_verID = di.diseaseID WHERE p.predictionID IN (SELECT pr.predictionID FROM prediction pr JOIN verification ve ON ve.predictionID = pr.predictionID WHERE ve.doctorID = %s) ORDER BY v.verificationID DESC', (doctorID))
            ver_doctors = cursor.fetchall()

            pagination = Pagination(page=page, per_page=limit, total=total, record_name='verifikasi', css_framework='bootstrap4' ,bs_version=5 , show_single_page=False, anchor='result', link_size=30)

            return render_template('public/verification-doctor.html', username = session['username'], role = session['role'], predictions = predictions, lenPredictions = len(predictions), ver_doctors = ver_doctors, pred_diseases = pred_diseases, pagination = pagination)
    else:
        return redirect(url_for('login'))

@app.route('/data/prediction', methods=["GET", "POST"])
def show_prediction():
    if "username" in session :
        if session['role'] == "patient":
            page =  request.args.get(get_page_parameter(), type=int, default=1)
            limit = 10 #perpage
            offset = page*limit - limit

            results = cursor.execute('SELECT * FROM prediction WHERE userID = %s ORDER BY predictionID DESC', (session['id']))
            results = cursor.fetchall()
            total = len(results)

            predictions = cursor.execute('SELECT * FROM prediction WHERE userID = %s ORDER BY predictionID DESC LIMIT %s OFFSET %s', (session['id'], limit, offset))
            predictions = cursor.fetchall()

            pred_diseases = cursor.execute('SELECT d.diseaseName FROM disease d JOIN prediction p ON p.diseaseID = d.diseaseID WHERE p.userID = %s ORDER BY p.predictionID DESC LIMIT %s OFFSET %s', (session['id'], limit, offset))
            pred_diseases = cursor.fetchall()

            pagination = Pagination(page=page, per_page=limit, total=total, record_name='prediksi', css_framework='bootstrap4' ,bs_version=5 , show_single_page=False, anchor='result', link_size=30)

            return render_template('public/prediction-patient.html', username = session['username'], role = session['role'], predictions = predictions, lenPredictions = len(predictions), pred_diseases = pred_diseases, pagination = pagination)
        
        elif session['role'] == "doctor":
            page =  request.args.get(get_page_parameter(), type=int, default=1)
            limit = 10 #perpage
            offset = page*limit - limit

            predictions = cursor.execute('SELECT * FROM prediction WHERE verified = 0 ORDER BY predictionID DESC LIMIT %s OFFSET %s', (limit, offset))
            predictions = cursor.fetchall()

            results = cursor.execute('SELECT * FROM prediction WHERE verified = 0 ORDER BY predictionID DESC')
            results = cursor.fetchall()
            total = len(results)

            pred_names = cursor.execute('SELECT d.diseaseName, u.name FROM disease d JOIN prediction p ON p.diseaseID = d.diseaseID JOIN user u ON u.userID = p.userID WHERE p.verified = 0 ORDER BY p.predictionID DESC LIMIT %s OFFSET %s', (limit, offset))
            pred_names = cursor.fetchall()

            diseases = cursor.execute('SELECT * FROM disease')
            diseases = cursor.fetchall()

            pagination = Pagination(page=page, per_page=limit, total=total, record_name='prediksi', css_framework='bootstrap4' ,bs_version=5 , show_single_page=False, anchor='result', link_size=30)

            return render_template('public/prediction-doctor.html', username = session['username'], role = session['role'], predictions = predictions, lenPredictions = len(predictions), pred_names = pred_names, diseases = diseases, pagination = pagination)
    else:
        return redirect(url_for('login'))

@app.route('/')
def index():
    
    if "username" in session:
        return redirect(url_for('home', username = session['username'], role = session['role'], **request.args))
    else:
        return render_template('public/index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    
    msg = ''
    # print(session['username'])
    if "username" in session :
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']

        id1 = cursor.execute("SELECT userID FROM user WHERE email = %s", (email))
        id1 = cursor.fetchone()
        if id1 == None:
            msg = 'Incorrect email/password!'
            return render_template('public/login.html', err = 1, msg = "Email atau kata sandi salah!")
        else :
            id = id1[0]
            password = request.form['password']
            cursor.execute('SELECT * FROM user WHERE userID = %s AND password = %s', (id, password))
            account = cursor.fetchone()
            print(account)

            if account:
                # name1 = cursor.execute('SELECT SUBSTR(name, 1, POSITION(' ' IN name)-1) AS Nickname FROM user WHERE userID = %s AND password = %s', (id, password))
                name1 = cursor.execute('SELECT name FROM user WHERE userID = %s AND password = %s', (id, password))
                name1 = cursor.fetchone()

                # if name1 == '' :
                name_arr = name1[0].split()
                name = name_arr[0]
                print(name)
                role = cursor.execute('SELECT role FROM user WHERE userID = %s AND password = %s', (id, password))
                role = cursor.fetchone()

                session['email'] = email
                session['id'] = id
                session['username'] = name
                session['role'] = role[0]
            
                session['loggedin'] = True
                #baru sampe sini (bingung mau pake email atau username)
                # if role[0] == 1:
                #     return redirect(url_for('admin_dashboard', username = username))
                # else:
                #     print('masuk')
                #     return redirect(url_for('home', username = username,**request.args))
                print('masuk')
                return redirect(url_for('home', username = name, role = role, **request.args))
            else:
                return render_template('public/login.html', err = 1, msg = "Akun belum terdaftar!")
    return render_template('public/login.html',msg=msg)

@app.route('/home', methods=['GET','POST'])
def home():
    
    if "username" in session:
        return render_template('public/index.html', username = session['username'], role = session['role'])
    else:
        return redirect(url_for('index'))

@app.route('/signUp', methods=["GET", "POST"])
def signUp():
    
    if request.method == "POST":
        role = request.form['user']
        print(role)
        if role == "doctor":
            return render_template('public/signUpDoctor1.html', role = role)
        elif role == "patient":
            return render_template('public/signUpPublic1.html', role = role)

    return render_template("public/signUp.html")

@app.route('/signUpDoctor1', methods=["GET", "POST"])
def signUpDoctor1():
    
    if request.method == "POST":
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['date']
        role = request.form['role']

        if name == '' or gender == '' or dob == '':
            return render_template("public/signUpDoctor1.html", err = 1, role = role)
        elif dob > date.today():
            return render_template("public/signUpDoctor1.html", err = 1, role = role)
        return render_template('public/signUpDoctor2.html', role = role, name = name, gender = gender, dob = dob)
    return render_template("public/signUpDoctor1.html")

@app.route("/signUpDoctor2", methods=["GET", "POST"])
def signUpDoctor2():
    
    msg = ''
    if request.method == "POST":
        email = request.form['email']
        phoneNum = request.form['phone']
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['date']
        role = request.form['role']

        account_exist = cursor.execute("SELECT * FROM user WHERE email = %s", (email))
        account_exist = cursor.fetchone()

        if account_exist:
            msg = "Account with this email already exist"
            return render_template("public/signUpDoctor2.html", msg = msg)
        else:
            return render_template('public/signUpDoctor3.html', role = role, name = name, gender = gender, dob = dob, email = email, phoneNum = phoneNum)
        
    return render_template("public/signUpDoctor2.html")

@app.route("/signUpDoctor3", methods=["GET", "POST"])
def signUpDoctor3():
    
    if request.method == "POST":
        nik = request.form['nik']
        job = request.form['job']
        email = request.form['email']
        phoneNum = request.form['phone']
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['date']
        role = request.form['role']

        account_exist = cursor.execute("SELECT * FROM doctor WHERE nik = %s", (nik))
        account_exist = cursor.fetchone()

        if account_exist:
            msg = "Account with this identity number already exist"
            return render_template("public/signUpDoctor3.html", msg = msg)
        else:
            return render_template('public/signUpDoctor4.html', role = role, name = name, gender = gender, dob = dob, email = email, phoneNum = phoneNum, nik = nik, job = job)

    return render_template("public/signUpDoctor3.html")

@app.route("/signUpDoctor4", methods=["GET", "POST"])
def signUpDoctor4():
    
    if request.method == "POST":
        hostName = request.form['hostName']
        hostAdd = request.form['hostAdd']
        nik = request.form['nik']
        job = request.form['job']
        email = request.form['email']
        phoneNum = request.form['phone']
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['date']
        role = request.form['role']

        return render_template('public/signUpDoctor5.html', role = role, name = name, gender = gender, dob = dob, email = email, phoneNum = phoneNum, nik = nik, job = job, hostName = hostName, hostAdd = hostAdd)
    return render_template("public/signUpDoctor4.html")

@app.route("/signUpDoctor5", methods=["GET", "POST"])
def signUpDoctor5():
    
    if request.method == "POST":
        password = request.form['password']
        hostName = request.form['hostName']
        hostAdd = request.form['hostAdd']
        nik = request.form['nik']
        job = request.form['job']
        email = request.form['email']
        phoneNum = request.form['phone']
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['date']
        role = request.form['role']

        return render_template('public/signUpDoctor6.html', role = role, name = name, gender = gender, dob = dob, email = email, phoneNum = phoneNum, nik = nik, job = job, hostName = hostName, hostAdd = hostAdd, password = password)
    return render_template("public/signUpDoctor5.html")

@app.route("/signUpDoctor6", methods=["GET", "POST"])
def signUpDoctor6():
    
    if request.method == "POST":
        password = request.form['password']
        hostName = request.form['hostName']
        hostAdd = request.form['hostAdd']
        nik = request.form['nik']
        job = request.form['job']
        email = request.form['email']
        phoneNum = request.form['phone']
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['date']
        role = request.form['role']
        usernames = name.split()
        username = usernames[0]

        cursor.execute("INSERT INTO user (userID, name, email, password, role, phone, dob, gender) VALUES ('', %s, %s, %s, %s, %s, %s, %s)", (name, email, password, role, phoneNum, dob, gender))
        connection.commit()
        userIDs = cursor.execute("SELECT userID FROM user WHERE email = %s", (email))
        userIDs = cursor.fetchone()
        userID = userIDs[0]

        cursor.execute("INSERT INTO doctor (doctorID, userID, position, nik, hospitalName, hospitalAddress) VALUES ('', %s, %s, %s, %s, %s)", (userID, job, nik, hostName, hostAdd))
        connection.commit()

        session['email'] = email
        session['id'] = userID
        session['username'] = username
        session['role'] = role[0]

        return redirect(url_for('home', username = session['username'], role = session['role'], **request.args))
    return render_template("public/signUpDoctor6.html")

@app.route('/signUpPublic1', methods=["GET", "POST"])
def signUpPublic1():
    
    if request.method == "POST":
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['date']
        role = request.form['role']

        return render_template('public/signUpPublic2.html', role = role, name = name, gender = gender, dob = dob)
    return render_template("public/signUpPublic1.html")

@app.route("/signUpPublic2", methods=["GET", "POST"])
def signUpPublic2():
    
    msg = ''
    if request.method == "POST":
        email = request.form['email']
        phoneNum = request.form['phone']
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['date']
        role = request.form['role']

        account_exist = cursor.execute("SELECT * FROM user WHERE email = %s", (email))
        account_exist = cursor.fetchone()

        if account_exist:
            msg = "Account with this email already exist"
            return render_template("public/signUpPublic2.html", msg = msg)
        else:
            return render_template('public/signUpPublic3.html', role = role, name = name, gender = gender, dob = dob, email = email, phoneNum = phoneNum)
        
    return render_template("public/signUpPublic2.html")

@app.route("/signUpPublic3", methods=["GET", "POST"])
def signUpPublic3():
    
    if request.method == "POST":
        password = request.form['password']
        email = request.form['email']
        phoneNum = request.form['phone']
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['date']
        role = request.form['role']

        return render_template('public/signUpPublic4.html', role = role, name = name, gender = gender, dob = dob, email = email, phoneNum = phoneNum, password = password)
    return render_template("public/signUpPublic3.html")

@app.route("/signUpPublic4", methods=["GET", "POST"])
def signUpPublic4():
    
    if request.method == "POST":
        password = request.form['password']
        email = request.form['email']
        phoneNum = request.form['phone']
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['date']
        role = request.form['role']
        usernames = name.split()
        username = usernames[0]

        cursor.execute("INSERT INTO user (userID, name, email, password, role, phone, dob, gender) VALUES ('', %s, %s, %s, %s, %s, %s, %s)", (name, email, password, role, phoneNum, dob, gender))
        connection.commit()
        userIDs = cursor.execute("SELECT userID FROM user WHERE email = %s", (email))
        userIDs = cursor.fetchone()
        userID = userIDs[0]

        session['email'] = email
        session['id'] = userID
        session['username'] = username
        session['role'] = role[0]

        return redirect(url_for('home', username = session['username'], role = session['role'], **request.args))
    
    return render_template("public/signUpPublic4.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" in session:
        data_user = cursor.execute('SELECT name, gender, dob, email, password, phone FROM user WHERE userID = %s', session['id'])
        data_user = cursor.fetchone()

        numOfPrediction = cursor.execute('SELECT * FROM prediction WHERE userID = %s', session['id'])
        numOfPrediction = cursor.fetchone()
        if numOfPrediction != None:
            numOfPrediction = len(numOfPrediction)
        else:
            numOfPrediction = 0

        numOfVerification = cursor.execute('SELECT * FROM verification v JOIN prediction p ON p.predictionID = v.predictionID WHERE p.userID = %s', session['id'])
        numOfVerification = cursor.fetchone()
        if numOfVerification != None:
            numOfVerification = len(numOfVerification)
        else:
            numOfVerification = 0

        numOfNormal = cursor.execute('SELECT * FROM verification v JOIN prediction p ON p.predictionID = v.predictionID WHERE p.userID = %s AND v.disease_verID = 1', session['id'])
        numOfNormal = cursor.fetchone()
        if numOfNormal != None:
            numOfNormal = len(numOfNormal)
        else:
            numOfNormal = 0

        return render_template("public/profile.html", username = session['username'], role = session['role'], data_user = data_user, numOfPrediction = numOfPrediction, numOfVerification = numOfVerification, numOfNormal = numOfNormal)
    return redirect(url_for('login'))

@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if "username" in session:
        data_user = cursor.execute('SELECT name, gender, dob, email, password, phone FROM user WHERE userID = %s', session['id'])
        data_user = cursor.fetchone()

        if request.method == "POST":
            name = request.form['fullname']
            gender = request.form['gender']
            dob = request.form['date']
            phoneNum = request.form['phone']
            email = request.form['email']
            password = request.form['password']
            newpassword = request.form['newpassword']
            usernames = name.split()
            username = usernames[0]
            
            cursor.execute('SELECT * FROM user WHERE userID = %s AND password = %s', (id, password))
            account = cursor.fetchone()
        
            if account:
                cursor.execute('UPDATE user SET name = %s, gender = %s, dob = %s, phone = %s, email = %s, password = %s', {name, gender, dob, phone, email, password})
                cursor.commit()

                session['email'] = email
                session['username'] = username

                return redirect(url_for('profile'))
            else:
                msg = "Password salah!"
                return render_template("public/editProfile.html", username = session['username'], role = session['role'], msg = msg, data_user = data_user)
        else:
            return render_template("public/editProfile.html", username = session['username'], role = session['role'], data_user = data_user)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))






