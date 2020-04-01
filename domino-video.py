import numpy as np
import cv2 as cv
import functions as fun
import time
from threading import Thread

# arrays for dots
squares = []
domino_circles = []

# various movies to chose
# video_src = "videos/domino4.mp4"
video_src = "videos/domino5.mp4"


class ThreadedCamera(object):
    def __init__(self, src=0):
        self.capture = cv.VideoCapture(src)
        self.capture.set(cv.CAP_PROP_BUFFERSIZE, 2)

        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1 / 60
        self.FPS_MS = int(self.FPS * 1000)

        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(self.FPS)

    def show_frame(self, frame):
        cv.imshow("Domino dots counter", frame)
        cv.waitKey(self.FPS_MS)

    def grab_frame(self):
        return self.frame


if __name__ == "__main__":
    threaded_camera = ThreadedCamera(video_src)
    while True:
        try:
            frame = threaded_camera.grab_frame()

            # finding squares in which are dots
            img_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            _, thrash = cv.threshold(img_grey, 100, 255, cv.THRESH_BINARY)
            kernel = np.ones((3, 3), np.uint8)
            thrash = cv.erode(thrash, kernel, iterations=1)
            contours, _ = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
            cv.imshow("thrash squares", thrash)
            for contour in contours:
                area = cv.contourArea(contour)
                if area > 9000 and area < 43000:
                    approx = cv.approxPolyDP(
                        contour, 0.01 * cv.arcLength(contour, True), True
                    )

                    if len(approx) == 4:
                        squares.append(contour)
                        # cv.drawContours(frame, [approx], 0, (255, 255, 255), 6)

            # finding dots
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            gray = cv.medianBlur(gray, 13)
            cv.imshow("thrash dots", gray)
            circles = cv.HoughCircles(
                gray,
                cv.HOUGH_GRADIENT,
                1,
                30,
                param1=60,
                param2=30,
                minRadius=0,
                maxRadius=0,
            )
            detected_circles = np.uint16(np.around(circles))

            for (x, y, r) in detected_circles[0, :]:
                if r < 25 and r > 6:
                    domino_circles.append((x, y, r))
            frame = fun.draw_dots(squares, domino_circles, frame)
            # cv.putText(
            #     frame,
            #     "Total number of dots: {}".format(len(domino_circles)),
            #     (15, 50),
            #     cv.FONT_HERSHEY_SIMPLEX,
            #     1,
            #     (0, 0, 144),
            #     4,
            # )
            squares = []
            domino_circles = []
            threaded_camera.show_frame(frame)
        except AttributeError:
            pass
