import cv2
import easyocr
import matplotlib.pyplot as plt
from gtts import gTTS
import os
import pyttsx3
import ffmpeg
engine = pyttsx3.init()
engine.runAndWait()

#imagen
#https://omes-va.com/easyocr-python-opencv/
#audio
#https://pypi.org/project/pyttsx3/
#read image
image_path = '/home/roberto/Escritorio/traduccion/reglas.jpeg'

img = cv2.imread(image_path)

#instance text detector
reader = easyocr.Reader(["es"], gpu=False)


#detect text on image
text_ = reader.readtext(img)
todos_los_textos = []
umbral = 0.25



#draw text
for t in text_:
    
    bbox,text,score = t
    
    print(text)
    todos_los_textos.append(text)
    
    #draw bbox
    #if score > umbral:
     #   cv2.rectangle(img, bbox[0], bbox[2], (0,255,0),5)
      #  cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2)
    
#plt.imshow(img, cmap='viridis')
#plt.colorbar()
#plt.show()







#audio



import pyttsx3
language = 'es'
engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

engine.say(todos_los_textos)
engine.runAndWait()
engine.stop()

"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
engine.save_to_file(todos_los_textos, 'probando.mp3')
engine.runAndWait()

    