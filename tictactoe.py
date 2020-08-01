#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_tictactoe import Ui_MainWindow

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.count = 1
        self.ksi = 0.1
        self.finished = 0
        self.game = {8:self.pushButton_10,0:self.pushButton_2,1:self.pushButton_3,2:self.pushButton_4,3:self.pushButton_5,4:self.pushButton_6,5:self.pushButton_7,6:self.pushButton_8,7:self.pushButton_9}
        self.resultSet = {"positive":200,"negative":-100}
        self.board = ["b" for i in range(9)]
        self.w = [0.5 for i in range(11)]
    
        for i in self.game:
            self.game[i].clicked.connect(self.buttonPressed)
    
        self.label_2.setText("Game %d" %(self.count)) 
        self.pushButton.clicked.connect(self.clear)
        self.sfile = open("tic-tac-toe.data","r")
        self.lines = self.sfile.readlines()
        for line in self.lines:
            line = line.replace(",","")
            self.result = self.resultSet[line[line.__len__()-9:line.__len__()-1]]
            line = line[:line.__len__()-9]
            self.generate(line)
            self.lms() 
            print ( "Board = %s Result = %.2f V(b) = %.2f  \n" %(line,self.result,self.vb))
            print ( "x1 = %.2f x2 = %.2f x3 = %.2f x4 = %.2f x5 = %.2f x6 = %.2f x7 = %.2f x8 = %.2f x9 = %.2f \n" %(self.x[1],self.x[2],self.x[3],self.x[4],self.x[5],self.x[6],self.x[7],self.x[8],self.x[9]))
            print ( "w1 = %.2f w2 = %.2f w3 = %.2f w4 = %.2f w5 = %.2f w6 = %.2f w7 = %.2f w8 = %.2f w9 = %.2f \n" %(self.w[1],self.w[2],self.w[3],self.w[4],self.w[5],self.w[6],self.w[7],self.w[8],self.w[9]))

    def generate(self,s):
        self.x = [0.0 for i in range(11)]
        directions = [s[:3],s[3:6],s[6:9],s[::3],s[1::3],s[2::3],s[::4],s[2:8:2]]
	cc = 0
        for d in directions:
            cx = d.count("x")
            co = d.count("o")
            cb = d.count("b")
            if ("xxb" in d  or "bxx" in d):
                self.x[1]+=1
            if ("oob" in d or "boo" in d):
                self.x[2]+=1
            if (cx == 1 and cb == 2):
                self.x[3]+=1
            if (co == 1 and cb == 2):
                self.x[4]+=1
            if (cx == 3):
                self.x[5]+=1
            if (co == 3):
                self.x[6]+=1
            if ("xbx" in d):
                self.x[7]+=1
            if ("obo" in d):
                self.x[8]+=1
            if (cc in (1,4,6,7) and cb == 1 and 'x' == d[1]):
                self.x[9]+=1
            if (cc in (1,4,6,7) and cb == 1 and 'o' == d[1]):
                self.x[10]+=1
	    cc+=1
        

    def Vb(self):
        self.vb = self.w[0] + self.w[1] * self.x[1] +  self.w[2] * self.x[2] + self.w[3] * self.x[3] + self.w[4] * self.x[4] + self.w[5] * self.x[5] + self.w[6] * self.x[6] + self.w[7] * self.x[7] + self.w[8] * self.x[8] + self.w[9] * self.x[9] + self.w[10] * self.x[10]
    
    def lms(self):
        self.Vb()
        self.w[1] = self.w[1] + self.ksi * (self.result - self.vb) * self.x[1]
        self.w[2] = self.w[2] + self.ksi * (self.result - self.vb) * self.x[2]
        self.w[3] = self.w[3] + self.ksi * (self.result - self.vb) * self.x[3]
        self.w[4] = self.w[4] + self.ksi * (self.result - self.vb) * self.x[4]
        self.w[5] = self.w[5] + self.ksi * (self.result - self.vb) * self.x[5]
        self.w[6] = self.w[6] + self.ksi * (self.result - self.vb) * self.x[6]
        self.w[7] = self.w[7] + self.ksi * (self.result - self.vb) * self.x[7]
        self.w[8] = self.w[8] + self.ksi * (self.result - self.vb) * self.x[8]
        self.w[9] = self.w[9] + self.ksi * (self.result - self.vb) * self.x[9]
        self.w[10] = self.w[10] + self.ksi * (self.result - self.vb) * self.x[10]

    def computer(self):
        max_vb = -200
        max_index = -1
        for i in range(18): 
            if (self.board[i%9] == "b"):
                would = [x for x in self.board] 
                self.result = -100
                if (i/9 < 1):
                    would[i%9] = "o"
                    self.generate("".join(would))
                    self.Vb()
                    self.vb*=-1
                else:
                    would[i%9] = "x"
                    self.generate("".join(would))
                    self.Vb()
                print ("Vb = %.2f max_vb = %.2f index = %d max_index = %d " %(self.vb,max_vb,i,max_index))
                print ( "x1 = %.2f x2 = %.2f x3 = %.2f x4 = %.2f x5 = %.2f x6 = %.2f x7 = %.2f x8 = %.2f \n" %(self.x[1],self.x[2],self.x[3],self.x[4],self.x[5],self.x[6],self.x[7],self.x[8]))
                if (self.vb > max_vb):
                    max_vb = self.vb
                    max_index = i % 9
        if (max_index != -1):
            self.board[max_index] = "x"
            self.game[max_index].setText("X")
            self.check()
            t = "".join(self.board)
            print ("%s\n%s\n%s" %(t[:3],t[3:6],t[6:9]))

    def check(self):
        self.generate("".join(self.board))
        t = "".join(self.board)
        if (self.x[5] > 0):
            self.finished = 1
            self.label.setText("Player X won")
            self.result = 200
            print("%d.Player X won" %(self.count))
            print ("%s\n%s\n%s" %(t[:3],t[3:6],t[6:9]))
        if (self.x[6] > 0):
            self.finished = 2
            self.label.setText("Player O won")
            self.result = -100
            print("%d.Player O won" %(self.count))
            print ("%s\n%s\n%s" %(t[:3],t[3:6],t[6:9]))


    def buttonPressed(self):
        button = self.sender()
        temp = [key for key,value in self.game.iteritems() if value.objectName() == button.objectName()][0]
        if (self.board[temp] == "b" and self.finished == 0):
            self.board[temp] = "o"
            button.setText("O")
            self.check() 
            if (self.finished == 0):
                self.computer()

    def clear(self):
        self.count+=1
        self.finished = 0
        self.label.setText("") 
        temp = [key for key,value in self.resultSet.iteritems() if value == self.result][0]
        endgame = ",".join(self.board)+","+temp+"\n"
        #if (endgame not in self.lines):
        #    self.sfile.write(endgame)        
        print("-----------------------------\n")
        self.label_2.setText("Game %d" %(self.count))
        self.board = ["b" for x in range(9)]
        for i in self.game:
            self.game[i].setText("")

app = QtGui.QApplication(sys.argv)
run = MainWindow()
run.show()
sys.exit(app.exec_())

