import cv2
import numpy as np
import pyautogui

def click_Image(img_loc: str, reference: object, what: str):
    numbers = ["First", "Second", "Third", "Fourth", "FIfth", "Sixth", "Seventh", "Eighth", "Nineth", "Tenth"]
    input = numbers.index(what)

    user_img = cv2.imread(img_loc, cv2.IMREAD_IGNORE_ORIENTATION)
    ref_img = cv2.imread(reference, cv2.IMREAD_IGNORE_ORIENTATION)

    result = cv2.matchTemplate(ref_img, user_img, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    w = user_img.shape[1]
    h = user_img.shape[0]

    threshold = 0.58

    yloc, xloc = np.where(result >= threshold)

    ## grouping of rectangles to avoid multiple matching in a single location
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        ## duplicate so that there is at least 2 rectangles on top of each other
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    ## print how many are detected
    print(len(rectangles))

    rectangles_info = []
    rectangles = sorted(rectangles, key=lambda x: x[0])  # Sort rectangles based on x-coordinates

    for i, (x, y, w, h) in enumerate(rectangles):
        cv2.rectangle(ref_img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(ref_img, str(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        # Print coordinates
        print(f"Rectangle {i} coordinates: x={x}, y={y}")
        rectangles_info.append((x, y))

    pyautogui.click(rectangles_info[input])

    cv2.imshow('Reference', ref_img)
    cv2.waitKey()
    cv2.destroyAllWindows()

# Example usage
click_Image("models/shesh.png", "models/reference.png", "Second")


# rectangles = sorted(rectangles, key=lambda y: y[1])  # Sort rectangles based on y-coordinates