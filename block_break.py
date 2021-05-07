#ゲーム本体
import tkinter as tk
import random
import sys

#基本設定
root = tk.Tk() #ルート
root.title("ブロック崩し") #タイトル
root.geometry("600x480+320+90") #画面のサイズとデスクトップ上の位置

#ウィンドウ関連
class Window():
    def __init__(self):
        self.width = 600 #ウインドウサイズ(x)
        self.height = 480 #ウインドウサイズ(y)
        self.center_x = self.width/2 #センター(x)
        self.center_y = self.height/2 #センター(y)
        self.tick = 20 #画面更新秒数(ms)

    def resizeEvent(self,event): #ウィンドウサイズの変更
        size_x = tk.Tk().winfo_width() #変更後のウィンドウサイズ(x)
        size_y = tk.Tk().winfo_height() #変更後のウィンドウサイズ(y)

win = Window() #ウィンドウのインスタンス生成
cv = tk.Canvas(root, width = win.width, height = win.height) #キャンバス生成
cv.pack()

#ボール設定
class Ball:

    def __init__(self):
        self.x = 250 #ボールの初期位置(中心のX座標)
        self.y = 250 #ボールの初期位置(中心のY座標)
        self.w = 10 #ボールの幅(大きさ)
        self.dx = 4 #フレームごとの移動量(x座標)
        self.dy = 4 #フレームごとの移動量(y座標)
        self.color = "red" #ボールの色
    
    def draw(self): #描画
        cv.create_oval(self.x-self.w, self.y-self.w, self.x+self.w, self.y+self.w, fill = self.color, tag = "ball")
        cv.pack()

    def move(self): #動作
        #移動
        self.x += self.dx
        self.y += self.dy
        #壁にぶつかるとき
        if self.x - self.w < 0 or self.x + self.w > win.width:
            self.dx *= -1
        if self.y - self.w < 0 or self.y + self.w > win.height:
            self.dy *= -1

        #パドルにぶつかるとき
        if self.y + self.w > paddle.y - paddle.wy and ball.x > paddle.x-paddle.wx and ball.x < paddle.x+paddle.wx:
            self.dy *= -1

    def delete(self):
        cv.delete("ball")
ball = Ball() #ボールのインスタンス生成

#パドル設定
class Paddle:
    
    def __init__(self):
        self.x = win.center_x #パドルの初期位置(y座標)
        self.y = win.height - 30 #パドルの初期位置(x座標)
        self.wx = 45 #パドルの幅(x座標)
        self.wy = 8 #パドルの幅(y座標)
        self.dx = 15 #パドルの移動量(y成分の変化なし)
        self.color = "blue" #パドルの色
    
    def draw(self): #描画
        cv.create_rectangle(self.x-self.wx,self.y-self.wy, self.x+self.wx,self.y+self.wy, fill=self.color, tag="paddle")

    def right(self,event): #右移動
        cv.delete("paddle")
        self.x += self.dx
        self.draw()
    def left(self,event): #左移動
        cv.delete("paddle")
        self.x -= self.dx
        self.draw()

    def move(self): #移動キーバインド
        root.bind("<Right>",self.right)
        root.bind("<Left>",self.left)
paddle = Paddle() #パドルのインスタンス生成

#ブロック設定
class Block:
    w_x =60 #ブロックの幅(x座標)
    w_y = 30 #ブロックの幅(y座標)
    #global dy, score

    #当たったかどうかの情報 1:まだ,0:当たった
    block_list =[[1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1]]
    def draw(self): #描画
        for j in range(5):
            color_r = random.randint(0,15)
            color_g = random.randint(0,15)
            color_b = random.randint(0,15)
            cord = '#' + hex(color_r)[2:] + hex(color_g)[2:] + hex(color_b)[2:]
            for i in range(10):
                    cv.create_rectangle(i*self.w_x, j*self.w_y, (i+1)*self.w_x, (j+1)*self.w_y, fill = cord, tag = "block"+str(j)+str(i))

    def reflect(self): #ボールの反射
        for i in range(10):
            for j in range(5):
                #ボールが上から反射
                if (ball.y-ball.w < (j+1)*self.w_y #ボールがブロックより下にある
                    and i*self.w_x < ball.x < (i+1)*self.w_x #ボールがブロックの左右に挟まれている
                    and self.block_list[j][i] == 1): #スイッチが1
                        ball.dy *= -1 #反射
                        cv.delete("block"+str(j)+str(i)) #ブロックを消す
                        self.block_list[j][i] = 0 #スイッチを切る
                        score.score += 1 #加点
                        score.delete() #旧スコア削除
                        score.draw() #新スコア生成
block = Block() #ブロックのインスタンス生成

#スコア
class Score():
    score = 0 #初期値
    def draw(self):
        cv.create_text(win.width - 50, 470, text = "Score : " +str(self.score), font = ('FixedSys', 16), tag = "score")
    def delete(self):
        cv.delete("score")
score = Score() #スコアのインスタンス生成

#ゲームオーバー
def gameover():
    #global w, dx, dy
    if ball.y + ball.w > win.height :
        cv.delete("paddle")
        cv.delete("ball")
        cv.create_text(win.center_x, win.center_y, text = 'GAME OVER', font = ('FixedSys', 90))
        ball.w = 0
        ball.dx = 0
        ball.dy = 0

#クリア
def gameclear():
    #global w, dx, dy
    if score.score == 30 :
        cv.delete("paddle")
        cv.delete("ball")
        cv.create_text(win.center_x, win.center_y, text = "GAME CLEAR", font = ('FixedSys', 90))
        ball.w = 0
        ball.dx = 0
        ball.dy = 0

def gameloop():
    #Window.resizeEvent() #ウィンドウサイズの変更に応じた処理
    ball.delete() #ボール消去
    ball.move() #ボールを動かす
    paddle.move() #パドルを動かす
    block.reflect() #ボールの反射とブロックの消去
    ball.draw() #ボール描画
    gameover() #ゲームオーバー表示
    gameclear() #クリア表示
    root.after(win.tick, gameloop) #最初に戻る
'''
#メイン処理
def driver():
    cv.create_text(win.center_x, win.center_y-40, text = 'ブロック崩し', font = (u'MS　ゴシック', 90))
    cv.create_text(win.center_x, win.center_y+110, text = 'Play (Press "P")', font = (u'MS　ゴシック', 30))
    cv.create_text(win.center_x, win.center_y+140, text = 'Setting (Press "S")', font = (u'MS　ゴシック', 30))

    def play(self,event): #ゲーム


    #def setting(self,event): #設定


    def keys(self): #キーバインド
        root.bind("<KeyPress>", self.play())
        root.bind("<Key-s>", self.setting())
'''
#driver() #スタート画面
#root.after(win.tick, driver) #最初に戻る

#実行部
block.draw() #ブロック初期描画
ball.draw() #ボール初期描画
paddle.draw() #パドル初期描画
score.draw() #スコア初期描画
gameloop() #ゲーム中
root.mainloop()