import tkinter
from PIL import Image, ImageTk

#ウィンドウ作成
root = tkinter.Tk() #ウィンドウのオブジェクト

#ここにウィンドウの設定・表示内容
root.title("test")
root.minsize(640,480)

canvas = tkinter.Canvas(bg="black", width=640, height=480) #canvasの背景色とサイズ指定
canvas.place(x=0,y=0) #canvasオブジェクトの座標指定
"""
img1 = Image.open(open("taiyou.jpg","rb"))
img1 = img1.thumbnail((640,480), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(img1)
"""
img1 = tkinter.PhotoImage(file = "taiyou.gif")
canvas.create_image(0, 0, image = img1)


#メインループ
root.mainloop() #ウィンドウ表示 必ず最後に書く