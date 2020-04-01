import cv2 as cv


def draw_dots(square, circles, frame):
    i = 0
    x1 = 0
    y1 = 0
    for square in square:
        for (x, y, r) in circles:
            if cv.pointPolygonTest(square, (x, y), False) == 1:
                (x1, y1, w, h) = cv.boundingRect(square)
                cv.circle(frame, (x, y), r, (0, 50, 144), -1)
                i += 1
        cv.putText(
            frame,
            "#{}".format(i),
            (x1 - 100, y1),
            cv.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 144),
            2,
        )
        i = 0
    return frame
