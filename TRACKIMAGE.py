import pandas as pd
import datetime
import time
import xlWrite
import re
import cv2
import numpy as np


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
    return res
    message2.configure(text=res)