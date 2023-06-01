import os
import json
import io
from PIL import Image
import cv2
import numpy
import base64
import signal


def INT_SIG(s_no, s_fr):
    print("\nInterrupt Signal Received\nExiting....")
    exit(1)


signal.signal(signal.SIGINT, INT_SIG)

data = {
    "name": "",
    "age": "",
    "gender": "",
    "type-of-vaccine": "",
    "image": "",
    "no-of-dose": "",
    "aadhar-card-no": "",
}


def createValidInpuData(msg, avl=None, t=str) -> None:
    if not avl:
        c = input(msg)
        try:
            return t(c)
        except:
            return createValidInpuData(msg, avl, t)
    print(msg)
    for i in range(len(avl)):
        print((i + 1).__str__() + ".", avl[i])
    c = int(input("Option: "))
    try:
        return avl[c - 1]
    except:
        return createValidInpuData(msg, avl, t)


class VaccineData(object):
    def __init__(self) -> None:
        self.data = []
        super().__init__()
        if not os.path.exists("data.gz"):
            open("data.gz", "x").write("[]")
            return
        try:
            self.data = json.load(open("data.gz", "r"))
        except:
            os.remove("data.gz")
            self.data = []

    def get_details(self, id):
        return self.data[self.c[id]]

    def add_data(self, name, age, gender, tov, nod, aadhar, image):
        try:
            image = base64.b64encode(open(image, "rb").read()).decode()
        except:
            print("Invalid Image Path")
            return 13

        self.data.append(
            {
                "name": name.__str__(),
                "age": age.__str__(),
                "gender": gender.__str__(),
                "type-of-vaccine": tov.__str__(),
                "image": image,
                "no-of-dose": nod.__str__(),
                "aadhar-card-no": aadhar.__str__(),
            }
        )

        with open("data.gz", "w") as f:
            json.dump(self.data, f, indent=4)
        return 0

    def getImages(self):
        self.c = []
        if not self.data == []:
            for i in self.data:
                c_img = self.__convert_image(i["image"])
                self.c.append(c_img)
        return self.c

    def getDataSet(self):
        self.d = []
        if not self.data == []:
            for i in self.data:
                i.pop("image")
                self.d.append(i)
        return self.d

    def __convert_image(self, b64Image):
        img_data = base64.b64decode(b64Image.encode())
        img = Image.open(io.BytesIO(img_data))
        img = numpy.frombuffer(img_data, dtype=numpy.uint8)
        img = cv2.imdecode(img, flags=cv2.IMREAD_COLOR)
        return img
