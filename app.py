from crypt import methods
import urllib.request
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import cv2
import face_recognition
import os

app = Flask(__name__)

def saveImages(user_url, aadhar_url):
    urllib.request.urlretrieve(user_url, "./static/Images/userimage.jpg")
    urllib.request.urlretrieve(aadhar_url, "./static/Images/aadharimage.jpg")
    print("yes called")
    return

@app.route('/', methods=['GET', 'POST'])
def main():
    return "Its working fine"

@app.route('/face-auth', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        body = request.json
        user_url = body['userurl']
        aadhar_url = body['aadharurl']
        saveImages(user_url, aadhar_url)
        # userImgURL = request.form.get('userImg')
        #user_url = "https://m.economictimes.com/thumb/msid-73295898,width-1200,height-900,resizemode-4,imgsize-187943/dhoni.jpg"
        # aadharImgURL = request.form.get('aadharImg')
        #aadhar_url = "https://c.ndtvimg.com/2020-07/m7opt04g_ms-dhoni-afp_625x300_06_July_20.jpg"
        if user_url is None:
            return jsonify({"error": "No Userimage uploaded"}), 400
        if aadhar_url is None:
            return jsonify({"error": "No aadharImage uploaded"}), 400

        saveImages(user_url, aadhar_url)

        userImage = face_recognition.load_image_file("static/Images/rakesh1.jpg")
        userImage = cv2.cvtColor(userImage, cv2.COLOR_BGR2RGB)
        lokashi1 = face_recognition.face_locations(userImage)[0]
        encodelokasi1 = face_recognition.face_encodings(userImage)[0]
        kotakwajha1 = cv2.rectangle(userImage, (lokashi1[3], lokashi1[0]), (lokashi1[1], lokashi1[2]), (255, 0, 0), 2)

        aadharImg = face_recognition.load_image_file("static/Images/rakesh2.jpg")
        aadharImg = cv2.cvtColor(aadharImg, cv2.COLOR_BGR2RGB)
        lokashi2 = face_recognition.face_locations(aadharImg)[0]
        encodelokasi2 = face_recognition.face_encodings(aadharImg)[0]
        kotakwajha2 = cv2.rectangle(aadharImg, (lokashi2[3], lokashi2[0]), (lokashi2[1], lokashi2[2]), (255, 0, 0), 2)

        hasil = face_recognition.compare_faces([encodelokasi1], encodelokasi2)
        persamann = face_recognition.face_distance([encodelokasi1], encodelokasi2)  

        print(hasil, persamann)    
        
        os.remove("./static/Images/userimage.jpg")
        os.remove("./static/Images/aadharimage.jpg")
        if hasil[0] == True:
            return jsonify({"mached": True}), 200
        else:
            return jsonify({"mached": False}), 200   


if __name__ == '__main__':
    app.run(debug=True, port=8008)