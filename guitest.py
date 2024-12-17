import tkinter as tk
from time import sleep, time
from IPython.display import clear_output    
from subprocess import call
from tkinter import PhotoImage
import os
from PIL import Image , ImageTk

image_main = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/陳禹豪.png')
image_pvp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/playervsplayer.png')
image_pve = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/playervsplayer.png')
image_training = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/trainingpicture.png')
image_pvp_main = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/playervsplayer.png')
image_pve_main = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/playervsplayer.png')
image_defaultmode = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/defaultpicture.png')
image_extra1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/forextra1.png')
image_quitall = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/exit.png')
image_quitpvp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/exit.png')
image_quitpve = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/exit.png')
image_easy = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/weaker_ai.png')
image_difficult = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures/powerful_ai.png')
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

#photo function
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
            pixels[x , y] = (r + 50 , g + 50, b + 50)
    
    img.save(image)

#button press function
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

def quitpvpmain():
    global defaultmode , extra1 , quit
    defaultmode.destroy()
    extra1.destroy()
    quit.destroy()
    mainbackground()

def quitpvemain():
    global easy , difficult , quit
    easy.destroy()
    difficult.destroy()
    quit.destroy()
    mainbackground()

def singleplayer():
    global pvp , pve , training
    pvp.destroy()
    pve.destroy()
    training.destroy()
    pvebackground()

def ai_training():
    window.destroy()
    call(['python' , 'train2.py'])

def easymode():
    window.destroy()
    call(['python' , 'PvAI.py'])

def difficultmode():
    window.destroy()
    call(['python' , 'difficultPvAI.py'])



#button onplace function
def on_enter_pvp(event):
    pvp.config(fg = 'black')
    backgroundset_main(image_pvp)

def on_leave_pvp(event):
    pvp.config(fg='blue')
    backgroundset_main(image_main)

def on_enter_pve(event):
    pve.config(fg = 'black')
    backgroundset_main(image_pve)

def on_leave_pve(event):
    pve.config(fg='blue')
    backgroundset_main(image_main)

def on_enter_training(event):
    training.config(fg = 'black')
    backgroundset_main(image_training)

def on_leave_training(event):
    training.config(fg='blue')
    backgroundset_main(image_main)

def on_enter_quitall(event):
    quitall.config(fg='black')
    backgroundset_main(image_quitall)

def on_leave_quitall(event):
    quitall.config(fg='blue')
    backgroundset_main(image_main)

def on_enter_defaultmode(event):
    defaultmode.config(fg = 'black')
    backgroundset_pvp(image_defaultmode)

def on_leave_defaultmode(event):
    defaultmode.config(fg='blue')
    backgroundset_pvp(image_pvp_main)

def on_enter_extra1(event):
    extra1.config(fg = 'black')
    backgroundset_pvp(image_extra1)

def on_leave_extra1(event):
    extra1.config(fg='blue')
    backgroundset_pvp(image_pvp_main)

def on_enter_quitpvp(event):
    quit.config(fg='black')
    backgroundset_pvp(image_quitpvp)

def on_leave_quitpvp(event):
    quit.config(fg='blue')
    backgroundset_pvp(image_pvp_main)

def on_enter_easy(event):
    easy.config(fg = 'black')
    backgroundset_pve(image_easy)

def on_leave_easy(event):
    easy.config(fg='blue')
    backgroundset_pve(image_pvp_main)

def on_enter_difficult(event):
    difficult.config(fg = 'black')
    backgroundset_pve(image_difficult)

def on_leave_difficult(event):
    difficult.config(fg='blue')
    backgroundset_pve(image_pvp_main)

def on_enter_quitpve(event):
    quit.config(fg='black')
    backgroundset_pve(image_quitpve)

def on_leave_quitpve(event):
    quit.config(fg='blue')
    backgroundset_pve(image_pvp_main)


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
    quit = tk.Button(window , text='quit' , font=('Helvetica' , fontsize) ,image= quit_photo , command=quitpvpmain ,  compound= 'center' , relief='flat' , bd=0 ,highlightthickness=0 )

    
    defaultmode.place(x = buttonstartx , y = buttonstarty + 0 * (buttonheight + 50) , width=buttonwidth , height=buttonheight)
    extra1.place(x = buttonstartx , y = buttonstarty + 1 * (buttonheight + 50), width=buttonwidth , height=buttonheight)
    quit.place(x = buttonstartx , y = buttonstarty + 2 * (buttonheight + 50), width=buttonwidth , height=buttonheight)

    defaultmode.bind('<Enter>' , on_enter_defaultmode)
    defaultmode.bind('<Leave>' ,on_leave_defaultmode)
    extra1.bind('<Enter>' , on_enter_extra1)
    extra1.bind('<Leave>' , on_leave_extra1)
    quit.bind('<Enter>' , on_enter_quitpvp  )
    quit.bind('<Leave>' , on_leave_quitpvp)

def pvebackground():

    global easy , difficult , quit , bg_label, window , easy_photo , difficult_photo , quit_photo
    img = Image.open(image_pvp_main)

    easy_img = img.crop(bounds1)
    difficult_img = img.crop(bounds2)
    quit_img = img.crop(bounds3)

    easy_img.save('easy.png')
    difficult_img.save('difficult.png')
    quit_img.save('quit.png')

    colorset('easy.png')
    colorset('difficult.png')
    colorset('quit.png')

    window.bg_photo = tk.PhotoImage(file=image_pve_main) 
    bg_label = tk.Label(window, image=window.bg_photo)
    bg_label.image = window.bg_photo
    bg_label.place(x = 0 , y = 0, relwidth=1, relheight=1) 

    easy_photo = tk.PhotoImage(file='easy.png')
    difficult_photo = tk.PhotoImage(file='difficult.png')
    quit_photo = tk.PhotoImage(file='quit.png')


    easy = tk.Button(window , text='normal' , font=('Helvetica' , fontsize) ,image=easy_photo , command=easymode , compound= 'center' , relief= 'flat',bd=0 , highlightthickness=0 )
    difficult = tk.Button(window , text='difficult' ,font=('Helvetica' , fontsize) , image= difficult_photo , command=difficultmode  ,  compound= 'center' , relief= 'flat' , bd=0 , highlightthickness=0 )
    quit = tk.Button(window , text='quit' , font=('Helvetica' , fontsize) ,image= quit_photo , command=quitpvemain ,  compound= 'center' , relief='flat' , bd=0 ,highlightthickness=0 )

    
    easy.place(x = buttonstartx , y = buttonstarty + 0 * (buttonheight + 50) , width=buttonwidth , height=buttonheight)
    difficult.place(x = buttonstartx , y = buttonstarty + 1 * (buttonheight + 50), width=buttonwidth , height=buttonheight)
    quit.place(x = buttonstartx , y = buttonstarty + 2 * (buttonheight + 50), width=buttonwidth , height=buttonheight)

    easy.bind('<Enter>' , on_enter_easy)
    easy.bind('<Leave>' ,on_leave_easy)
    difficult.bind('<Enter>' , on_enter_difficult)
    difficult.bind('<Leave>' , on_leave_difficult)
    quit.bind('<Enter>' , on_enter_quitpve)
    quit.bind('<Leave>' , on_leave_quitpve)

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

    training = tk.Button(window , text='training' , font=('Helvetica' , fontsize) ,image=training_photo , command=ai_training , compound= 'center' , relief= 'flat',bd=0 , highlightthickness=0 )
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
    quitall.bind('<Enter>' , on_enter_quitall)
    quitall.bind('<Leave>' , on_leave_quitall)

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

def backgroundset_pve(image):
    global easy , difficult , quit , easy_photo , difficult_photo , quit_photo , bg_label
    
    img = Image.open(image)


            # Crop the image
    easy_img = img.crop(bounds1)
    difficult_img = img.crop(bounds2)
    quit_img = img.crop(bounds3)

    easy_img.save('easy.png')
    difficult_img.save('difficult.png')
    quit_img.save('quit.png')

    colorset('easy.png')
    colorset('difficult.png')
    colorset('quit.png')

# Define bounds (left, upper, right, lower) in pixels
    new_bg = tk.PhotoImage(file=image) 
    bg_label.config(image=new_bg)
    bg_label.image = new_bg
    
    easy_photo = tk.PhotoImage(file='easy.png')
    difficult_photo = tk.PhotoImage(file='difficult.png')
    quit_photo = tk.PhotoImage(file='quit.png')


    easy.config(image= easy_photo , compound='center')
    difficult.config(image=difficult_photo , compound='center')
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

training = tk.Button(window , text='training' , font=('Helvetica' , fontsize) , fg= 'blue',image=training_photo , command=ai_training , compound= 'center' , relief= 'flat',bd=0 , highlightthickness=0 )
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
quitall.bind('<Enter>' , on_enter_quitall)
quitall.bind('<Leave>' , on_leave_quitall)

    # Add other widgets on top of the background

window.mainloop()







