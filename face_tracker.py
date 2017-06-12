#pylint: disable=E1101
"""
Face Tracker
Timur Jaganov <andeniel@gmail.com>
"""
import os
import cv2
from modules.CFaceTracker import CFaceTracker

def start_video(cface):
    """start video camera"""
    video = cv2.VideoCapture(0)
    cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    process_this_frame = True
    while True:
        _, frame = video.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        if process_this_frame:
            locations, names = cface.track(small_frame)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(locations, names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def start():
    """start script"""
    cface = CFaceTracker()

    for file in os.listdir("./images"):
        if file.endswith(".jpg"):
            file_path = os.path.join("./images", file)
            title = os.path.basename(file)[:-4]
            # print(title, file_path)
            cface.add_faceimage(title, file_path)
    # cface.add_faceimage("Jaganov", "images/andeniel.jpg")
    # # cface.get_faces()

    start_video(cface)


start()
