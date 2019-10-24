"""
"""

from random import randint
from math import pi, cos, sin, floor

import logging

import cv2
import numpy as np
import pymunk


# ?                            Classes


class Map(object):
    """ The map.

    Procedural dungeon generation
    """
    # Map object. It define a Room with spetial properties

    rooms_list = []
    map_table = []
    x_max = 512
    y_max = 512
    x_length_max = 50
    x_length_min = 10
    y_length_max = 50
    y_length_min = 10
    img = []

    def __init__(self, name, nb_rooms, radius):
        # ? Creation of the openCV image
        self.name = name
        for x in range(self.x_max):
            self.map_table.append([])
            for y in range(self.y_max):
                self.map_table[x].append(0)
        self.img = np.zeros((self.y_max, self.x_max, 3), np.uint8)

        self.simulation_space = pymunk.Space()

        # ? Generation of the rooms

        self.generate_rooms(nb_rooms, radius,)
        self.draw_map(0)
        self.room_separation()

    def generate_rooms(self, nb_rooms, radius,):
        """Generation of all the rooms of a map."""

        for i in range(nb_rooms):
            rand_angle = randint(0, 359)*180/pi
            rand_dist = randint(0, radius)

            x = floor(rand_dist * cos(rand_angle) + self.x_max/2)
            y = floor(rand_dist * sin(rand_angle) + self.y_max/2)

            x_length = randint(self.x_length_min, self.x_length_max)
            y_length = randint(self.y_length_min, self.y_length_max)

            self.rooms_list.append(Room(x, y, x_length, y_length,
                                        self.simulation_space))

    def room_separation(self):
        """ Use pymunk librairy to separate the rooms"""

        for i in range(100):
            self.simulation_space.step(0.01)
            self.draw_map(0)
        # ? setup param in simulation

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


class Room(object):
    """ A basic rectangle room"""

    def __init__(self, x, y, x_len, y_len, simulation):
        self.x_len = x_len
        self.y_len = y_len
        self.weight = x_len * y_len
        self.body = pymunk.Body(self.weight, 0)
        self.body.position = x + x_len/2, y + y_len/2

        # ? definition of the shape of the object :
        points = [(x, y), (x + x_len, y),
                  (x, y + y_len), (x + x_len, y + y_len)]

        self.shape = pymunk.Poly(self.body, points)

    def draw(self, img):
        """draw the room on the map

        Arguments:
            img {OpenCV image} -- the openCV image where the room will be drawn
        """
        x, y = self.body.position
        x = floor(x)
        y = floor(y)
        cv2.rectangle(img, (x, y),
                      (x+self.x_len, y+self.y_len), (0, 255, 0), 2)
