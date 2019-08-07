# Hello
from Class import Map


mapObject = Map('New Map')
obj = mapObject.addRoom('Simple')

import cv2
import numpy as np

# Create a black image
img = np.zeros((512,512,3), np.uint8)

obj.draw(img)

cv2.imshow('Image',img)
cv2.waitKey(0)