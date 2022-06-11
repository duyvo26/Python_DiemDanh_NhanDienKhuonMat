import cv2
import numpy as np
import os 
#sql
import ketnoi
#sql
import os 
from time import sleep
# audio
import audio
# audio
from datetime import date



def NhanDien():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read('trainer/trainer.yml')
    except:
        audio.play("Vui lòng thêm thông tin sinh viên")
        return
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    cam = cv2.VideoCapture(0)
    cam.set(3, 1920)
    cam.set(4, 1080)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    while True:
        ret, img =cam.read()
        img = cv2.flip(img, 1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.3,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            if (confidence < 25):
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            today = "_"+date.today().strftime("%x")
            cv2.putText(img, str(id) + str(today), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            mssv = str(id)
            if(mssv != 'unknown'):
                tensv = ketnoi.LayTenSV(mssv)
                if tensv != False:
                    if tensv == "None":
                        audio.play("Không tìm thấy tên bạn trên danh sách sinh viên")
                    else:
                        str_noidung = str(tensv) + str(' xác nhận điểm danh')
                        cv2.putText(img, str_noidung, (x+10,y-25), font, 1, (255,255,255), 2)
                        ketnoi.DiemDanh(mssv)
                        audio.play(str_noidung)

        cv2.imshow('Diem danh',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    cam.release()
    cv2.destroyAllWindows()
