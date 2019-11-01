"""
"""

from random import randint
from math import pi, cos, sin, floor, sqrt

import logging

import cv2
import numpy as np

# *############################################################################
# *                            Function
# *############################################################################


def two_room_movement(room_1, room_2, x_middle, y_middle):
    """
    This function will test if two rooms overlap and will move the second one

    room_X : is a room object

    return False if no overlap (no room moved)
    """

    # ? Define coordinates
    x1, y1, len_x1, len_y1 = room_1.x, room_1.y, room_1.x_len, room_1.y_len
    x2, y2, len_x2, len_y2 = room_2.x, room_2.y, room_2.x_len, room_2.y_len

    # ? calculate overlaping area
    dx = min(floor(x1 - len_x1 / 2), floor(x2 - len_x2 / 2)) \
        - max(floor(x1 + len_x1 / 2), floor(x2 + len_x2 / 2))
    dy = min(floor(y1 - len_y1 / 2), floor(y2 - len_y2 / 2)) \
        - max(floor(y1 + len_y1 / 2), floor(y2 + len_y2 / 2))

    room_1_dist = sqrt((x1 - x_middle)*(x1 - x_middle)
                       + (y1 - y_middle)*(y1 - y_middle))
    room_2_dist = sqrt((x2 - x_middle) * (x2 - x_middle)
                       + (y2 - y_middle) * (y2 - y_middle))

    if (dx >= 0) and (dy >= 0):
        move_unit = 2
        """if x1 > x2:
            move_x = - move_unit
        else:
            move_x = move_unit

        if y1 > y2:
            move_y = - move_unit
        else:
            move_y = move_unit"""

        room_to_move = 1
        x_force = x1 - x_middle
        y_force = y1 - y_middle

        if room_1_dist < room_2_dist:
            room_to_move = 2
            x_force = x2 - x_middle
            y_force = y2 - y_middle
        ref = min(x_force, y_force)
        if ref == 0 :
            ref = 1
        move_x, move_y = floor(x_force), floor(y_force)
        return [move_x, move_y, room_to_move]
    else:
        return False

# *############################################################################
# *                            Classes
# *############################################################################


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

        # ? Generation of the rooms

        self.generate_rooms(nb_rooms, radius,)
        self.draw_map(0)
        self.room_separation()
        self.draw_map(0)

    def generate_rooms(self, nb_rooms, radius,):
        """Generation of all the rooms of a map."""

        for i in range(nb_rooms):
            rand_angle = randint(0, 359)*180/pi
            rand_dist = randint(10, radius)

            x = floor(rand_dist * cos(rand_angle) + self.x_max/2)
            y = floor(rand_dist * sin(rand_angle) + self.y_max/2)

            x_length = randint(self.x_length_min, self.x_length_max)
            y_length = randint(self.y_length_min, self.y_length_max)

            tmp_room = Room(x, y, x_length, y_length, len(self.rooms_list))
            self.rooms_list.append(tmp_room)

    def room_separation(self):
        """ Using separation steering algorithm"""
        room_moved = True
        while room_moved:
            room_moved = False
            for base_room in self.rooms_list:
                base_room.set_color("blue")
                for move_room in self.rooms_list:
                    if base_room.id != move_room.id:
                        result = two_room_movement(base_room, move_room,
                                                   floor(self.x_max / 2),
                                                   floor(self.y_max / 2))
                        if result is not False:
                            if result[2] == 2:
                                move_room.x += result[0]
                                move_room.y += result[1]
                            else:
                                base_room.x += result[0]
                                base_room.y += result[1]
                            room_moved = True
                self.draw_map(20)
                base_room.set_color("green")
        # ? setup param in simulation
        print("Over")

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
        self.img = np.zeros((self.y_max, self.x_max, 3), np.uint8)
        cv2.rectangle(self.img, (0, 0),
                      (floor(self.x_max/2), floor(self.y_max/2)),
                      (0, 0, 255), 2)
        for room in self.rooms_list:
            room.draw(self.img)
        cv2.imshow('Map', self.img)
        cv2.waitKey(wait_time)


class Room(object):
    """ A basic rectangle room"""

    def __init__(self, x, y, x_len, y_len, _id):
        self.id = _id
        self.x = x
        self.y = y
        self.x_len = x_len
        self.y_len = y_len
        self.weight = x_len * y_len
        self.color = (0, 255, 0)
        self.border_size = 2

    def set_color(self, name):
        if name == "green":
            self.color = (0, 250, 0)
        elif name == "blue":
            self.color = (255, 0, 0)
        elif name == "red:":
            self.color = (0, 0, 250)

    def draw(self, img):
        """draw the room on the map

        Arguments:
            img {OpenCV image} -- the openCV image where the room will be drawn
        """
        corner1 = (floor(self.x - self.x_len / 2),
                   floor(self.y - self.y_len / 2))
        corner2 = (floor(self.x + self.x_len / 2),
                   floor(self.y + self.y_len / 2))
        cv2.rectangle(img, corner1, corner2,
                      self.color, self.border_size)

