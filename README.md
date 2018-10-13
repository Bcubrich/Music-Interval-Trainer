# Music-Interval-Trainer
Python Code For Generating Random Musical Interval, Plotting Them, and Hearing Them
Project Title: Musical Interval Trainer
Version: 1.0.0
-------------------------------------------------------------------------------
Note:
This is the first time I have attempted ot put together a package of anything.
I intend to eventually package this an .exe, and provide an installable .msi file,
but I am currently troubleshooting that. This hardly counts, as it is just a bit 
of python code, but I hope that this project will run easily on other machines. Going to 
test it on my laptop as soon as I get it uploaded.
---------------------------------------------------------------------------------

Installing:

1) To run this you just need to extract the contents of the zip file "Interval Trainer.zip" to a folder
2) Then open 'Interval_trainer_v1_1.py' in a python IDE, with QT as the backend.
	2a) You may need to specify matplotlib.use('Qt5Agg') on your IDE but on mine I specify
 		it internally in setting
3) Run the Cell as usual in your IDE
4) Depending on your IDE, system, and version of python, you will need to install some packages
    -pygame
    -tkinter
    

Errors: The current version of the code does not generate any error on my machine,
         please contact me with errors @ bcubrich@gmail.com


Accuracy of Notes: I checked all the outputs of the program in both ascending and decending intervals,
          but I cannot gaurantee the accuracy of the results. Double check them as you go...it's good practice! 
          Please contact me if you find mistakes.

Accuracy of Pitches: The pitches were generated using a MIDI pluck algorithm in audacity. I checked the
sequence of notes in every key, but occasionally I notice that the pitch gets the wrong octave. Also, future
version of this will include a bigger octave range. Also notify me of error here if you find them. 


Built With: Anaconda/Spyder IDE w/ Python 3.6.5 :: Anaconda, Inc.



Author: Bart Cubrich

Created: 10 October 2018
Last Edit: 12 October 2018


Liscense: Open File, Open Source

Acknowledgments:
Audacity, where I generated the pitches.
Many authors on stack exchange, where I search for clues to how to do this
Jessica Pachaeco, for inspiring me to learn to sing intervals
University of Ediburg Music Department, for the music theory couse
