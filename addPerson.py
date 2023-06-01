from vaccineData import createValidInpuData, VaccineData
import cv2
import os
from pprint import pprint


def cap_image():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        cv2.imshow("img1", frame)
        p_k = cv2.waitKey(1) & 0xFF
        if p_k == ord("y"):
            cv2.resize(frame, (400, 400))
            cv2.imwrite(".tmp.png", frame)
            cv2.destroyAllWindows()
            break

    cap.release()
    cv2.destroyAllWindows()
    return ".tmp.png"


if __name__ == "__main__":
    vcd = VaccineData()

    name = createValidInpuData("Enter Your Name: ")
    age = createValidInpuData("Enter Your Age: ", None, int)
    gender = createValidInpuData("Choose Your Gender", ["Male", "Female"])
    tov = createValidInpuData(
        "Choose Type of Vaccine", ["Covaxin", "CovidShield", "Sputnik V"]
    )
    nod = createValidInpuData("Number of doses taken: ", None, int)
    aadhar = createValidInpuData("Aadhar Card No: ", None, int)
    image_opt = createValidInpuData(
        "Image Option", ["Capture From Camera", "Read Image From File"]
    )

    while True:
        if image_opt == "Capture From Camera":
            ret = vcd.add_data(name, age, gender, tov, nod, aadhar, cap_image())
            os.remove(".tmp.png")
        else:
            image = createValidInpuData("Enter Image Path: ", None)
            ret = vcd.add_data(name, age, gender, tov, nod, aadhar, image)
        if ret == 0:
            break

    current = vcd.data[-1]
    current.pop("image")
    pprint(current, indent=4)
