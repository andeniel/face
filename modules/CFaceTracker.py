"""
Module for init and Track Faces
Timur Jaganov <andeniel@gmail.com>
"""
import face_recognition as fc

class CFaceImage(object):
    """Record For ImageTracker"""
    def __init__(self, title, bitmap):
        print("Create new Image -> %s" % title)
        self.title = title
        self.bitmap = bitmap

class CFaceTracker(object):
    """Base Class to Init Face Tracker"""

    def __init__(self):
        print("Init FaceTracker")
        self.faces = set()
        self.lives = set()

    def add_faceimage(self, title, image_path):
        """Add new FaceImage from Image"""
        bitmap = fc.face_encodings(fc.load_image_file(image_path))[0]
        self.faces.add(CFaceImage(title, bitmap))

    def get_faces(self):
        """Get all faces"""
        print(self.faces)

    def find_lives(self, dest, targets):
        """iter lives and get"""
        for face in targets:
            match = fc.compare_faces([face.bitmap], dest)
            if match[0]:
                return face

    def track(self, small_frame):
        """track image, faces"""
        locations = fc.face_locations(small_frame)
        encodings = fc.face_encodings(small_frame, locations)
        names = []
        founded = set()

        for _, encod in zip(locations, encodings):
            face = self.find_lives(encod, self.lives)
            if face is None:
                face = self.find_lives(encod, self.faces)
                if face is None:
                    # name = "Unknown ~%s" % str(len(self.lives))
                    name = "Unknown"
                    # SEND TO SERVER, Unknown man
                    face = CFaceImage(name, encod)
                    print("Upload to server Unknown")
                    # self.faces.add(face)
                self.lives.add(face)

            founded.add(face)
            names.append(face.title)

        self.lives = founded & self.lives
        return locations, names
