from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *

import fileinput

class my_application:
    def __init__(self, master):
        self.master = master
        master.title("Fast reading")
        master.resizable(0,0)
        self.text = False 
        self.stop = True
        self.indx = -1
        self.end = True
        
        self.show_text = StringVar()
        self.show_text.set("Select a file")
        self.show_progress = StringVar()
        self.show_progress.set("Progress 0 %")
        self.w_num = IntVar()
        self.w_num.set(1)
        
        self.lbl_frame = Frame(master, width = 40)
        self.lbl_speed = Label(master, text = "Current speed", font = "Arial 10")
        self.sca_speed = Scale(master, orient = HORIZONTAL, 
                               length = 400, from_ = 200, to = 1000, tickinterval = 100, resolution = 100)
        self.lbl = Label(master, width = 40, height = 5, bg = 'grey80', textvariable = self.show_text, font = "Arial 12")
        self.progress = Label(self.master, textvariable = self.show_progress, font = "Arial 10")
        
        self.bttn_frame = Frame(master)
        self.bttn_open = Button(master, text = "Open a file", command = self.button_open)
        self.bttn_start = Button(self.bttn_frame, text = "Start", command = self.button_start, fg = "green")
        self.bttn_next = Button(self.bttn_frame, text = "Next", command = self.button_next)
        self.bttn_previous = Button(self.bttn_frame, text = "Back", command = self.button_previous)
                        
        self.lbl.pack(fill = 'x')
        self.lbl_frame.pack(fill = 'x')
        self.lbl_speed.pack(in_ = self.lbl_frame, side = 'left')
        self.sca_speed.pack(in_ = self.lbl_frame, side = 'left')
        self.progress.pack(in_ = self.lbl_frame, side = 'right')
        
        self.select_frame = Frame(master)
        self.select_frame.pack(fill = 'x')
        Label(text = "Number of words", font = "Arial 10").pack(in_ = self.select_frame, side = 'left')
        Radiobutton(text = "1", variable = self.w_num, value = 1,
                    command = self.change_w_num).pack(in_ = self.select_frame, side = 'left')
        Radiobutton(text = "2", variable = self.w_num, value = 2,
                    command = self.change_w_num).pack(in_ = self.select_frame, side = 'left')
               
        self.bttn_frame.pack()
        self.bttn_previous.pack(in_ = self.bttn_frame, side = 'left')
        self.bttn_start.pack(in_ = self.bttn_frame, side = 'left')
        self.bttn_next.pack(in_ = self.bttn_frame, side = 'left')
        self.bttn_open.pack()
                        
        master.bind('<Key>', self.keypress)
        
    def button_open(self):
        file_name = askopenfilename(filetypes=[("Text files","*.txt")])
        if file_name:
            self.create_text(file_name)
            self.show_text.set("GO!")
            self.indx = 0
            self.change_w_num()
            self.end = False
                                   
    def create_text(self, file_name):
        f = open(file_name)
        self.text1 = f.read().replace('\n',' ').replace('— ','—').replace('– ','–').split(' ')
        self.text1 = list(filter(('').__ne__, self.text1))
        self.text2 = []
        for i in range(0,len(self.text1)-1,2):
            self.text2.append(self.text1[i] + " " + self.text1[i+1])
        if len(self.text1) % 2:
            self.text2.append(self.text1[-1])
        self.text1.append("The end!")
        self.text2.append("The end!")
   
    def change_w_num(self):
        if self.indx > -1:
            if self.w_num.get() == 1:
                self.text = self.text1
                self.indx = self.indx * 2 
            if self.w_num.get() == 2:
                self.text = self.text2
                self.indx = (self.indx-1) // 2
    
    def button_start(self):
        if self.stop:
            if self.indx == -1:
                self.show_text.set("First select a file!") 
            else: 
                if self.end:
                    self.indx = 0
                    self.end = False
                self.bttn_start["text"] = "Pause"
                self.bttn_start["fg"] = "red"
                self.stop = False
                self.update_text()
        else:
            self.bttn_start["text"] = "Start"
            self.bttn_start["fg"] = "green"
            self.indx -= 1
            self.stop = True
        
    def button_next(self):
        if self.stop and -1 < self.indx < len(self.text)-1 :
            self.indx += 1
            self.show_text.set(self.text[self.indx])  
            self.show_progress.set("Progress %s" %(self.indx * 100 // len(self.text)) + "%")
            if self.indx == len(self.text)-1:
                self.show_progress.set("Progress 100%")
                
    def button_previous(self):
        if self.stop and self.indx > 0:
            self.indx -= 1
            self.show_text.set(self.text[self.indx])
            self.show_progress.set("Progress %s" %(self.indx * 100 // len(self.text)) + "%")
    
    def update_text(self):
        if self.indx == len(self.text):
            self.stop = True
            self.end = True
            self.indx -= 1
            self.bttn_start["text"] = "Start again"
            self.bttn_start["fg"] = "orange"
        if not (self.stop or self.end):
            self.show_text.set(self.text[self.indx])
            self.indx += 1
            self.show_progress.set("Progress %s" %(self.indx * 100 // len(self.text)) + "%")
            self.master.after(60000//self.sca_speed.get(), self.update_text)
        
            
    def keypress(self, event):
        if event.keycode == 32:
            self.button_start()
        if event.keycode == 38:
            self.sca_speed.set(self.sca_speed.get() + 100)
        if event.keycode == 40: 
            self.sca_speed.set(self.sca_speed.get() - 100)
        if event.keycode == 37: 
            self.button_previous()
        if event.keycode == 39: 
            self.button_next()
                                    
if __name__ == "__main__":
    root = Tk()
    my_gui = my_application(root)
    root.mainloop()
