"""
Procedural dungeon generator

following the process describe by the devs of TinyKeep here :
https://www.reddit.com/r/gamedev/comments/1dlwc4/procedural_dungeon_generation_algorithm_explained/

Coded by Skengrek
"""

from src.Class import Map


i = 0
map_object = Map('New Map', 200, 100)
while i < 10:
    map_object.draw_map(100)
    i += 1
