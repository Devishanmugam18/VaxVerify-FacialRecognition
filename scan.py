import numpy as np
import face_recognition as fr
import cv2
from vaccineData import VaccineData
from PIL import Image

video_capture = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


encode_face_img = lambda x: fr.face_encodings(x)[0]
data_ = VaccineData()
data_images = data_.getImages()
data_images = list(map(encode_face_img, data_images))


known_face_encondings = data_images

map_gender = lambda m: "M" if m == "Male" else "F"


def map_to_name_av(d):
    r = ""
    r += d["name"].__str__()
    # r += '[' + d['no-of-dose'].__str__() + ']'
    r += "[" + d["age"].__str__() + "]"
    r += "[" + map_gender(d["gender"]) + "]"
    if d["no-of-dose"] == 2:
        r += "[" + "Vaccinated" + "]"
    else:
        r += "[" + "Partially Vaccinated" + "]"
    return r


data_details = data_.getDataSet()
known_face_names = list(map(map_to_name_av, data_details))

while True:
    ret, frame = video_capture.read()

    rgb_frame = frame[:, :, ::-1]

    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(
        face_locations, face_encodings
    ):
        matches = fr.compare_faces(known_face_encondings, face_encoding)

        name = "NotVaccinated"

        face_distances = fr.face_distance(known_face_encondings, face_encoding)

        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        print(name)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 209, 200), 0)

        cv2.rectangle(
            frame, (left, bottom - 30), (right, bottom), (0, 209, 200), cv2.FILLED
        )
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 10, bottom - 10), font, 1.0, (30, 33, 34), 1)

    cv2.imshow("Webcam_facerecognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("p"):
        break

video_capture.release()
cv2.destroyAllWindows()
