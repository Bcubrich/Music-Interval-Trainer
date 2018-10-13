#%%
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 5:30 PM

Last Modified on Fri Oct 12 16:16:50 2018

@author: Bart Cubrich

This code uses matplotlib to generate  musical staff,
it plots a stating not eon that staff, and plays it.
It asks the user to guess the correct pitch a certain
interval above the starting pitch. The user can reset this
pitch to a different pitch.

In order for the plot to be the right size you need to use
a Tkinter backend.

"""


'''These parameters right up front are so you can change what range of notes you
will be given'''

global _8va
global _8va_cleff
global random_8v
random_8v=False         #If True randomly go up and down octaves while playing
_8va_cleff=False         #If True show the notes on a normal grand staff, instead of 8vb staff
_8va=False              #IF true play whatever note is started on an actoave higher
_8vb=False
c_low=False
treble=False
#import time

#import matplotlib
import numpy as np
#import pandas as pd

#matplotlib.use('Qt5Agg')
#import matplotlib
import matplotlib.pyplot as plt
import random
from tkinter import Tk
#from IPython import get_ipython
#get_ipython().run_line_magic('matplotlib', 'qt')
#from tkinter.filedialog import askopenfilename
import matplotlib.image as image
from matplotlib.widgets import Button

import pygame
pygame.mixer.init()
#import sys
#import wx
#import os
from inspect import getsourcefile
from os.path import abspath
from matplotlib.widgets import TextBox


source_dir=abspath(getsourcefile(lambda:0))
source_dir=source_dir.split('<')[0]

global note_dict
global note_dict_sharp
global note_dict_flat
global note_dict_inv
global int_dict
global int_dict_inv
global notes
global intervals
global note_plot
global note_dict_full
global new_note
#global note_name
global quaver
global _8vb
global c_low
global treble
#list1=[]
#directory ='C:/Users/Bart/Network/Interval Trainer/Pitches/'
#import os
#for filename in os.listdir(directory):
#    if filename.endswith(".png") or filename.endswith(".mp3"):
#        files=str(os.path.join(directory, filename)).split('/')
#        test=files[-2]+'/'+files[-1]
#        list1.append(test)
#
#        continue
#    else:
#        continue
#print(list1)

note_dict={'A': 1, 'A#/Bb':2, 'B':3, 'C':4,'C#/Db':5,'D':6,'D#/Eb':7,'E':8,'F':9,'F#/Gb':10,'G':11,'G#/Ab':12}
note_dict_full={'A': 1, 'A#':2,'Bb':2, 'B':3, 'Cb':3, 'B#':4,'C':4,'C#':5,'Db':5,'D':6,'D#':7,'Eb':7,'E':8, 'Fb':8, 'E#':9,'F':9,'F#':10, 'Gb':10,'G':11,'G#':12,'Ab':12}
note_dict_sharp={'A': 4, 'A#':4, 'B':5, 'C':6,'C#':6,'D':7,'D#':7,'E':1,'F':2,'F#':2,'G':3,'G#':3}
note_dict_flat={'A': 4, 'Bb':5, 'B':5, 'C':6,'Db':7,'D':7,'Eb':8,'E':1,'F':2,'Gb':3,'G':3,'Ab':4}
interval_lines={'P1':0, 'm2':1, 'M2':1, 'm3':2, 'M3':2, 'P4':3,'A4(TT)':3, 'P5':4, 'm6':5, 'M6':5, 'm7':6, 'M7':6, 'P8':7, 'A8':7}

line_name_dict={'E':1,'F':2,'G':3,'A':4,'B':5,'C':6,'D':7}
note_dict_inv=dict()
int_dict=dict()
int_dict_inv=dict()
note_dict_full_inv=dict()
line_name_dict_inv=dict()
notes=list(note_dict.keys())
spelling_dict=dict()
#filename=get_dat()
#im = image.imread('C:/Users/Bart/Network/Interval Trainer/G cleff.png')
g_cleff_8vb=image.imread(source_dir+'/Images/G cleff 8vb.png')
f_cleff_8vb=image.imread(source_dir+'/Images/F cleff 8vb.png')
quaver='$\u2669$'

for key, note in zip(note_dict.keys(), note_dict.values()):
   note_dict_inv[note]=key

for key, note in zip(note_dict_full.keys(), note_dict_full.values()):
   note_dict_full_inv[note]=key

for key, note in zip(line_name_dict.keys(), line_name_dict.values()):
   line_name_dict_inv[note]=key

for note in note_dict_full.keys():
    spelling_dict[note]=note
odd_spelling={'E#':'F', 'B#':'C', 'Ax':'B','Bx':'C#', 'Cx':'D', 'Dx':'E',
              'Ex':'F#','Fx':'G', 'Cb':'B', 'Ebb':'D', 'Fb':'E', 'Bbb':'A',
              'Dbb':'C', 'Fbb':'Eb', 'Gbb':'F', 'Abb':'G', 'Cbb':'B', 'Gx':'A'}
for note1, note2 in zip(odd_spelling.keys(), odd_spelling.values()):
    spelling_dict[note1]=note2

#print (spelling_dict)
intervals=('P1', 'm2', 'M2', 'm3', 'M3', 'P4','A4(TT)', 'P5', 'm6', 'M6', 'm7', 'M7', 'P8', 'A8')

for i in range(0,14):
    int_dict[intervals[i]]=i

for interval, semitone in zip(int_dict.keys(), int_dict.values()):
   int_dict_inv[semitone]=interval


def initial_note():
    note=random.choice(notes)
#    note='B'                   #need to kill this for full effect
    rand=int(np.random.randint(2, size=1))
#    rand=1                          #kill this as well


    if len(note)>1:
        note=note.split('/')[rand]
        if rand ==0:
            note_plot=note_dict_sharp.get(str(note))
            sign='$\u266f$'
        else:
            note_plot=note_dict_flat.get(str(note))
            sign='$\u266d$'
    else:
        note_plot=note_dict_sharp.get(str(note))
        sign=''
    return note, note_plot,sign




def ran_interval():
    interval=random.choice(intervals)

    interval_val=int_dict.get(str(interval))

    return interval, interval_val

def spec_interval():
    interval=random.choice(intervals)

    interval_val=int_dict.get(str(interval))

    return interval, interval_val

def raise_window(figname=None):
    if figname: plt.figure(figname)
    cfm = plt.get_current_fig_manager()
    cfm.window.activateWindow()
    cfm.window.raise_()


def get_dat():
    root = Tk()
    root.withdraw()
    root.focus_force()
    root.attributes("-topmost", True)
#    root.wm_attributes('-topmost', 1)
    filename = askopenfilename()      # Open single file

    return filename

def quit_loop():          #Get user inputs and Kill the radio button window on "Okay"
    global x
    global y
    global sx_2spercent
    global sy_2spercent
    x=float(e1.get())
    y=float(e2.get())
    sx_2spercent=float(e3.get())
    sy_2spercent=float(e4.get())
    root.destroy()




'''========================================================================
============================================================================

==========================================================================='''
class Interval_train(object):
    initial_note, note_plot, sign=initial_note()
    initial_note_val=note_dict_full.get(str(initial_note))

    '''randomly go up an octave'''

    bool_ran=1
    bool_ran2=1
    if random_8v==True:
        bool_ran=np.random.randint(2, size=1)
        bool_ran2=np.random.randint(2, size=1)
        #bool_ran=0 #(or not randomly)
        if bool_ran == 0:
            g_cleff_8vb=image.imread(source_dir+'/Images/G cleff.png')
            f_cleff_8vb=image.imread(source_dir+'/Images/F cleff.png')
        pos_neg=1 if random.random() < 0.5 else -1
        note_plot+=int(7*pos_neg*bool_ran2)
    if _8va_cleff == True:
        bool_ran=0
        g_cleff_8vb=image.imread(source_dir+'/Images/G cleff.png')
        f_cleff_8vb=image.imread(source_dir+'/Images/F cleff.png')
    if _8va == True:
        note_plot+=7
    if _8vb == True:
        note_plot+=-7
    if treble == True:
        bool_ran=0
        note_plot+=-7

#    def print_interval(interval_,a_b,initial_note):
#        print('What is a ' + interval_ + ' ' + a_b + ' ' + initial_note + '?')


    interval_, interval_val_=ran_interval()
    above_or_below=1 if random.random() < 0.5 else -1
    a_b= 'above' if above_or_below==1 else 'below'



    staff, staff_ax=plt.subplots(figsize=(6, 4))
    staff_ax.axhline(y=1, color='0', linestyle='-')
    staff_ax.axhline(y=3, color='0', linestyle='-')
    staff_ax.axhline(y=5, color='0', linestyle='-')
    staff_ax.axhline(y=7, color='0', linestyle='-')
    staff_ax.axhline(y=9, color='0', linestyle='-')
    staff_ax.axhline(y=-3, color='0', linestyle='-')
    staff_ax.axhline(y=-5, color='0', linestyle='-')
    staff_ax.axhline(y=-7, color='0', linestyle='-')
    staff_ax.axhline(y=-9, color='0', linestyle='-')
    staff_ax.axhline(y=-11, color='0', linestyle='-')
    staff_ax.set_ylim(-15,25)
    staff_ax.set_xlim(0,10)
    staff_ax.axis('off')
    note_query=staff_ax.text(-1,12,'What is a ' + interval_ + ' ' + a_b + ' ' + 'this note?', size=12, weight='bold')
    new_note_plot=0

    if sign =='$\u266f$':
        sign_offset_init=0
    else:
        sign_offset_init=1




    initial_note_plot,=staff_ax.plot(5-0.1,note_plot+3.75, marker=quaver, markersize=50, color='0')
    initial_note_sign,=staff_ax.plot(4.4,note_plot+sign_offset_init, marker=sign, markersize=25, color='0')
    #staff_ax.plot(5,note_plot, marker='o',color='r')
    #plt.text(1,5, s=u"\U0001D11E", family="Times New Roman")
    #staff_ax.text(0,16,'What note is this?', fontsize=20)

    staff_ax.imshow(g_cleff_8vb, aspect='auto', extent=(0.2, 1.2, -2.5, 10), zorder=-1)
    staff_ax.imshow(f_cleff_8vb, aspect='auto', extent=(0.2, 1.35, -9, -3.25), zorder=-1)

    '''Plot barlines'''
    x1=(0,0)
    x2=(10,10)
    y1=(-11,9)
    staff_ax.plot(x1,y1,linestyle='-',color='0')
    staff_ax.plot(x2,y1,linestyle='-',color='0')
    sign_plot,=staff_ax.plot(0,0, alpha=0)
    sign_plot2,=staff_ax.plot(0,0, alpha=0)
    check_mark,=staff_ax.plot(0,0, alpha=0)
    sound_file=None
    sound_file2=None

    '''Draw Ledger Lines'''
    c_ledger=None
    ledger1=None
    ledger2=None
    ledger3=None
    ledger4=None
    error1=0
    error2=0
    note_name=''
    if note_plot==-1:
        c_ledger,=staff_ax.plot(5,note_plot, marker='_', markersize=30, mew=2, color='0')
    if note_plot>10:
        ledger1,=staff_ax.plot(5,11, marker='_', markersize=30, mew=2, color='0') if note_plot>=11 else staff_ax.plot(0,0, alpha=0)
        ledger2,=staff_ax.plot(5,13, marker='_', markersize=30, mew=2, color='0') if note_plot>=13 else staff_ax.plot(0,0, alpha=0)
        ledger3,=staff_ax.plot(5,15, marker='_', markersize=30, mew=2, color='0') if note_plot>=15 else staff_ax.plot(0,0, alpha=0)
        ledger4,=staff_ax.plot(5,17, marker='_', markersize=30, mew=2, color='0') if note_plot>=17 else staff_ax.plot(0,0, alpha=0)

    pressed=0
    answer=staff_ax.text(9, 12, "", size=14, weight='bold')
#    print_interval(interval_,a_b,initial_note)

    '''Play the note sound based on what octave we are in, this depends
    on if the clef shows in an 8vb cleff or not'''
#    pitch_num= '2' if initial_note=='A' or initial_note=='A#' or initial_note=='Bb' or initial_note=='B' else '3'
    pitch_num= 2 if note_plot < 6 else 3
    pitch_num = 4 if note_plot>12 else pitch_num
    pitch_num = 1 if note_plot<-1 else pitch_num
    pitch_num=pitch_num -1 if initial_note=='Cb' else pitch_num
    pitch_num =pitch_num+1
    pitch_num =pitch_num +1 if bool_ran ==0 else pitch_num
    spellcheck=spelling_dict.get(initial_note)
    sound_file2=source_dir+'/Pitches/'+str(spellcheck)+str(pitch_num)+'.wav'
    pygame.mixer.music.load(sound_file2)
    pygame.mixer.music.play()


    def interval(self,event):

        self.interval_, self.interval_val_=ran_interval()
        self.above_or_below=1 if random.random() < 0.5 else -1
        self.a_b= 'above' if self.above_or_below==1 else 'below'

        try:
            self.note_query
            self.note_query.remove()
        except ValueError:
            self.error1+=1
        try:
            self.new_note_plot
            self.new_note_plot.remove()
        except ValueError:
             self.error1+=1
        except AttributeError:
            self.error2+=1

        try:
            self.sign_plot
            self.sign_plot.remove()
        except ValueError:
            self.error1+=1

        self.note_query=self.staff_ax.text(-1,12,'What is a ' + self.interval_ + ' ' + self.a_b + ' this note?', size=13, weight='bold')

        try:
            self.sign_plot2
            self.sign_plot2.remove()
        except ValueError:
            self.error1+=1

        try:
            self.answer
            self.answer.remove()
        except ValueError:
            self.error1+=1

        try:
            self.c_ledger
            self.c_ledger.remove()
        except ValueError:
            self.error1+=1
        except AttributeError: 
            self.error2+=1

        try:
            self.ledger1
            self.ledger1.remove()
        except ValueError:
            self.error1+=1
        except AttributeError:
            self.error2+=1

        try:
            self.ledger2
            self.ledger2.remove()
        except ValueError:
            self.error1+=1
        except AttributeError:
            self.error2+=1
        try:
            self.ledger3
            self.ledger3.remove()
        except ValueError:
            self.error1+=1
        except AttributeError:
            self.error2+=1

        try:
            self.ledger4
            self.ledger4.remove()
        except ValueError:
            self.error1+=1
        except AttributeError:
            self.error2+=1

        try:
            self.check_mark
            self.check_mark.remove()
        except ValueError:
            self.error1+=1
        except AttributeError:
            self.error2+=1

        self.staff.show()
        self.pressed=0 if self.pressed==1 else 0

    '''=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'''
    def show_answer(self, event):
        '''this is the meat of the thing. It takes the random intervals
        and correctly classifies and plots them. The classification is
        the though part, and I am sure it was not done efficiently'''

        if self.pressed == 0:                     #this is so this only runs once, and doesn't keep plotting things. You can still hear the interval again

            new_note_val=self.initial_note_val+self.interval_val_*self.above_or_below


            new_note_val=new_note_val if new_note_val<13 else new_note_val-12
            new_note_val=new_note_val if new_note_val<13 else new_note_val-12
            new_note_val=new_note_val if new_note_val>0 else new_note_val+12
            new_note_val=new_note_val if new_note_val>0 else new_note_val+12

            new_note=note_dict_full_inv.get(new_note_val)
#            new_note_plot=note_dict_flat.get(str(new_note))

            line_inc=interval_lines.get(str(self.interval_))
            new_line=self.note_plot+line_inc*self.above_or_below
            new_line=new_line if new_line<8 else new_line-7
            new_line=new_line if new_line>0 else new_line+7
            new_line=new_line if new_line<8 else new_line-7
            new_line=new_line if new_line>0 else new_line+7

    #        print ('New line:'+str(new_line))
    #            print('New Line:' +str(new_line))
            line_name=line_name_dict_inv.get(new_line)
    #        print ('Note Line:'+line_name)

            self.note_name=line_name
            sign_offset=0
    #        if len(new_note)>1:
            self.sign=""
            mew=0.5
            sym_size=25
            if line_name==new_note:
                self.sign=""
            elif self.interval_=='P1' or self.interval_=='P8':
                self.note_name=self.initial_note
                self.sign=""

            elif line_name==new_note[:1]:
                self.sign= '$\u266d$'
                self.note_name=new_note
                sign_offset=1

            elif self.interval_=='A8':
                if self.above_or_below==1:
                    if note_dict_full.get(line_name)==note_dict_full.get(new_note):
                        self.note_name=line_name
                        self.sign= ''
                        sign_offset=0
                    elif '#' in self.initial_note:
                        self.sign= '$\u00D7$'
                        self.note_name=line_name+'x'
                        sign_offset=0
                        mew=0.05
                        sym_size=15
                    elif 'b' in self.initial_note:
                        self.note_name=line_name
                        self.sign= ''
                        sign_offset=0
                    else:
                        self.sign= '$\u266f$'
                        self.note_name=line_name+'#'
                        sign_offset=0
                else:
                    if note_dict_full.get(line_name)==note_dict_full.get(new_note):
                        self.note_name=line_name
                        self.sign= ''
                        sign_offset=0
                    elif 'b' in self.initial_note:
                        self.sign= '$\u266d$'
                        self.note_name=line_name+'bb'
                        sign_offset=1



            elif 'b' in new_note and note_dict_full.get(line_name)>note_dict_full.get(new_note):
                self.note_name=line_name
                self.sign=""

            elif 'b' in new_note and line_name=='E' and note_dict_full.get(line_name)==note_dict_full.get(new_note):
                self.note_name=line_name
                self.sign=""
                test1=note_dict_full.get(self.note_name)

            elif 'b' in self.initial_note:

                if line_name=='E' and new_note=='D':
                    self.sign= '$\u266d$'
                    self.note_name=line_name + 'b'
                    sign_offset=1
                    test1=note_dict_full.get(self.note_name)
                    test2=note_dict_full.get(new_note)
                    test_val=np.abs(test1-test2)
                    if test_val>0:
                        self.sign= '$\u266d$'
                        self.note_name=line_name+'bb'
                        sign_offset=1

                else:
                    self.sign= '$\u266d$'
                    self.note_name=line_name + 'b'
                    sign_offset=1
                    test1=note_dict_full.get(self.note_name)
                    test2=note_dict_full.get(new_note)
                    test_val=np.abs(test1-test2)
                    if test_val>0:
                        self.sign= '$\u266d$'
                        self.note_name=line_name+'bb'
                        sign_offset=1

            elif '#' in self.initial_note:
                self.sign= '$\u266f$'
                self.note_name=line_name+'#'
                sign_offset=0

                test1=note_dict_full.get(self.note_name)
                test2=note_dict_full.get(new_note)
                test_val=test1-test2
                if test_val<0 or new_note=='A' and line_name=='G' :
                    self.sign= '$\u00D7$'
                    self.note_name=line_name+'x'
                    sign_offset=0
                    mew=0.05
                    sym_size=15
                elif test_val>0:
                    self.sign=''
                    self.note_name=self.note_name[:1]

            elif note_dict_full.get(line_name)==note_dict_full.get(new_note):
                self.note_name=line_name
                self.sign=""

            elif note_dict_full.get(line_name)>note_dict_full.get(new_note):
                self.sign= '$\u266f$'
                self.note_name=line_name+'#'
                sign_offset=0

            else:
                self.sign= '$\u266f$'
                self.note_name=line_name+'#'
                sign_offset=0

            line_abs=self.note_plot+line_inc*self.above_or_below
            note_num= 2 if line_abs < 6 else 3
            note_num = 4 if line_abs>12 else note_num
            note_num = 1 if line_abs<-1 else note_num
            note_num=note_num -1 if self.note_name=='Cb' else note_num
            note_num+=1
            note_num =note_num+1 if self.bool_ran==0 else note_num
            note_num =note_num+1 if self.note_name=='B#' else note_num
            spellcheck=spelling_dict.get(self.note_name)
            self.sound_file=source_dir+'/Pitches/'+str(spellcheck)+str(note_num)+'.wav'
            if event!=None:
                self.answer=self.staff_ax.text(9, 12, self.note_name, size=14, weight='bold')
                self.new_note_plot,=self.staff_ax.plot(5-0.1,line_abs+3.7, marker=quaver, markersize=50, color='0')
                self.sign_plot,=self.staff_ax.plot(4.4,line_abs+sign_offset, marker=self.sign, markersize=sym_size, color='0',mew=mew)
                if 'bb' in self.note_name:
                    self.sign_plot2,=self.staff_ax.plot(4,line_abs+sign_offset, marker=self.sign, markersize=25, color='0',mew=mew)
                else:
                    self.sign_plot2,=self.staff_ax.plot(0,0,alpha=0)

                if line_abs==-1:
                    self.c_ledger,=self.staff_ax.plot(5,line_abs, marker='_', markersize=30, mew=2, color='0')
                if line_abs>10:
                    self.ledger1,=self.staff_ax.plot(5,11, marker='_', markersize=30, mew=2, color='0') if line_abs>=11 else self.staff_ax.plot(0,0, alpha=0)
                    self.ledger2,=self.staff_ax.plot(5,13, marker='_', markersize=30, mew=2, color='0') if line_abs>=13 else self.staff_ax.plot(0,0, alpha=0)
                    self.ledger3,=self.staff_ax.plot(5,15, marker='_', markersize=30, mew=2, color='0') if line_abs>=15 else self.staff_ax.plot(0,0, alpha=0)
                    self.ledger4,=self.staff_ax.plot(5,17, marker='_', markersize=30, mew=2, color='0') if line_abs>=17 else self.staff_ax.plot(0,0, alpha=0)




                pygame.mixer.music.load(self.sound_file)
                pygame.mixer.music.play()

                self.staff.show()
                self.pressed=1


    def reset(self, event):
        '''this function clears the plot and porvides a new root note'''
        self.initial_note, self.note_plot, self.sign=initial_note()
        self.initial_note_val=note_dict_full.get(str(self.initial_note))
        self.interval_, self.interval_val_=ran_interval()
        self.above_or_below=1 if random.random() < 0.5 else -1
        self.a_b= 'above' if self.above_or_below==1 else 'below'
        bool_ran=1
        bool_ran2=1
        if random_8v==True:
            bool_ran=np.random.randint(2, size=1)
            bool_ran2=np.random.randint(2, size=1)
            #bool_ran=0 #(or not randomly)
            if bool_ran == 0:
                g_cleff_8vb=image.imread(source_dir+'/Images/G cleff.png')
                f_cleff_8vb=image.imread(source_dir+'/Images/F cleff.png')
            self.pos_neg=1 if random.random() < 0.5 else -1
            self.note_plot+=int(7*pos_neg*bool_ran2)
        if _8va_cleff == True:
            bool_ran=0
            g_cleff_8vb=image.imread(source_dir+'/Images/G cleff.png')
            f_cleff_8vb=image.imread(source_dir+'/Images/F cleff.png')
        if _8va == True:
            self.note_plot+=7
        if _8vb == True:
            self.note_plot+=-7
        if treble == True:
            self.note_plot+=-7

        


        if self.sign =='$\u266f$':
            self.sign_offset_init=0
        else:
            self.sign_offset_init=1


        try:
            self.note_query
            self.note_query.remove()
        except ValueError:
            self.error1+=1
        try:
            self.new_note_plot
            self.new_note_plot.remove()
        except ValueError:
            self.error1+=1
        except AttributeError:
            self.error2+=1

        try:
            self.initial_note_plot
            self.initial_note_plot.remove()
        except ValueError:
            self.error1+=1
        except AttributeError:
            self.error2+=1

        try:
            self.initial_note_sign
            self.initial_note_sign.remove()
        except ValueError:
            self.error1+=1
        except AttributeError:
            self.error2+=1
        try:
            self.sign_plot
            self.sign_plot.remove()
        except ValueError:
            self.error1+=1

        try:
            self.check_mark
            self.check_mark.remove()
        except ValueError:
            self.error1+=1
        except AttributeError:
            self.error2+=1

        try:
            self.sign_plot2
            self.sign_plot2.remove()
        except ValueError:
            self.error1+=1
        try:
            self.answer
            self.answer.remove()
        except ValueError:
            self.error1+=1

        self.note_query=self.staff_ax.text(-1,12,'What is a ' + self.interval_ + ' ' + self.a_b + ' ' + self.initial_note + '?', size=13, weight='bold')
        self.initial_note_plot,=self.staff_ax.plot(5-0.1,self.note_plot+3.75, marker=quaver, markersize=50, color='0')
        self.initial_note_sign,=self.staff_ax.plot(4.4,self.note_plot+self.sign_offset_init, marker=self.sign, markersize=25, color='0')

        self.staff.show()
        self.pressed=0 if self.pressed==1 else 0
        self.pitch_num= 2 if self.note_plot < 6 else 3
        self.pitch_num = 4 if self.note_plot>12 else self.pitch_num
        self.pitch_num = 1 if self.note_plot<-1 else self.pitch_num
        self.pitch_num=self.pitch_num -1 if initial_note=='Cb' else self.pitch_num
        self.pitch_num =self.pitch_num+1
        self.pitch_num =self.pitch_num +1 if self.bool_ran ==0 else self.pitch_num


        self.sound_file2=source_dir+'/Pitches/'+str(self.initial_note)+str(self.pitch_num)+'.wav'
        pygame.mixer.music.load(self.sound_file2)
        pygame.mixer.music.play()

    '''======================----------------------------======================'''
    '''------------------------------------------------------------------------'''
    '''This part sets up the results of the sound button, and the check answer
    function. For some reason teh check answer functio nis going really slow right now
    but I am note sure why, because the sounds are instantaneous.'''
    '''------------------------------------------------------------------------'''

    def root(self, event):
        pygame.mixer.music.load(self.sound_file2)
        pygame.mixer.music.play()


    def play_answer(self,event):
        self.show_answer(event=None)
        pygame.mixer.music.load(self.sound_file)
        pygame.mixer.music.play()

    def chord_tone(self,event):
        self.show_answer(event=None)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.sound_file))
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.sound_file2))

    def submit(self, text):

        try:
            self.check_mark
            self.check_mark.remove()
        except ValueError:
            self.error1+=1
        except AttributeError:
            self.error2+=1


        self.show_answer(event=None)
        if self.note_name==text:
            symbol='$\u2713$'
            color='g'
        elif spelling_dict.get(self.note_name)==text:
            symbol='$\u2713$'
            color='g'
        else:
            symbol='$\u2573$'
            color='r'
        self.check_mark,=self.staff_ax.plot(6.5, 20, marker=symbol, markersize=20, color=color,mew=2)


'''========================================================================='''
'''--------------------------------------------------------------------------'''
'''This last part is outside of the class callback, and serves to initital
the callback instance, in particular setting up the buttons and entry boxes'''






callback = Interval_train()
b1_loc = plt.axes([0.1, 0.05, 0.2, 0.075])
b2_loc = plt.axes([0.3, 0.05, 0.2, 0.075])
b3_loc = plt.axes([0.5, 0.05, 0.2, 0.075])
b4_loc = plt.axes([0.7, 0.05, 0.2, 0.075])
b5_loc = plt.axes([0.75, 0.75, 0.2, 0.075])
b6_loc = plt.axes([0.05, 0.75, 0.2, 0.075])
b7_loc = plt.axes([0.5, 0.75, 0.1, 0.075])

bshow = Button(b1_loc, 'Show Answer')
bshow.on_clicked(callback.show_answer)
breset = Button(b6_loc, 'Reset')
breset.on_clicked(callback.reset)
broot = Button(b3_loc, 'Play Root')
broot.on_clicked(callback.root)
banswer = Button(b4_loc, 'Play Answer')
banswer.on_clicked(callback.play_answer)
binterval = Button(b5_loc, 'Next Interval')
binterval.on_clicked(callback.interval)
bchord = Button(b2_loc, 'Play Together')
bchord.on_clicked(callback.chord_tone)

answer_box = TextBox(b7_loc, 'Check   \n Answer  ', initial='C')
answer_box.on_submit(callback.submit)
#filename=get_dat()

#raise_window()
