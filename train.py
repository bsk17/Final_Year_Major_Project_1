
import tkinter as tk
from tkinter import messagebox
import cv2
import os
import os.path
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import xlWrite
import re

window = tk.Tk()
helv36 = tk.font.Font(family='Helvetica', size=36, weight='bold')
window.title("Face_Recogniser_Major_Project")
window.geometry('1280x720')
window.configure(background='blue')

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Font is a tuple of (font_family, size_in_points, style_modifier_string)
message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System", bg="Green",
                   fg="white", width=50, height=1, font=('times', 25, 'italic bold underline'))

message.place(x=195, y=20)

# to get ID of student
lbl = tk.Label(window, text="Enter ID", width=20, height=2, fg="red", bg="yellow", font=('times', 15, ' bold '))
lbl.place(x=295, y=100)

txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 15, ' bold '))
txt.place(x=595, y=115)

# to get Name of student
lbl2 = tk.Label(window, text="Enter Name", width=20, fg="red", bg="yellow", height=2, font=('times', 15, ' bold '))
lbl2.place(x=295, y=200)

txt2 = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 15, ' bold '))
txt2.place(x=595, y=215)

# to get Class of student
lbl4 = tk.Label(window, text="Enter Sec-Sem", width=20, fg="red", bg="yellow", height=2, font=('times', 15, ' bold '))
lbl4.place(x=295, y=300)

txt4 = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 15, ' bold '))
txt4.place(x=595, y=315)

# to get Roll No of student
lbl5 = tk.Label(window, text="Enter Roll No", width=20, fg="red", bg="yellow", height=2, font=('times', 15, ' bold '))
lbl5.place(x=295, y=400)

txt5 = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 15, ' bold '))
txt5.place(x=595, y=415)

# Notification Label
lbl3 = tk.Label(window, text="Notification : ", width=20, fg="red", bg="yellow", height=2,
                font=('times', 15, ' bold underline '))
lbl3.place(x=295, y=500)

message = tk.Label(window, text="", bg="yellow", fg="red", width=42, height=2, activebackground="yellow",
                   font=('times', 15, ' bold '))
message.place(x=595, y=500)

lbl3 = tk.Label(window, text="Attendance : ", width=20, fg="red", bg="yellow", height=2,
                font=('times', 15, ' bold  underline'))
lbl3.place(x=295, y=650)


message2 = tk.Label(window, text="", fg="red", bg="yellow", activeforeground="green", width=30, height=2,
                    font=('times', 15, ' bold '))
message2.place(x=595, y=650)


# function to clear the text
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text=res)


# to check if the input is number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


# function to capture the images and save in directory
def take_images():
    # get the Id, Name, Class, Roll no from textbox
    id_input = (txt.get())
    name_input = (txt2.get())
    class_input = (txt4.get())
    roll_no_input = (txt5.get())

    # to check for Id and name
    if is_number(id_input) and name_input.isalpha() and is_number(roll_no_input):
        cam = cv2.VideoCapture(0)
        harcascade_path = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascade_path)
        # sampleNum is used to get only a maximum of 60 images
        sample_number = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # incrementing sample number
                sample_number = sample_number+1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name_input + "." + id_input + '.' + str(sample_number) + ".jpg", gray[y:y+h, x:x+w])
                # display the frame
                cv2.imshow('frame', img)
            # wait for 100 milli seconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 100
            elif sample_number > 59:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + id_input + " Name : " + name_input
        # columns used for saving student details
        row = [id_input, name_input, class_input, roll_no_input]

        # we keep a single Student Details file which which will be used for all the students of all the classes
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text=res)
    # if wrong inputs are provided then we check for the cases
    else:
        if is_number(id_input) and is_number(roll_no_input):
            res = "Enter Alphabetical Name"
            message.configure(text=res)
        if name_input.isalpha() and is_number(roll_no_input):
            res = "Enter Numeric Id"
            message.configure(text=res)
        if is_number(id_input) and name_input.isalpha():
            res = "Enter Numeric Roll No"
            message.configure(text=res)


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
    message.configure(text=res)


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


# function which helps in recognizing the images
def track_images():
    # creating the LBPH recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # cv2.createLBPHFaceRecognizer()

    # reading the data from the trainer file created by training
    recognizer.read("Trainer.yml")

    # xml file containing facial features
    harcascade_path = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(harcascade_path)

    # to get the id and name of student from the csv file created
    df = pd.read_csv("StudentDetails\StudentDetails.csv")

    # to start capturing videos
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names = ['Id', 'Name', 'Class', 'RollNO', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    # variable used as flag when recognized
    accepted = False
    xl_name = 'Name'
    xl_class = 'Class'
    xl_roll_no = 0

    # recognition is performed
    while not accepted:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                # we get the name as numpy element which includes ['.......']
                aa = df.loc[df['Id'] == Id]['Name'].values

                # we find only string using regex and convert to string using numpy function
                xl_name = " ".join(re.findall("[a-zA-Z]+", np.array2string(aa)))

                # similarly we find the class of student
                xl_class = " ".join(re.findall("[a-zA-Z0-9]+", np.array2string(df.loc[df['Id'] == Id]['Class'].values)))

                # we find the roll no which is of numpy type and covert to string
                roll_no = "".join(re.findall("[0-9]", np.array2string(df.loc[df['Id'] == Id]['RollNO'].values)))
                # we then convert the above string to integer to pass as an argument later
                xl_roll_no = int(roll_no)

                # to display detail in the image frame
                tt = str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id, xl_name, xl_class, xl_roll_no, date, time_stamp]
                accepted = True

            else:
                Id = 'Unknown'
                tt = str(Id)

            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', im)
        if cv2.waitKey(1) == ord('q'):
            break

    # ts = time.time()
    # date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    # time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    # # fileName = "Attendance\Attendance_"+date+".csv"
    print(attendance)

    # we pass the argument to create an xml file according to class and date
    xlWrite.output(xl_class + ' Attendance ', xl_class, xl_roll_no, xl_name, 'yes')

    cam.release()
    cv2.destroyAllWindows()

    res = attendance
    message2.configure(text=res)


# function to perform when quit button is pressed
def close_window():
    dialog_title = 'QUIT'
    dialog_text = 'Are you sure?'
    answer = messagebox.askquestion(dialog_title, dialog_text)
    if answer == messagebox.OK:
        window.destroy()


# these are the clear button used in the layout
clearButton = tk.Button(window, text="Clear", command=clear, fg="red", bg="yellow", width=20, height=1,
                        activebackground="Red", font=('times', 15, ' bold '))
clearButton.place(x=860, y=110)

clearButton2 = tk.Button(window, text="Clear", command=clear, fg="red", bg="yellow", width=20, height=1,
                         activebackground="Red", font=('times', 15, ' bold '))
clearButton2.place(x=860, y=210)

clearButton3 = tk.Button(window, text="Clear", command=clear, fg="red", bg="yellow", width=20, height=1,
                         activebackground="Red", font=('times', 15, ' bold '))
clearButton3.place(x=860, y=310)

clearButton4 = tk.Button(window, text="Clear", command=clear, fg="red", bg="yellow", width=20, height=1,
                         activebackground="Red", font=('times', 15, ' bold '))
clearButton4.place(x=860, y=410)

# these are the functional buttons used in the layout
takeImg = tk.Button(window, text="Take Images", command=take_images, fg="red", bg="yellow", width=20, height=2,
                    activebackground="Red", font=('times', 15, ' bold '))
takeImg.place(x=95, y=570)

trainImg = tk.Button(window, text="Train Images", command=train_images, fg="red", bg="yellow", width=20, height=2,
                     activebackground="Red", font=('times', 15, ' bold '))
trainImg.place(x=395, y=570)

trackImg = tk.Button(window, text="Track Images", command=track_images, fg="red", bg="yellow", width=20, height=2,
                     activebackground="Red", font=('times', 15, ' bold '))
trackImg.place(x=695, y=570)

# we should call the function close_windows() in command
quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="red", bg="yellow", width=20, height=2,
                       activebackground="Red", font=('times', 15, ' bold '))
quitWindow.place(x=995, y=570)

window.mainloop()
