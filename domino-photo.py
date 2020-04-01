import numpy as np
import cv2 as cv
import functions as fun

# arrays for dots
squares = []
domino_circles = []

# frame = cv.imread("photos/domino1.png")
frame = cv.imread("photos/domino2.png")

img_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
_, thrash = cv.threshold(img_grey, 100, 255, cv.THRESH_BINARY)
kernel = np.ones((3, 3), np.uint8)
thrash = cv.erode(thrash, kernel, iterations=1)
contours, _ = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
cv.imshow("thrash squares", thrash)

for contour in contours:
    area = cv.contourArea(contour)
    if area > 9000:
        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)

        if len(approx) == 4:
            squares.append(contour)
            # cv.drawContours(frame, [approx], 0, (255, 255, 255), 6)
# finding dots
gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
gray = cv.medianBlur(gray, 11)
cv.imshow("thrash dots", gray)
circles = cv.HoughCircles(
    gray, cv.HOUGH_GRADIENT, 1, 30, param1=60, param2=30, minRadius=0, maxRadius=0
)
detected_circles = np.uint16(np.around(circles))

for (x, y, r) in detected_circles[0, :]:
    if r < 25 and r > 5:
        domino_circles.append((x, y, r))
frame = fun.draw_dots(squares, domino_circles, frame)
squares = []
domino_circles = []
cv.imshow("Domino dots counter", frame)

cv.waitKey(0)
cv.destroyAllWindows()
