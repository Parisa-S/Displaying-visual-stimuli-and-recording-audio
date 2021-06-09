# -*- coding: utf-8 -*-
"""

@author: Parisa

This program displays visual stimuli (images) involving text or numbers to a 
person (i.e. "speaker") and records his/her voice into an audio clip, while 
he/she reads aloud the visual stimuli.

The speaker is notified with a brief beep sound at the beginning of each image,
 which is displayed for a time window of 4 seconds. After the notification, 
 audio recordings starts and goes on until  the end of the time window. As the 
 time window is finished, an audio clip is saved.  Subseqently, the  current 
 image is flushed and the next image (e.g. a word or number) is displayed. 
 
The outputs of the program are (i) an audio clip for each image and (ii) the 
ist of words/numbers appearing on the images stored in a text file. 

Parisa Supitayakul

"""


import tkinter as tk
import winsound
from datetime import datetime
import numpy as np

import sounddevice as sd
from scipy.io.wavfile import write

"""
INFILE cnotains a list of file names of images to be displayed. The options for 
INFILE are country.txt, capital.txt, elements. txt.
"""
INFILE = "elements.txt" 

OUT_FPATH = 'recordings/' + INFILE.replace('.txt','/') 

DUR_IMAGE = 4000 # display duration of each image (msec)
DUR_INTERMISSION = 1000 # intermission duration before the next image appears (msec)
FSAMPLING = 44100  # sampling rate of audio (samples/sec)
REC_DURATION = 4 # duration of audio recordings (sec)

pointer = 0 # for pointing to the current row in the output text file
data = []
myrecording = np.array(data)


def setup_window():
    """
    Set up the tk window with tex label 
    param: pady (pixel) is the distance from top of the text label
    """
    global text
    
    main_screen.attributes('-fullscreen', True)
    text = tk.Label(main_screen,text='SET UP', font="none 40 bold",anchor="center")
    text.pack(pady=500)

    
def update_text():
    """
    Automatic update of the image (word/number)
    
    Run clear_text function after DUR_IMAGE msec. If all the words in the list 
    (INFILE) are finished to display, destroy the window, save the output files
    and terminate the program
    """
    
    global pointer 
    global myrecording
    
    print('Before show text:'+str(datetime.now()))
    text.configure(text=all_list[pointer]) 
    myrecording = sd.rec(int(REC_DURATION * FSAMPLING), samplerate=FSAMPLING, channels=1)  
    main_screen.after(DUR_IMAGE, clear_text)

        
def clear_text():
    """
    Export audio file and display a blank screen for 10 msec.
    After the blank screen, run play_sound
    """
    
    global pointer 
    
    write(OUT_FPATH + str(all_list[pointer])+'.wav', FSAMPLING, myrecording)
    text.configure(text=' ')
    pointer +=1
    
    if pointer != len(all_list):
        main_screen.after(10, play_sound)
    else:
        main_screen.destroy()
        
def play_sound():
    """
    For DUR_INTERMISSION, play beep sound (for 900 msec at 500Hz)
    """
    
    print('Before play sound:'+str(datetime.now()))
    main_screen.after(DUR_INTERMISSION, update_text)
    winsound.Beep(500,900)
    print('After play sound:'+str(datetime.now()))

    
def exit(event):
    main_screen.destroy()   
   
if __name__ == '__main__':
    
    file = open(INFILE,encoding = 'utf8')
    all_list = np.loadtxt(file,\
                           delimiter='\n', usecols=(0), \
                           skiprows=0,\
                           dtype=np.str  
                           )
    
    main_screen = tk.Tk()
    setup_window()
    print(str(datetime.now()))
    
    play_sound()
    main_screen.bind("<Escape>", exit)
    main_screen.mainloop()

