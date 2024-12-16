import pygame
import pyautogui, cv2
import tkinter as tk
import webbrowser
from time import sleep, time
import keyboard
from IPython.display import clear_output    
from subprocess import call
from tkinter import PhotoImage
import os
import customtkinter as ctk
from PIL import Image , ImageTk 


image_main = '陳禹豪.png'
image_pvp = 'test1.png'
image_pve = 'test2.png'
image_training = 'test3.png'
image_pvp_main = '陳禹豪2.png'
image_defaultmode = 'test1.png'
image_extra1 = 'forextra1.png'
fontsize = 70

buttonwidth = 1000
buttonheight = 150
buttonstartx = 450
buttonstarty = 200

created = True 
bounds1 = (buttonstartx, buttonstarty + 0 * (buttonheight + 50), buttonstartx + buttonwidth, buttonstarty + buttonheight + 0 * (buttonheight + 50))  # Adjust these values as needed
bounds2 = (buttonstartx, buttonstarty + 1 * (buttonheight + 50), buttonstartx + buttonwidth, buttonstarty + buttonheight + 1 * (buttonheight + 50))
bounds3 = (buttonstartx, buttonstarty + 2 * (buttonheight + 50), buttonstartx + buttonwidth, buttonstarty + buttonheight + 2 * (buttonheight + 50))
bounds4 = (buttonstartx, buttonstarty + 3 * (buttonheight + 50), buttonstartx + buttonwidth, buttonstarty + buttonheight + 3 * (buttonheight + 50))

def sizeset(image):
    bound = (0 , 0 , 1900 , 1200)
    output_image = image.crop(bound)
    return output_image

def colorset(image):
    img = Image.open(image)
    img = img.convert('RGB')
    pixels = img.load()

    for x in range(buttonwidth):
        for y in range(buttonheight):
            r , g , b = pixels[x , y]
            pixels[x , y] = (r + 50 , g , b + 50)
    
    img.save(image)

def quitwhole():
    window.destroy()

def versus():
    global pvp , pve , training
    pvp.destroy()
    pve.destroy()
    training.destroy()
    pvpbackground()

def defaultmodeplay():
    window.destroy()
    call(['python' , 'play.py'])

def extramode1():
    window.destroy()
    call(['python' , 'play2.py'])

def quitnow():
    global defaultmode , extra1 , quit
    defaultmode.destroy()
    extra1.destroy()
    quit.destroy()
    mainbackground()

def singleplayer():
    pass

def ai_training():
    window.destroy()
    call(['python' , 'train2.py'])

def on_enter_pvp(event):
    pvp.config(state= 'normal' , fg = 'blue' , activeforeground="blue" , bg='lightgreen')
    backgroundset_main(image_pvp)

def on_leave_pvp(event):
    pvp.config(fg='red')
    backgroundset_main(image_main)

def on_enter_pve(event):
    pve.config(state= 'normal' , fg = 'blue' , activeforeground="blue" , bg='lightgreen')
    backgroundset_main(image_pve)

def on_leave_pve(event):
    pve.config(fg='red')
    backgroundset_main(image_main)

def on_enter_training(event):
    training.config(state= 'normal' , fg = 'blue' , activeforeground="blue" , bg='lightgreen')
    backgroundset_main(image_training)

def on_leave_training(event):
    training.config(fg='red')
    backgroundset_main(image_main)

def on_enter_defaultmode(event):
    defaultmode.config(state= 'normal' , fg = 'blue' , activeforeground="blue" , bg='lightgreen')
    backgroundset_pvp(image_defaultmode)

def on_leave_defaultmode(event):
    defaultmode.config(fg='red')
    backgroundset_pvp(image_pvp_main)

def on_enter_extra1(event):
    extra1.config(state= 'normal' , fg = 'blue' , activeforeground="blue" , bg='lightgreen')
    backgroundset_pvp(image_extra1)

def on_leave_extra1(event):
    extra1.config(fg='red')
    backgroundset_pvp(image_pvp_main)

def pvpbackground():

    global defaultmode , extra1 , quit , bg_label, window , defaultmode_photo , extra1_photo , quit_photo
    img = Image.open(image_pvp_main)

    defaultmode_img = img.crop(bounds1)
    extra1_img = img.crop(bounds2)
    quit_img = img.crop(bounds3)

    defaultmode_img.save('defaultmode.png')
    extra1_img.save('extra1.png')
    quit_img.save('quit.png')

    colorset('defaultmode.png')
    colorset('extra1.png')
    colorset('quit.png')

    window.bg_photo = tk.PhotoImage(file=image_pvp_main) 
    bg_label = tk.Label(window, image=window.bg_photo)
    bg_label.image = window.bg_photo
    bg_label.place(x = 0 , y = 0, relwidth=1, relheight=1) 

    defaultmode_photo = tk.PhotoImage(file='defaultmode.png')
    extra1_photo = tk.PhotoImage(file='extra1.png')
    quit_photo = tk.PhotoImage(file='quit.png')


    defaultmode = tk.Button(window , text='default' , font=('Helvetica' , fontsize) ,image=defaultmode_photo , command=defaultmodeplay , compound= 'center' , relief= 'flat',bd=0 , highlightthickness=0 )
    extra1 = tk.Button(window , text='extra1' , image= extra1_photo ,font=('Helvetica' , fontsize) , command=extramode1  ,  compound= 'center' , relief= 'flat' , bd=0 , highlightthickness=0 )
    quit = tk.Button(window , text='quit' , font=('Helvetica' , fontsize) ,image= quit_photo , command=quitnow ,  compound= 'center' , relief='flat' , bd=0 ,highlightthickness=0 )

    
    defaultmode.place(x = buttonstartx , y = buttonstarty + 0 * (buttonheight + 50) , width=buttonwidth , height=buttonheight)
    extra1.place(x = buttonstartx , y = buttonstarty + 1 * (buttonheight + 50), width=buttonwidth , height=buttonheight)
    quit.place(x = buttonstartx , y = buttonstarty + 2 * (buttonheight + 50), width=buttonwidth , height=buttonheight)
    defaultmode.bind('<Enter>' , on_enter_defaultmode)
    defaultmode.bind('<Leave>' ,on_leave_defaultmode)
    extra1.bind('<Enter>' , on_enter_extra1)
    extra1.bind('<Leave>' , on_leave_extra1)

def mainbackground():

    global bg_label , pvp , pve , training , window , pvp_photo , pve_photo  , training_photo , quitall , quitall_photo

    img = Image.open(image_main)
    
    window.bg_photo = tk.PhotoImage(file=image_main) 
    bg_label = tk.Label(window, image=window.bg_photo)
    bg_label.image = window.bg_photo
    bg_label.place(x = 0 , y = 0, relwidth=1, relheight=1)

        # Crop the image
    pvp_img = img.crop(bounds1)
    pve_img = img.crop(bounds2)
    training_img = img.crop(bounds3)
    quitall_img = img.crop(bounds4)

    pvp_img.save('pvp.png')
    pve_img.save('pve.png')
    training_img.save('training.png')
    quitall_img.save('quitall.png')

    colorset('pvp.png')
    colorset('pve.png')
    colorset('training.png')
    colorset('quitall.png')
    
    pvp_photo = tk.PhotoImage(file='pvp.png')
    pve_photo = tk.PhotoImage(file='pve.png')
    training_photo = tk.PhotoImage(file='training.png')
    quitall_photo = tk.PhotoImage(file='quitall.png')

    training = tk.Button(window , text='hockai vs hockai' , font=('Helvetica' , fontsize) ,image=training_photo , command=ai_training , compound= 'center' , relief= 'flat',bd=0 , highlightthickness=0 )
    pvp = tk.Button(window , text='player vs player' , image= pvp_photo ,font=('Helvetica' , fontsize) , command=versus  ,  compound= 'center' , relief= 'flat' , bd=0 , highlightthickness=0 )
    pve = tk.Button(window , text='player vs hockai' , font=('Helvetica' , fontsize) ,image= pve_photo , command=singleplayer ,  compound= 'center' , relief='flat' , bd=0 ,highlightthickness=0 )
    quitall = tk.Button(window , text='i want to leave' , font=('Helvetica' , fontsize) ,image= quitall_photo , command=quitwhole ,  compound= 'center' , relief='flat' , bd=0 ,highlightthickness=0 )

    pvp.place(x = buttonstartx , y = buttonstarty + 0 * (buttonheight + 50) , width=buttonwidth , height=buttonheight)
    pve.place(x = buttonstartx , y = buttonstarty + 1 * (buttonheight + 50), width=buttonwidth , height=buttonheight)
    training.place(x = buttonstartx , y = buttonstarty + 2 * (buttonheight + 50), width=buttonwidth , height=buttonheight)
    quitall.place(x = buttonstartx , y = buttonstarty + 3 * (buttonheight + 50) , width= buttonwidth , height=buttonheight)
    pvp.bind('<Enter>' ,on_enter_pvp)
    pvp.bind('<Leave>' ,on_leave_pvp)
    pve.bind('<Enter>' , on_enter_pve)
    pve.bind('<Leave>' , on_leave_pve)
    training.bind('<Enter>' , on_enter_training)
    training.bind('<Leave>' , on_leave_training)

def backgroundset_main(image):
    global pvp , training , pve ,pvp_photo , pve_photo , training_photo , bg_label , quitall , quitall_photo
    
    img = Image.open(image)

            # Crop the image
    pvp_img = img.crop(bounds1)
    pve_img = img.crop(bounds2)
    training_img = img.crop(bounds3)
    quitall_img = img.crop(bounds4)

    pvp_img.save('pvp.png')
    pve_img.save('pve.png')
    training_img.save('training.png')
    quitall_img.save('quitall.png')

    colorset('pvp.png')
    colorset('pve.png')
    colorset('training.png')
    colorset('quitall.png')

    new_bg = tk.PhotoImage(file=image) 
    bg_label.config(image=new_bg)
    bg_label.image = new_bg

    pvp_photo = tk.PhotoImage(file='pvp.png')
    pve_photo = tk.PhotoImage(file='pve.png')
    training_photo = tk.PhotoImage(file='training.png')
    quitall_photo = tk.PhotoImage(file='quitall.png')

    pvp.config(image=pvp_photo , compound='center')
    pve.config(image=pve_photo , compound='center')
    training.config(image=training_photo , compound='center')
    quitall.config(image=quitall_photo , compound='center')


def backgroundset_pvp(image):
    global defaultmode , extra1 , quit , defaultmode_photo , extra1_photo , quit_photo , bg_label
    
    img = Image.open(image)


            # Crop the image
    defaultmode_img = img.crop(bounds1)
    extra1_img = img.crop(bounds2)
    quit_img = img.crop(bounds3)

    defaultmode_img.save('defaultmode.png')
    extra1_img.save('extra1.png')
    quit_img.save('quit.png')

    colorset('defaultmode.png')
    colorset('extra1.png')
    colorset('quit.png')

# Define bounds (left, upper, right, lower) in pixels
    new_bg = tk.PhotoImage(file=image) 
    bg_label.config(image=new_bg)
    bg_label.image = new_bg
    
    defaultmode_photo = tk.PhotoImage(file='defaultmode.png')
    extra1_photo = tk.PhotoImage(file='extra1.png')
    quit_photo = tk.PhotoImage(file='quit.png')


    defaultmode.config(image=defaultmode_photo , compound='center')
    extra1.config(image=extra1_photo , compound='center')
    quit.config(image=quit_photo , compound='center')
    

    


window = tk.Tk()

window.title('guitest')
width = 1900
height = 1200
window.geometry(f'{width}x{height}')




img = Image.open(image_main)
    
window.bg_photo = tk.PhotoImage(file=image_main) 
bg_label = tk.Label(window, image=window.bg_photo)
bg_label.image = window.bg_photo
bg_label.place(x = 0 , y = 0, relwidth=1, relheight=1)




        # Crop the image
pvp_img = img.crop(bounds1)
pve_img = img.crop(bounds2)
training_img = img.crop(bounds3)
quitall_img = img.crop(bounds4)

pvp_img.save('pvp.png')
pve_img.save('pve.png')
training_img.save('training.png')
quitall_img.save('quitall.png')

colorset('pvp.png')
colorset('pve.png')
colorset('training.png')
colorset('quitall.png')

pvp_photo = tk.PhotoImage(file='pvp.png')
pve_photo = tk.PhotoImage(file='pve.png')
training_photo = tk.PhotoImage(file='training.png')
quitall_photo = tk.PhotoImage(file='quitall.png')

training = tk.Button(window , text='hockai vs hockai' , font=('Helvetica' , fontsize) , fg= 'blue',image=training_photo , command=ai_training , compound= 'center' , relief= 'flat',bd=0 , highlightthickness=0 )
pvp = tk.Button(window , text='player vs player' , image= pvp_photo ,font=('Helvetica' , fontsize) ,fg='blue', command=versus  ,  compound= 'center' , relief= 'flat' , bd=0 , highlightthickness=0 )
pve = tk.Button(window , text='player vs hockai' , font=('Helvetica' ,fontsize) ,fg = 'blue' , image= pve_photo , command=singleplayer ,  compound= 'center' , relief='flat' , bd=0 ,highlightthickness=0 )
quitall = tk.Button(window , text='I want to leave' , font=('Helvetica' , fontsize) ,fg = 'blue' , image= quitall_photo , command=quitwhole ,  compound= 'center' , relief='flat' , bd=0 ,highlightthickness=0 )


pvp.place(x = buttonstartx , y = buttonstarty + 0 * (buttonheight + 50) , width=buttonwidth , height=buttonheight)
pve.place(x = buttonstartx , y = buttonstarty + 1 * (buttonheight + 50), width=buttonwidth , height=buttonheight)
training.place(x = buttonstartx , y = buttonstarty + 2 * (buttonheight + 50), width=buttonwidth , height=buttonheight)
quitall.place(x = buttonstartx , y = buttonstarty + 3 * (buttonheight + 50) , width= buttonwidth , height=buttonheight)
pvp.bind('<Enter>' ,on_enter_pvp)
pvp.bind('<Leave>' ,on_leave_pvp)
pve.bind('<Enter>' , on_enter_pve)
pve.bind('<Leave>' , on_leave_pve)
training.bind('<Enter>' , on_enter_training)
training.bind('<Leave>' , on_leave_training)

    # Add other widgets on top of the background

window.mainloop()







