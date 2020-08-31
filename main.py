import cv2
import imageProcessing

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

import matplotlib.pyplot as plt
import numpy as np

# define time bounds and crop frame
video_length = 62
startT, endT = 2, 55
y1, y2, x1, x2 = 1006,1052,1750,1832
frames_per_inter = 5


custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

# load video
vidcap = cv2.VideoCapture('Forza 8.mp4')
success,image = vidcap.read()
count = 0

imagePrediction = []

# iterate through frames and extract speeds
while success:
  # crop and preprocess image
  x = np.array(image)[y1:y2,x1:x2]
  x = imageProcessing.get_grayscale(x)
  x = imageProcessing.thresholding(x)

  pred = pytesseract.image_to_string(x, config=custom_config)
  pred = pred.split('\n')[0]
  # append
  try:
      if int(pred) < 200:
          imagePrediction.append(int(pred))
      else:
          imagePrediction.append(-1)
  except:
      # not able to read speed
      imagePrediction.append(-1)

  print(pred)

  # cycle through set frames
  for _ in range(frames_per_inter):
      success,image = vidcap.read()
  count += 1

plt.scatter(list(range(len(imagePrediction))), imagePrediction)
plt.show()

time_space = video_length/len(imagePrediction)

# adjust data to fit into specified time frame
time = []
velocity = []
for i in range(len(imagePrediction)):
    if i*time_space > startT and i*time_space < endT and imagePrediction[1] != -1:
        time.append(i*time_space - startT)
        velocity.append(imagePrediction[i])

#plot data
plt.title('velocity (km/h) vs time (s)')
plt.xlabel('time (s)')
plt.ylabel('velocity (km/h)')
plt.scatter(time, velocity)
plt.show()

#export data to file
f = open('labdata.csv', 'w')
f.write('time (s), velocity(km/h), velocity(m/s)')
f.write('\n')
for i in range(len(velocity)):
    f.write('{},{},{}'.format(time[i], velocity[i], velocity[i]/3.6))
    f.write('\n')
f.close()
