# -*- coding: utf-8 -*-
from tkinter import *
from PIL import Image, ImageTk
import socket
from threading import Thread
import threading
import time
import os

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
sk.bind((socket.gethostname(), 1234))
sk.listen(5)

msg1 = ""
msg2 = ""
Run = True

def GameQuit(WinControl):
    global Run
    Run = False
    WinControl.quit()


def RunGameLevel(WinControl, level=0, solo=0):
    os.system("ConRan.py --level "+str(level)+" --solo "+str(solo))
    global msg1
    lb = Label(WinControl, text="Điểm\n"+msg1, fg="#006400")
    lb.config(font=("Courier", 25))
    lb.grid(row=0, column=2)


def GetHost(WinControl):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname_ex(hostname)[-1]
    strip = ""
    for i in ip_address:
        strip += i
        strip += "\t\n"
    Label(WinControl, text=u"Host: "+str(hostname)+u"\nIP all Interphace\n"+strip, fg="#FF0000").grid(row=0, column=0)

def Server():
    global msg1, Run, sk
    while Run:
        clientsocket, address = sk.accept()
        print(f"connect from {address} has been finished!")
        data = clientsocket.recv(1024).decode("utf-8")
        print(f"data: {data}")
        msg1 = data
        clientsocket.send(bytes("welcome to server", "utf-8"))
        clientsocket.close()
    

def WindowContol():
    WinControl = Tk()
    WinControl.title(u"Con Rắn Game Contol")

    myimg = ImageTk.PhotoImage(Image.open('snake.png'))
    Label(WinControl, image=myimg).grid(row=0, column=1)
    Label(WinControl, text=u"RẮN SĂN MỒI", fg="#006400").grid(row=1, column=1)
    Label(WinControl, text=u"\t", fg="#006400").grid(row=2, column=0)

    Button(WinControl, text=u"Lấy lại IP", padx=25, pady=10, command=lambda: GetHost(WinControl), fg="white", bg="#008000",).grid(row=1, column=0)
    Button(WinControl, text=u"Thoát game", padx=25, pady=10, command=lambda: GameQuit(WinControl), fg="white", bg="#008000",).grid(row=1, column=2)
    Button(WinControl, text=u"Cấp độ 0", padx=50, pady=20, command=lambda: RunGameLevel(WinControl, 0, 0), fg="white", bg="#DC143C").grid(row=3, column=0)
    Button(WinControl, text=u"Cấp độ 1", padx=50, pady=20, command=lambda: RunGameLevel(WinControl, 1, 0), fg="white", bg="#8A2BE2").grid(row=3, column=1)
    Button(WinControl, text=u"Cấp độ 2", padx=50, pady=20, command=lambda: RunGameLevel(WinControl, 2, 0), fg="white", bg="#0000FF").grid(row=3, column=2)
    Button(WinControl, text=u"Cấp độ 3", padx=50, pady=20, command=lambda: RunGameLevel(WinControl, 3, 0), fg="white", bg="#8B0000").grid(row=4, column=0)
    Button(WinControl, text=u"Cấp độ 4", padx=50, pady=20, command=lambda: RunGameLevel(WinControl, 4, 0), fg="white", bg="#8B008B").grid(row=4, column=1)
    Button(WinControl, text=u"Cấp độ 5", padx=50, pady=20, command=lambda: RunGameLevel(WinControl, 5, 0), fg="white", bg="#009900").grid(row=4, column=2)
    
    Label(WinControl, text=u"IP LAN\nhoặc WIFI", fg="#006400").grid(row=5, column=0)
    ip_addr_input = Entry(WinControl, width = 26)
    ip_addr_input.grid(row=5, column=1)
    ip_addr_input.insert(0, u"Nhập IP người SOLO")
    Button(WinControl, text=u"SOLO", padx=50, pady=20, command=lambda: RunGameLevel(WinControl, 0, 1), fg="white", bg="#FF4500").grid(row=5, column=2)

    WinControl.mainloop()

if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=Server, args=())
        t2 = threading.Thread(target=WindowContol, args=())
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        if Run == False:
            sk.shutdown(socket.SHUT_RDWR)
            sk.close()
            print("close")
            quit()
        
    except:
        print ("error")

