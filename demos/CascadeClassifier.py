import os
import cv2
import json

def DOMO_detect_cars_in_images(img):
    image = cv2.imread(img)
    height, width, _ = image.shape

    bottom_left = image[height//2:height, 0:width//2]
    bottom_right = image[height//2:height, width//2:width]

    car_cascade = cv2.CascadeClassifier('../utils/cars.xml')
    bottom_left_gray = cv2.cvtColor(bottom_left, cv2.COLOR_BGR2GRAY)
    bottom_right_gray = cv2.cvtColor(bottom_right, cv2.COLOR_BGR2GRAY)

    bottom_left_cars = car_cascade.detectMultiScale(bottom_left_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    bottom_right_cars = car_cascade.detectMultiScale(bottom_right_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in bottom_left_cars:
        cv2.rectangle(bottom_left, (x, y), (x + w, y + h), (0, 0, 255), 2)

    for (x, y, w, h) in bottom_right_cars:
        cv2.rectangle(bottom_right, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imwrite('bottom_left.png', bottom_left)
    cv2.imwrite('bottom_right.png', bottom_right)

DOMO_detect_cars_in_images('0000000045.png')