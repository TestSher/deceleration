#3.3{18/1/2021}
#==============================================================================================
from tkinter import*
from tkinter import messagebox
import tkinter.font as tkFont
import math
import PIL.Image, PIL.ImageTk
import time
import my_serial as ser
import tkinter as tk
root = Tk()
global resault
global avg_samples
from gpiozero import CPUTemperature
result=0
version="version: 3.3 (last update 18/1/2021)"

sysdim = PhotoImage(file = 'images/_System data.png')
setim = PhotoImage(file = 'images/_   Settings.png')
conim = PhotoImage(file = 'images/small_confirm.png')
startim = PhotoImage(file = 'images/_    Initiate.png')

#==============================================================================================
def init():
    init = Toplevel()
    init.geometry('800x480+0+0')
    init.resizable(width=False,height=False)
    my_canvas = Canvas(init, width=735, height=735, bg='white')
    my_canvas.pack(pady=0)

    photo = PhotoImage(file ="images/matmon.ico")
    init.iconphoto(False, photo)

    img = PIL.Image.open('images/big_gauge.png')
    image = PIL.ImageTk.PhotoImage(image=img)
    my_image = my_canvas.create_image(2, 2, anchor=NW, image=image)

    global my_line , my_line1
    my_line = my_canvas.create_line(250, 250, 250, 250, fill='red', width=10)
    my_line1 = my_canvas.create_line(250, 250, 250, 250, fill='red', width=10)
    #time.sleep(0.01)

    def rotate_pointer(degree):
        global my_line , my_line1
        if my_line != None:
            my_canvas.delete(my_line)
            my_canvas.delete(my_line1)

            my_line = None
            my_line1 = None



        x = 260 * math.cos(((2 * math.pi) / 360.0) * degree) + 367
        y = 356 - 260 * math.sin(((2 * math.pi) / 360.0) * degree)
        my_line = my_canvas.create_line(367, 356, x, y, fill='black', width=10)
        my_line1 = my_canvas.create_line(367, 356, x, y, fill='white', width=3)

    global avg_samples, index
    avg_buff = [0] * 10
    index = 0
    avg_samples = 0

    def avg_filter(sample):
        global avg_samples, index

        weight_sample = sample / 10
        avg_samples = avg_samples - avg_buff[index] + weight_sample
        avg_buff[index] = weight_sample

        index += 1
        if index >= 10:
            index = 0

        return avg_samples
    def needle():
        msg = ser.get_message(ser1)
        if msg != None:
            msg1 = msg[1:-1]
            result = ser.parse_message(msg1)
            avg_result = avg_filter(result[0])
            print(avg_result)
            rotate_pointer(avg_result*294.2)

        root.after(30, needle)

    root.after(1000, needle)


    ser1 = ser.my_init_serial()

#==============================================================================================

def sysdata():
    sysdata = Toplevel()
    photo = PhotoImage(file = "images/matmon.ico")
    sysdata.iconphoto(False, photo)
    sysdata.geometry('400x270+200+125')
    sysdata.resizable(width=False,height=False)
    sysdata.attributes('-alpha',1)
    sysdata.title('System Data')
    Label(sysdata,text='System Data',font='calibri 22', fg='black').place(x=140, y=0)
    Label(sysdata,text='Raspberry pi Temp:',font='calibri 17', fg='black').place(x=10, y=40)
    Label(sysdata,text=version,font='calibri 11', fg='black').place(x=10, y=230)

    def temp():
        cpu = CPUTemperature()
        Label(sysdata,text= cpu.temperature,font='calibri 17', fg='green').place(x=210, y=42)

        root.after(1000,temp)

    root.after(20,temp)

#==============================================================================================

def opensettings():

    settings = Toplevel()
    photo = PhotoImage(file ="images/matmon.ico")
    settings.iconphoto(False, photo)
    settings.geometry('600x400+0+0')
    settings.resizable(width=False,height=False)
    settings.attributes('-alpha',1)
    settings.title('Settings')
    P = Canvas(settings, bg="blue", height=210, width=0)
    img = PhotoImage(file = 'images/resized_window.png')
    background_label = Label(settings, image=img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    P.pack()
    def Confirm():
     label4["text"]=entry2.get()
     label6["text"]=entry3.get()
     #label15["text"]=entry6.get()
     with open("DataExp.txt", "w") as text_file:
       text_file.write("vehicle category :" + entry2.get()+ '\n')
       text_file.write("Date :" + entry3.get()+ '\n')
       #text_file.write("delta between measurments:" + entry6.get()+ '\n')

    Label(settings,text='Settings',font='calibri 22', fg='black').place(x=240, y=0)
    #Label(settings,text='Units( g | m/s^2 ) :',font='calibri 17', fg='black').place(x=20, y=40)
    #Label(settings,text=' Δ between measurments (ms):',font='calibri 17', fg='black').place(x=14, y=75)
    #button6=Button(settings,text='  g  ',command=start,relief="groove")
    #button6.place(x=260, y=46)
    #button9=Button(settings,text=' m/s^2 ',command=start,relief="groove")
    #button9.place(x=300, y=46)
    #button10=Button(settings,text='✓',command=start,relief="groove")
    #button10.place(x=490, y=78)

    label5=Label(settings,text='vehicle category:',font='calibri 17', fg='black')
    label5.place(x=20, y=120)
    entry2=Entry(settings,font='calibri 16', fg='blue')
    entry2.place(x=260, y=120)
    label4=Label(settings,text="")
    label7=Label(settings,text='Date:',font='calibri 17', fg='black')
    label7.place(x=20, y=165)
    entry3=Entry(settings,font='calibri 16', fg='blue')
    entry3.place(x=260, y=165)
    label6=Label(settings,text="")
    entry6=Entry(settings,font='calibri 16', fg='black')
    #entry6.place(x=260, y=76)
    #label15=Label(settings,text="")

    button3=Button(settings,text='Confirm!',command=Confirm,image = conim)
    button3.place(x=20, y=300)


#==============================================================================================


photo = PhotoImage(file ="images/matmon.ico")
root.iconphoto(False, photo)
root.geometry('800x480+0+0')
C = Canvas(root, bg="blue", height=210, width=0)
img = PhotoImage(file = 'images/matmon.png')
background_label = Label(root, image=img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

C.place()

#==============================================================================================

"""label5=Label(root,text='vehicle category:',font='calibri 22', fg='black')
label5.place(x=170, y=165)
entry2=Entry(root,font='calibri 22', fg='blue')
entry2.place(x=380, y=166)
label4=Label(root,text="")
label7=Label(root,text='Date:',font='calibri 22', fg='black')
label7.place(x=305, y=222)
entry3=Entry(root,font='calibri 22', fg='blue')
entry3.place(x=380, y=223)
label6=Label(root,text="")"""

#==============================================================================================

button5=Button(root,text='System Data',command=sysdata,image = sysdim)
button5.place(x=57, y=60)
button2=Button(root,text='Settings',command=opensettings,image = setim)
button2.place(x=57, y=145)
button1=Button(root,text='start',command=init,image = startim)
button1.place(x=57, y=230)



#==============================================================================================

root.title('Brake Fade Tool')
#root.overrideredirect(1)
root.resizable(width=False,height=False)
root.attributes('-alpha',1)


#==============================================================================================

#root.after(1000, start)
root.mainloop()