import cv2
import random

class Map(object):
    # Room object. It define a Room with spetial properties

    def __init__(self, name):
        # Define the object Map.
        self.name = name

    def addRoom(self,room_type):
        if room_type=='Simple':
            return Simple()
            

class Room(object):
    def draw(self):
        print('Not implemented')

    def fits(self):
        print('Not Implemented') 


class Simple(Room):
    # A simple Room is a basic rectangle with size and coordinate.
    def __init__(self):
        self.x = random.randint(1,512)
        self.y = random.randint(1,512)
        self.hSize = random.randint(10,100)
        self.vSize = random.randint(10,100)

    #! override
    def draw(self,img):
        cv2.rectangle(img,(self.x,self.y),(self.x+self.hSize,self.y+self.vSize),(0,255,0),2)