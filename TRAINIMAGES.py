import os
from PIL import Image
import cv2
import numpy as np


# to train the images captured so far
def train_images():
    # we create LBPH recognizer
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    # we use frontal face features
    harcascade_path = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascade_path)
    faces, Id = get_images_and_label("TrainingImage")
    recognizer.train(faces, np.array(Id))

    # creating the trainer
    recognizer.save("Trainer.yml")
    res = "Image Trained"
    # +",".join(str(f) for f in Id)
    return res


# utility function
def get_images_and_label(path):
    # get the path of all the files in the folder
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]

    # create empty face list
    faces = []

    # create empty ID list
    Ids = []

    # now looping through all the image paths and loading the Ids and the images
    for imagePath in image_paths:
        # loading the image and converting it to gray scale
        pil_image = Image.open(imagePath).convert('L')

        # Now we are converting the PIL image into numpy array
        image_np = np.array(pil_image, 'uint8')

        # getting the Id from the image
        id = int(os.path.split(imagePath)[-1].split(".")[1])

        # extract the face from the training image sample
        faces.append(image_np)
        Ids.append(id)
    return faces, Ids
