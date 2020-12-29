from tkinter import *
import math
import PIL.Image, PIL.ImageTk
import my_serial as ser
global resault

def rotate_pointer(degree):
    global my_line,my_line1

    if my_line != None:
        my_canvas.delete(my_line)
        my_canvas.delete(my_line1)
        my_line = None
        my_line1 = None
        

    x = 200 * math.cos(((2 * math.pi) / 360.0) * degree) + 244
    y = 255 - 200 * math.sin(((2 * math.pi) / 360.0) * degree)
    my_line = my_canvas.create_line(244, 255, x, y, fill='black', width=10)
    my_line1 = my_canvas.create_line(244, 255, x, y, fill='white', width=3)

#==========================================================================
resault=0

def f():

    msg = ser.get_message(ser1)
    if msg != None:
        msg1 = msg[1:-1]
        result = ser.parse_message(msg1)
        #print(resault)
        print(result[0])
        rotate_pointer(result[0]*300)

    root.after(30, f)

ser1 = ser.my_init_serial()

#==========================================================================
root = Tk()
root.title('Gauge')
root.geometry('480x350+0+0')
root.resizable(width=False,height=False)
my_canvas = Canvas(root, width=475, height=475, bg='white')
my_canvas.pack(pady=0)

my_line = my_canvas.create_line(250, 250, 250, 250, fill='red', width=10)
my_line1 = my_canvas.create_line(250, 250, 250, 250, fill='red', width=10)
img = PIL.Image.open('images/gauge.png')
image = PIL.ImageTk.PhotoImage(image=img)
my_image = my_canvas.create_image(2, 2, anchor=NW, image=image)


root.after(1000, f)


root.mainloop()
