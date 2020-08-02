"""
"""

from random import randint
from math import pi, cos, sin, floor, sqrt

import logging

import pymunk

import cv2
import numpy as np

# *############################################################################
# *                            Function
# *############################################################################


def do_overlap(room_1_corners, room_2_corners):
    l1_x, l1_y = room_1_corners[0]
    r1_x, r1_y = room_1_corners[1]

    l2_x, l2_y = room_2_corners[0]
    r2_x, r2_y = room_2_corners[1]

    # If one rectangle is on left side of other
    if l1_x > r2_x or l2_x > r1_x:
        return False

    # If one rectangle is above other
    if l1_y > r2_y or l2_y > r1_y:
        return False

    return True


def two_room_movement(room_1, room_2, x_middle, y_middle):
    """
    This function will test if two rooms overlap and will move the second one

    room_X : is a room object

    return False if no overlap (no room moved)
    """

    # ? Define coordinates
    x1, y1 = room_1.x, room_1.y
    x2, y2 = room_2.x, room_2.y

    # ? are they overlapping ?

    if do_overlap(room_1.get_corners(), room_2.get_corners()):

        # ? calculate which room is the far away from the center

        room_1_dist = sqrt((x1 - x_middle)*(x1 - x_middle)
                           + (y1 - y_middle)*(y1 - y_middle))
        room_2_dist = sqrt((x2 - x_middle) * (x2 - x_middle)
                           + (y2 - y_middle) * (y2 - y_middle))
        """move_unit = 2
        if x1 > x2:
            move_x = - move_unit
        else:
            move_x = move_unit

        if y1 > y2:
            move_y = - move_unit
        else:
            move_y = move_unit"""

        room_to_move = 1
        x_force = x1 - x2
        y_force = y1 - y2

        x_forces = 500 # nombre magique
        y_forces = 500 # nombre magique

        # Generate all x combination to test which is the smallest
        for (x1, x2) in [(x[0], y[0]) for x in room_1.get_corners()
                         for y in room_2.get_corners()]:
            _force = max(x1, x2) - min(x1, x2)
            if x_force > _force:
                x_force = _force

        # Generate all y combination to test which is the smallest
        for (y1, y2) in [(x[1], y[1]) for x in room_1.get_corners()
                         for y in room_2.get_corners()]:
            _force = max(y1, y2) - min(y1, y2)
            if y_force > _force:
                y_force = _force

        if room_1_dist < room_2_dist:
            room_to_move = 2

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

        self.space = pymunk.Space()

        # ? Generation of the rooms

        self.generate_rooms(nb_rooms, radius,)
        self.draw_map(0)
        self.room_separation_bis()
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
            self.space.add(tmp_room.body, tmp_room.shape)
            self.rooms_list.append(tmp_room)

    def room_separation(self):
        """ Using separation steering algorithm"""
        room_moved = True
        while room_moved:
            room_moved = False
            for base_room in self.rooms_list:
                base_room.set_color("blue")
                for move_room in self.rooms_list:
                    move_room.set_color("red")
                    self.draw_map(20)
                    move_room.set_color("green")
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

    def room_separation_bis(self):
        """
        Using physics engine
        """
        for x in range(1000):
            self.space.step(x/100000)
            self.draw_map(1)

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

    def draw_map(self, wait_time=0):
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

        self.body = pymunk.Body(self.weight/1000, pymunk.inf)
        self.body.position = self.x, self.y

        corner_1 = [x-x_len, y-y_len]
        corner_2 = [x-x_len, y+y_len]
        corner_3 = [x+x_len, y+y_len]
        corner_4 = [x+x_len, y-y_len]

        self.shape = pymunk.Poly(self.body, [corner_1, corner_2,
                                             corner_3, corner_4])

    def get_corners(self):
        """Since room coordinates define the center"""
        corner1 = [floor(self.x - (self.x_len / 2)),
                   floor(self.y - (self.y_len / 2))]
        corner2 = [floor(self.x + (self.x_len / 2)),
                   floor(self.y + (self.y_len / 2))]
        return [corner1, corner2]

    def set_color(self, name):
        if name == "green":
            self.color = (0, 250, 0)
        elif name == "blue":
            self.color = (255, 0, 0)
        elif name == "red":
            self.color = (0, 0, 250)

    def draw(self, img):
        """draw the room on the map

        Arguments:
            img {OpenCV image} -- the openCV image where the room will be drawn
        """
        self.x, self.y = self.body.position.x, self.body.position.y

        corner1 = (floor(self.x - self.x_len / 2),
                   floor(self.y - self.y_len / 2))
        corner2 = (floor(self.x + self.x_len / 2),
                   floor(self.y + self.y_len / 2))
        cv2.rectangle(img, corner1, corner2,
                      self.color, self.border_size)

