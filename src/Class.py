"""This contains all class necessary to run the main code.
    It contains :
    Map
    Room
        Simple
        Etc ...
"""

import random

import cv2
import numpy as np


# ?                            Classes


class Map():
    """ Map
        This define the map object containing a list of Rooms objects.
    """
    # Map object. It define a Room with spetial properties

    rooms_list = []
    map_table = []
    x_max = 512
    y_max = 512
    img = []

    def __init__(self, name):
        # Define the object Map.
        self.name = name
        for x in range(self.x_max):
            self.map_table.append([])
            for y in range(self.y_max):
                self.map_table[x].append(0)
        self.img = np.zeros((self.y_max, self.x_max, 3), np.uint8)

    def add_room(self, room_type):
        """[summary]

        Arguments:
            room_type {str} -- The definition of the new room type

        Returns:
            Room object -- Return the object created.
        """
        room_valid = 0
        while room_valid == 0:
            if room_type == 'Simple':
                tmp_obj = Simple(len(self.rooms_list)+1,
                                 self.x_max, self.y_max)
                tmp_fits = tmp_obj.fits(self.map_table)
                self.map_table = tmp_fits[1]
                if tmp_fits[0]:
                    room_valid = 1
            else:
                tmp_obj = None
                room_valid = 1

        if tmp_obj != None:
            self.rooms_list.append(tmp_obj)
        return tmp_obj

    def get_rooms_list(self):
        """Get the list of rooms of this map object

        Returns:
            [Room] -- a table of Room object
        """
        return self.rooms_list

    def get_img(self):
        """get methods for the open CV image of the map

        Returns:
            OpenCV image -- can show the map composition
        """
        return self.img

    def draw_map(self, wait_time):
        """methods to show the map in a drawing

        Arguments:
            wait_time {int} -- the time to wait for each update (0 means to wait for an input)
        """
        for x in self.rooms_list:
            x.draw(self.img)
        cv2.imshow('Map', self.img)
        cv2.waitKey(wait_time)


class Room:
    """
        Parent class for all rooms. This help to keep the same definition
        of methods for all subclass
    """

    def draw(self, img):
        """This method will print Not implemented if the subclass did not
            override it

        Arguments:
            img {OpenCV image} -- the image were the room will be draw
        """
        print('Not implemented')

    def fits(self, map_table):
        """This method will print Not implemented if the subclass did not
            override it
        """
        print('Not Implemented')


class Simple(Room):
    """The basic class for rectangle rooms.

    Arguments:
        Room {object} -- Parent class.
    """
    # A simple Room is a basic rectangle with size and coordinate.

    def __init__(self, object_id, x_max, y_max):
        self.id = object_id
        self.x = random.randint(1, x_max)
        self.y = random.randint(1, y_max)
        self.hSize = random.randint(50, 100)
        self.vSize = random.randint(50, 100)

    def draw(self, img):
        """draw the room on the map

        Arguments:
            img {OpenCV image} -- the openCV image where the room will be drawn
        """
        cv2.rectangle(img, (self.x, self.y), (self.x+self.hSize,
                                              self.y+self.vSize), (0, 255, 0), 2)
        cv2.putText(img, str(self.id), (self.x+5, self.y+15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

    def fits(self, map_table):
        """Test if newly created room can fit

        Arguments:
            img {openCV image} -- the openCV image
            map_table {table} -- a table of the map containing the pbject
        """
        fit_value = 1

        if self.x+self.hSize > len(map_table)-5:
            fit_value = 0
        if self.y+self.vSize > len(map_table[1])-5:
            fit_value = 0
        tmp_map = map_table
        i = 0
        if fit_value == 1:
            for x_table in range(self.x, self.x+self.hSize):
                for y_table in range(self.y, self.y+self.vSize):
                    if map_table[x_table][y_table] == 1:
                        fit_value = 0
                    else:
                        map_table[x_table][y_table] = 1
                        i += 1
        if fit_value == 0:
            map_table = tmp_map
        return [fit_value, map_table]


class Corridor(Room):
    """The basic class for rectangle rooms.

    Arguments:
        Room {object} -- Parent class.
    """
    def __init__(self, object_id, room1, room2):
        self.object_id = object_id

        #
