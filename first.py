import os
import numpy as np
import cv2

from PIL import Image
from PIL import ImageGrab
import sys 

import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator

import time
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# path info
original_path = "C:/Users/dbsgh/Desktop/hackathon/org_i/"
test_path = "C:/Users/dbsgh/Desktop/hackathon/crop_i/"
crop_path = "C:/Users/dbsgh/Desktop/hackathon/crop_i/crop/"
resize_path = "C:/Users/dbsgh/Desktop/hackathon/resize_i/"
model_path = "C:/Users/dbsgh/Desktop/hackathon/model/model.h5"
size_file = "C:/Users/dbsgh/Desktop/hackathon/size/size.PNG"

# email info
sender = "yun190828@gmail.com"
toAddrList = ["dbsgh3025@gmail.com"]
cc_users = ["dbsgh0325@gmail.com"]

location = "not"

class image_preprocessing:
    def __init__(self, cam_width_num, cam_height_num, com_w_start, com_h_start):
        self.cam_width_num = cam_width_num
        self.cam_height_num = cam_height_num
        
        self.com_w_start = com_w_start
        self.com_h_start = com_h_start
        
        
        size_img = Image.open(size_file)
        
        self.com_w_len, self.com_h_len = size_img.size
        
        size_img.close()
        
        self.original_path = original_path
        self.crop_path = crop_path
        self.resize_path = resize_path
        
    # remove files(crop image, resize image)    
    def removeAllFile(self):
        try:
            if os.path.exists(self.crop_path):
                for file in os.scandir(self.crop_path):
                    os.remove(file.path)
        except:
            print("remove exception")
    
    # image capture
    def imageCapture(self):
        import time
        now = time.localtime()
        name = "%s%s" % (self.original_path, "org_image")
        imgGrab = ImageGrab.grab(bbox=(self.com_w_start, self.com_h_start, self.com_w_len, self.com_h_len))
        saveas="{}{}".format(name,'.png')
        imgGrab.save(saveas)
        print("capture complete")
    
    
    # get image from directory
    def getImage(self, path):
        file_list = os.listdir(path)
        img_list = []
        
        for item in file_list :
            if item.find('.png') is not -1 :
                img_list.append(item)
        print("get images")
        return img_list
        
    # image crop
    def cropImage(self, img_list):
        for name in img_list :
            img = Image.open('%s%s'%(self.original_path,name,))
            i_width, i_height = img.size
            
            cam_num = 1
            h_start = 0
            for h_num in range(0, self.cam_height_num):
                w_start = 0
                for w_num in range(0, self.cam_width_num):
                    cutted_img = img.crop((w_start, h_start, w_start + i_width/self.cam_width_num, h_start + i_height/self.cam_height_num))
                    cutted_img.save('%s%s.png'%(self.crop_path, cam_num))
                    cam_num += 1
                    w_start += i_width/self.cam_width_num
                h_start += i_height/self.cam_height_num
                    
            img.close()
        print("crop complete")


    def imageResize(self, img_list):
        for name in img_list :
            img = Image.open('%s%s'%(self.crop_path, name))
            img_array = np.array(img)
            img_resize = cv2.resize(img_array, (120,120), interpolation = cv2.INTER_AREA)
            img = Image.fromarray(img_resize)
            img.save('%s%s.PNG'%(self.resize_path, name))
            img.close()
        
        print("resize complete")

class model:
    def __init__(self):
        pass

    def doModelLoad(self,model_file_name):
        print("======[load model]======")
        from tensorflow.keras.models import load_model
        model = load_model(model_file_name)
        
        self.model = model
        
        print("======[load model complete]======")
        
        #pred = model.predict_classes(x_test)
    
    def loadTestImage(self, img_path):
        data_gen = ImageDataGenerator(rescale=1./255)

        X = data_gen.flow_from_directory(
            img_path,
            target_size=(256, 256),
            batch_size=3,
            class_mode=None)
  
        print(X)
        print("load test image complete")
        return X
    
    def doModelPredict(self,X):
        model = self.model
        
        pred = model.predict_classes(X)
        return pred

        
        
class sendEmail:
    def __init__(self):
        pass
        self.msg = MIMEMultipart('alternative')
        self.msg = MIMEMultipart('alternative')  
        self.msg['Subject'] = location
        self.msg['From'] = sender
        self.msg['To'] = ",".join(toAddrList)
        self.msg['Cc'] = ",".join(cc_users)
        
    def setContents(self, img_list, cam_num_list): 
        msg = self.msg
        
        for img in img_list:
            part = MIMEBase('application','octet-stream')
            attach = crop_path+img    
            part.set_payload(open(attach,'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename=%s'%os.path.basename(attach))
            msg.attach(part)
        
        text = ''
        for num in range(0, len(cam_num_list)):
            text += str(cam_num_list[num]) + ', '
 
        part1 = MIMEText(text, _charset='utf-8')

        msg.attach(part1)
        
        self.msg = msg
    
    def sendImage(self):
        msg = self.msg
    
        ss = smtplib.SMTP('smtp.gmail.com', 587)
        ss.ehlo()
        ss.starttls() 
        ss.login('yun190828@gmail.com', 'stncdwcvyrxkzmqj')
        ss.sendmail(sender, toAddrList+cc_users, msg.as_string())
        ss.close()
