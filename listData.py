from vaccineData import VaccineData
from pprint import pprint
import cv2

if __name__ == "__main__":
    db = VaccineData()
    imgs = db.getImages()
    data = db.getDataSet()
    for i in range(len(imgs)):
        pprint(data[i], indent=4)
        pprint("".join(["-" for i in range(40)]))

        cv2.imshow("Image", imgs[i])
        x = cv2.waitKey(0) & 0xFF
        if x == ord("q"):
            break

cv2.destroyAllWindows()
