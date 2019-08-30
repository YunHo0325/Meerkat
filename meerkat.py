from tkinter import *
from tkinter import ttk
import tkinter as tk
import first
from pynput.mouse import Controller
from pynput.mouse import Listener, Button


com_w_start = ""
com_h_start = ""
cam_width_num = ""
cam_height_num = ""

class Meerkat:
    def __init__(self):
        pass

    def showWindow(self):
        def pointClick():
            lis = clickListen()
            lis.startListener()
        
        def startButton():       
            print(type(com_w_start))
            i = first.image_preprocessing(int(cam_width_num.get()), int(cam_height_num.get()), int(com_w_start.get()), int(com_h_start.get()))

            # load_model
            md = first.model()
            md.doModelLoad(first.model_path)

            # email
            send_email = first.sendEmail()


            while 1:
                i = first.image_preprocessing(int(cam_width_num.get()), int(cam_height_num.get()), int(com_w_start.get()), int(com_h_start.get()))
                send_email = first.sendEmail()
                
                # getting image 
                i.removeAllFile()
                i.imageCapture()
                org_img_list = i.getImage(first.original_path)
                i.cropImage(org_img_list)
                
                # load test images
                X = md.loadTestImage(first.test_path)

                # predict
                pred = md.doModelPredict(X)
                print(pred)
                crop_img_list = i.getImage(first.crop_path)
                idx=0

                fire_img_list = []
                cam_num_list = []
                flag = 0
                
                for i in pred:
                    if i == 0:
                        fire_img_list.append(crop_img_list[idx])
                        cam_num_list.append(idx+1)
                        flag = 1
                    idx += 1   
                    
                # send image
                if flag == 1:
                    send_email.setContents(fire_img_list, cam_num_list)
                    send_email.sendImage()
                    flag = 0

        
        def endButton():
            exit(0)
            
        window = tk.Tk()
        text = tk.Text(window)

        window.title("Meerkat")
        window.resizable(False, False)
        window.geometry("640x360")
        
        label_Font=('Nanumgothic', 16, 'bold')
        button_Font=('Nanumgothic', 12, 'bold')
        any_Font=('Nanumgothic', 15, 'bold')
        
        camera_Label = tk.Label(window, text="< 카메라 >")
        camera_Label.config(font=label_Font)
        camera_Label.place(x=50, y=50)
        
        self.cam_width_num = StringVar()
        self.cam_height_num = StringVar()
        
        cam_width_num = self.cam_width_num
        cam_height_num = self.cam_height_num
        
        row_Label = tk.Label(window, text="가로 : ")
        row_Label.config(font=any_Font)
        row_Label.place(x=160, y=50)
        row_txt = tk.Entry(window, textvariable=cam_width_num)
        row_txt.place(x=225, y=50)
        
        col_Label = tk.Label(window, text="   세로 :", font=("Gothic, 15"))
        col_Label.config(font=any_Font)
        col_Label.place(x=360, y=50)
        row_txt = tk.Entry(window, textvariable=cam_height_num)
        row_txt.place(x=445, y=50)
        
        self.com_w_start = StringVar()
        self.com_h_start = StringVar()
        
        com_w_start = self.com_w_start
        com_h_start = self.com_h_start
        
        
        start_Label = tk.Label(window, text="< 시작점 > ", font=("Helvetica, 15"))
        start_Label.config(font=label_Font)
        start_Label.place(x=50, y=100)
        x_Label = tk.Label(window, text="x : ")
        x_Label.config(font=any_Font)
        x_Label.place(x=160, y=100)
        x_txt = tk.Entry(window, textvariable=com_w_start)
        x_txt.place(x=225, y=100)
        
        y_Label = tk.Label(window, text="   y :", font=("Gothic, 15"))
        y_Label.config(font=any_Font)
        y_Label.place(x=360, y=100)
        y_txt = tk.Entry(window, textvariable=com_h_start)
        y_txt.place(x=445, y=100)
        
        '''
        select_Button = tk.Button(window, text="   선택   ", command = pointClick)
        select_Button.config(font=button_Font)
        select_Button.place(x=200, y=100)
        '''
        
        
        start_Button = tk.Button(window, text ="   시작   ", command = startButton)
        start_Button.place(x=200, y=200)
        start_Button.config(font=button_Font)
        stop_Button = tk.Button(window, text ="   중지   ", command = endButton)
        stop_Button.place(x=400, y=200)
        stop_Button.config(font=button_Font)

        window.mainloop()

        
            

class clickListen:
    def __init__(self):
        pass
        
    def startListener(self):            
        def on_move(x, y):
            return


        def on_click(x, y, button, pressed):
            if pressed:
                com_w_start = x
                com_h_start = y


        def on_scroll(x, y, dx, dy):
            return
            
        with Listener(
            on_click=on_click) as listener:
            listener.join()
        
        
        
if __name__ == '__main__':
    shWin = Meerkat()
    shWin.showWindow()
    
    
    
    
