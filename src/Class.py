"""This contains all class necessary to run the main code.
    It contains :
    Map
    Room
        Simple
        Etc ...
"""

import random
import cv2


class Map():
    """ Map
        This define the map object containing a list of Rooms objects.
    """
    # Map object. It define a Room with spetial properties

    rooms_list = []

    def __init__(self, name):
        # Define the object Map.
        self.name = name

    def add_room(self, room_type):
        """[summary]

        Arguments:
            room_type {str} -- The definition of the new room type

        Returns:
            Room object -- Return the object created.
        """
        if room_type == 'Simple':
            tmp_obj = Simple()
            self.rooms_list.append(tmp_obj)
            return tmp_obj
        return None

    def get_rooms_list(self):
        """Get the list of rooms of this map object

        Returns:
            [Room] -- a table of Room object
        """
        return self.rooms_list


class Room():
    def draw(self, img):
        print('Not implemented')

    def fits(self):
        print('Not Implemented')


class Simple(Room):
    # A simple Room is a basic rectangle with size and coordinate.
    def __init__(self):
        self.x = random.randint(1, 512)
        self.y = random.randint(1, 512)
        self.hSize = random.randint(10, 100)
        self.vSize = random.randint(10, 100)

    #! override
    def draw(self, img):
        cv2.rectangle(img, (self.x, self.y), (self.x+self.hSize,
                                              self.y+self.vSize), (0, 255, 0), 2)
