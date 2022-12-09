import tkinter
from tkinter import Tk, Toplevel
from tkinter import *
import tkinter.messagebox as box
import subprocess, sys
from subprocess import Popen, PIPE
import threading
from functools import partial
import mysql.connector



def main():
    main_window = Tk()
    app = first(main_window)
    main_window.mainloop()


class first:    # Login Page
    def __init__(self, root):
        self.root = root
        self.root.title('FILE MONITORING SYSTEM')   # Tittle
        self.root.geometry('500x400+20+30') # Dimensions
        Label1 = Label(self.root,text = 'Username:', fg='black', font=("Helvetica", 16))
        Label1.place(x=60, y=50)

        txtfld1=Entry(self.root, bd=5)
        txtfld1.place(x=60, y=100)

        Label2 = Label(self.root,text = 'Password:', fg='black', font=("Helvetica", 16))
        Label2.place(x=60, y=150)

        txtfld2=Entry(self.root,show="*", bd=5)
        txtfld2.place(x=60, y=200)
        # Checkbox to mask/show password
        def my_show():
            if(v1.get()==1):
                txtfld2.config(show='')
            else:
                txtfld2.config(show='*')

        v1 = IntVar(value=0)
        C1 = Checkbutton(self.root, text = "Show Password", variable = v1,onvalue=1,offvalue=0,command=my_show)
        C1.place(x=60, y=250)

        def login(): # cheking user Input with mysql database
            username=txtfld1.get()
            password = txtfld2.get()
            mydb = mysql.connector.connect(host="localhost",user="root",passwd="1234",database="fms")
            cursor = mydb.cursor()
    
            savequery = "SELECT * FROM fmslogin WHERE username=%s AND password=%s" 
            # Get the records with these username and password 
            cursor.execute(savequery,(username,password)) 
            myresult = cursor.fetchall() 
    
            if myresult: # If there is such a record, then success
                box.showinfo("Info",'Login Successful')
                self.root.destroy()
                main_window = Tk()
                app = second(main_window, self)
                main_window.mainloop()

            else: # Wrong password
                box.showerror("Info","Login Error")
            cursor.close()
            mydb.close()
        btn = Button(self.root, text = 'Login',font=("Helvetica", 16),height= 1, width=10,command = login)
        btn.place(x=60,y=300)

class second:   # Asks for user Input for path
    def __init__(self, root, first):
        self.root = root
        self.root.title('FILE MONITORING SYSTEM')
        self.root.geometry('500x400+20+30')


        Label3 = Label(self.root,text = 'Enter the file directory to start FMS', fg='black', font=("Helvetica", 16))
        Label3.place(x=60, y=50)
        
        self.mystring = tkinter.StringVar(self.root)

        txtfld3=Entry(self.root,textvariable=self.mystring, bd=5)
        txtfld3.place(x=60, y=100)
        # Verify Input
        def input():
            directeory=txtfld3.get()
            
            if (directeory == ''):
                box.showinfo('info','Input Empty')
                    
            else:
                self.root.destroy()
                main_window = Tk()
                app = third(main_window, self)
                main_window.mainloop()

        btn2 = Button(self.root, text = 'Submit',font=("Helvetica", 16),height= 1, width=10,command = input)
        btn2.place(x=60,y=150)

    def return_id(self):    # Passing value to Next class
        return self.mystring.get()
        
class third:    # Function of FMS
    def __init__(self, root, first):
        self.root = root
        self.root.title('FILE MONITORING SYSTEM')
        self.root.geometry('700x700')

        fms_box = Text(self.root, borderwidth=3, relief="sunken")
        fms_box.place(x=10,y=100)

        def runScript(fms_box=None):    # Calling subprocess
            d= './fms.ps1'
            id = first.return_id()
            # Passing userInput as arguments to powershell
            p= subprocess.Popen(["powershell.exe","-File", d, id ],shell=True,bufsize=1,stdout=subprocess.PIPE, text=True)
            while p.poll() is None:
                msg=p.stdout.readline().strip()
                if msg:
                    fms_box.insert(END,msg + "\n")
        def tredRun(log_box_1=None):
        # create a thread to run the script
            threading.Thread(target=runScript, args=[log_box_1]).start()
        
        btn3 = Button(self.root, text = 'Start',font=("Helvetica", 16),height= 1, width=10,command = partial(tredRun,fms_box))
        # Real time Output using Threads
        btn3.place(x=60,y=50)
        
        scrollbar = Scrollbar(self.root, orient=VERTICAL)
        scrollbar.grid()
        old_stdout = sys.stdout
        sys.stdout = Redirect(fms_box)

class Redirect():

    def __init__(self, widget, autoscroll=True):
        self.widget = widget
        self.autoscroll = autoscroll

    def write(self, text):
        self.widget.insert('end', text)
        if self.autoscroll:
            self.widget.see("end")  # autoscroll

    def flush(self):
        pass



if __name__ == '__main__':
    main()