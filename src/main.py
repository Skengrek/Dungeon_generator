# Hello

from Class import Map


i = 0
map_object = Map('New Map')
while i < 10:
    map_object.add_room('Simple')
    map_object.draw_map(100)
    i += 1
