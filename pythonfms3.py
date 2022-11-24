import tkinter as tk
from tkinter import *
import tkinter.messagebox as box
import subprocess, sys


class FmsApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        # the container is where we'll put frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
        
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        Label1 = tk.Label(self,text = 'Username:', fg='black', font=("Helvetica", 16))
        Label1.place(x=60, y=50)

        txtfld1=tk.Entry(self, bd=5)
        txtfld1.place(x=60, y=100)

        Label2 = tk.Label(self,text = 'Password:', fg='black', font=("Helvetica", 16))
        Label2.place(x=60, y=150)

        txtfld2=Entry(self,show="*", bd=5)
        txtfld2.place(x=60, y=200)
        
        def my_show():
            if(v1.get()==1):
                txtfld2.config(show='')
            else:
                txtfld2.config(show='*')


        v1 = IntVar(value=0)
        C1 = Checkbutton(self, text = "Show Password", variable = v1,onvalue=1,offvalue=0,command=my_show)
        C1.place(x=60, y=250)
        def dialog1():
            username=txtfld1.get()
            password = txtfld2.get()
            if (username == 'admin' and  password == '123'):
                controller.show_frame("PageOne")
                box.showinfo('info','Correct Login')
                    
            else:
                box.showinfo('info','Invalid Login')

        btn = Button(self, text = 'Login',font=("Helvetica", 16),height= 1, width=10,command = dialog1)
        btn.place(x=60,y=300)


        

        

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label3 = tk.Label(self,text = 'Enter the file directory ', fg='black', font=("Helvetica", 16))
        Label3.place(x=60, y=50)

        txtfld3=tk.Entry(self, bd=5)
        txtfld3.place(x=60, y=100)

        def dialog2():
            directeory=txtfld3.get()
            
            if (directeory == ''):
                box.showinfo('info','Correct Login')
                    
            else:
                d= 'C:\\Users\\Bharath Reddy Musku\\Desktop\\CapstoneProject\\fms.ps1'

                p = subprocess.Popen(["powershell.exe","-File", d, directeory ], stdout=sys.stdout)

                p.communicate()


                box.showinfo('info','Invalid Login')




        btn2 = Button(self, text = 'Login',font=("Helvetica", 16),height= 1, width=10,command = dialog2)
        btn2.place(x=60,y=150)


if __name__ == "__main__":
    app = FmsApp()
    app.title('FILE MONITORING SYSTEM')
    app.geometry("500x400+20+30")
    app.mainloop()




    











