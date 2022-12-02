import cv2
import whisper

path = "output.mp4"

model = whisper.load_model("base")
print("Whisper model loaded.")
transcribe = model.transcribe(audio=path, fp16=False)

segments = transcribe['segments']

seconds = []
for item in range(len(segments)):
    seconds.append(round(segments[item]['start']))

text = []
for item in range(len(segments)):
   text.append(segments[item]['text'])

print(seconds)
print(text)

vidcap = cv2.VideoCapture(path)
success,image = vidcap.read()
success = True
while success:
    for sec in seconds: 
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(sec*1000))
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        cv2.imwrite("images/" + str(sec) + ".jpg", image)  
    break
else:
  print("All images are saved")
