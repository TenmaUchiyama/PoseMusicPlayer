import os 
from audioplayer import AudioPlayer
import time
import cv2
import numpy as np

player = AudioPlayer('res/musics/Beggin.mp3')
player.play(loop=True)
time.sleep(5)