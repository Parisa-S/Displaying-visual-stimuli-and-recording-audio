# -*- coding: utf-8 -*-
"""

@author: Parisa

This program is used for showing and recording the audio clip as mention in section 3.4 

We displayed a slide show to the speaker on the screen of a notebook PC. 
Each slide contained a text, which can be either a word or a number.
During displayed each slide, A single audio clip was recorded.

We let the speaker know when the recording is started by play a beep sound
at the beginning of each slide. After the time limit, the program saves the audio clip
then the current slide will flush and the next slide(e.g. a word or number) will display
on the screen automatically.
 
words used to display in each slide are store in the INFILE text.


"""


import tkinter as tk
import winsound
from datetime import datetime
import numpy as np

import sounddevice as sd
from scipy.io.wavfile import write


#INFILE options are  country.txt, capital.txt, atomic_numbers_1.txt, atomic_numbers_2.txt
INFILE = "elements.txt" 

OUT_FOLDER = '2020_10_recordings/' + INFILE.replace('.txt','/') 

TIME_FOR_WORD = 4000 # time for each slide in milisecond
TIME_FOR_WAIT = 1000 # time for wait before go next slide in milisecond
FSAMPLING = 44100  # Sample rate
REC_DURATION = 4 # Duration of recording(sec) ;convert from msec

pointer = 0 #for point the row in txt file
data = []
myrecording = np.array(data)


def setup_window():
    #Set up the tk window with tex label 
    #param : pady(pixel) is the distance from top of text label
    global text
    
    main_screen.attributes('-fullscreen', True)
    text=tk.Label(main_screen,text='SET UP', font="none 40 bold",anchor="center")
    text.pack(pady=500)

    
def update_text():
    #automatic update word on screen
    #main_screen.after(5000,clear_text) -> run clear_text function after 5000 msec
    #if the word in the list is finish , destroy the screen and close the program
    
    global pointer 
    global myrecording
    
    print('before show text:'+str(datetime.now()))
    text.configure(text=all_list[pointer]) 
    myrecording = sd.rec(int(REC_DURATION * FSAMPLING), samplerate=FSAMPLING, channels=1)  
    main_screen.after(TIME_FOR_WORD, clear_text)

        
def clear_text():
    #export audio file and clear the previous word to blank label
    #wait 10 msec and run play sound
    
    global pointer 
    
    write(OUT_FOLDER + str(all_list[pointer])+'.wav', FSAMPLING, myrecording)
    text.configure(text=' ')
    pointer +=1
    
    if pointer != len(all_list):
        main_screen.after(10, play_sound)
    else:
        main_screen.destroy()
        
def play_sound():
    #go to update the next text after TIME_FOR_WAIT(1000 msec)
    #during TIME_FOR_WAIT (1000 msec) waiting ,play beep sound for 900 msec 500Hz
    
    print('before play sound:'+str(datetime.now()))
    main_screen.after(TIME_FOR_WAIT, update_text)
    winsound.Beep(500,900)
    print('after play sound:'+str(datetime.now()))

    
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
