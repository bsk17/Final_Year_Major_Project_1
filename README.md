# final_year_project

LBPH algorithm of facial algorithm is used. 
Haarcascade_Frontal_Face_xml file is used for feature selection of faces.

How It Works (User perspective)?
  User has to enter ID serial wise starting form 1. 
  
  Respective Name,Class, Roll NO has to be entered.
  
  Then The first process is to take the image. 
  
  On successful capture The notification label gets filled up.
  
  The user presses Train button which gives notification as Image Trained. (offline)
  
  The user uses populate folder file to upload TrainingImage folder to Google Drive, 
  from there on Google Colab can be used to train the images, once trainer file is created
  download the file to local space. (online and quick)  
  
  Then Take Image which will pop up a capture window which automatically gets shut down when image is recognized.
  
  Finally an Excel File is created named as the Class and Date of Student inside which according to Roll Number 
  the student is registered as Present.
  
Future Works...
  Deploying the whole project using Raspberry PI.
 
This project has been developed for both windows and linux platforms.
