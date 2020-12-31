from tkinter import *
import math
import PIL.Image, PIL.ImageTk
import my_serial as ser
global result
result=0


def rotate_pointer(degree):
    global my_line , my_line1

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


#==========================================================================
def needle():
    msg = ser.get_message(ser1)
    if msg != None:
        msg1 = msg[1:-1]
        result = ser.parse_message(msg1)
        avg_result = avg_filter(result[0])
        print(avg_result)
        rotate_pointer(avg_result*294.2)


    root.after(30, needle)

ser1 = ser.my_init_serial()


    

#==========================================================================
root = Tk()
root.title('Gauge')
root.geometry('480x350+900+600')
root.resizable(width=False,height=False)
my_canvas = Canvas(root, width=475, height=475, bg='white')
my_canvas.pack(pady=0)

photo = PhotoImage(file ="images/matmon.ico")
root.iconphoto(False, photo)

my_line = my_canvas.create_line(250, 250, 250, 250, fill='red', width=10)
my_line1 = my_canvas.create_line(250, 250, 250, 250, fill='red', width=10)
img = PIL.Image.open('images/gauge.png')
image = PIL.ImageTk.PhotoImage(image=img)
my_image = my_canvas.create_image(2, 2, anchor=NW, image=image)


root.after(1000, needle)


root.mainloop()
