# Hello
import numpy as np
import cv2
from Class import Map


mapObject = Map('New Map')
obj = mapObject.add_room('Simple')


# Create a black image
img = np.zeros((512, 512, 3), np.uint8)

obj.draw(img)

cv2.imshow('Image', img)
cv2.waitKey(0)
