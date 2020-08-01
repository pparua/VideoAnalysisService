# VideoAnalysisService(Service to detect breaches)

#Install all libraries by running the following command from terminal
pip3 install -r requirements.txt

# Download yolov3.weights file from the below url and put it in the folder "covid-management\model\object_detector"

https://pjreddie.com/media/files/yolov3.weights

# Command for testing images

python breach_detection_driver.py --breach mask --input image --path input/pic1.jpg --client Cognizant-Kol-SDB --loc 2100 --notify wapp
python breach_detection_driver.py --breach mask --input image --path input/pic2.jpg --client Cognizant-Kol-SDB --loc 2100
python breach_detection_driver.py --breach mask --input image --path input/pic3.jpg --client Cognizant-Kol-SDB --loc 2100
python breach_detection_driver.py --breach sd,crowded --input image --path input/pic4.jpg --client Cognizant-Kol-SDB --loc 2100 --density 10 --min=70


# Command for testing videos

python breach_detection_driver.py --breach mask --path input/video101.mp4 --client Cognizant-Kol-SDB --loc 2003 --fpr 5 --notify wapp
python breach_detection_driver.py --breach sd,crowded --path input/video2.mp4 --client Cognizant-Kol-SDB --loc 2002 --fpr 50


# Command for uploading config (Layout image from first frame of video)

python config_loader.py --path input/video2.mp4 --client Cognizant-Kol-SDB --loc 2100



# Command for contact tracing

python trace.py --loc 2002

# Input parameters description

path    -> "Path to input file"            -> mandatory
client  -> "Client ID"                     -> mandatory
loc     -> "Location ID"                   -> mandatory
breach  -> "Breach Type : mask/sd/crowded" -> optional  -> default='all'
input   -> "Input file type : image/video" -> optional  -> default='video'
notify  -> "Notify to Admin : sms/wapp/no" -> optional  -> default='sms'
fpr     -> "Frame Processing rate"         -> optional  -> default=25
density -> "Crowd threashold"              -> optional  -> default=20
min     -> "Safe distance"                 -> optional  -> default=50
