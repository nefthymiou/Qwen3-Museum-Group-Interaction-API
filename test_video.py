import requests
import cv2
import os
import json
import time

url = "http://127.0.0.1:5555/api/relations"
output_folder = "output_frames"
os.makedirs("output_frames", exist_ok=True) 


video = cv2.VideoCapture('statesHD_out.mp4')
fps = int(video.get(cv2.CAP_PROP_FPS))  # Get original frame rate
frame_count = 0
saved_count = 0
results = []

while True:
    success, frame = video.read()
    if not success:
        break

    # Save only 1 frame for every 'fps' number of frames
    if frame_count % 500 == 0:
        filename = os.path.join(output_folder, f"frame_{saved_count:04d}.jpg")
        print(filename)
        cv2.imwrite(filename, frame)
        saved_count += 1
        data = {"message": {
                "text": "Describe the interaction with the guide",
                "files": [filename]}}
        res = requests.post(url, json=data) 
        if res.status_code == 200:
            results.append([frame_count, res.json()]) 
        else:
            print(f"Error on frame {frame_count}: {res.status_code}")    
        print(f"the result for the frame {frame_count} is")
        print(res.json())
    
    
    frame_count += 1
video.release()

# --- Auto save output JSON ---
os.makedirs("output_json", exist_ok=True)  # Folder created automatically
timestamp = int(time.time())
filename2 = f"output_json/relations_{timestamp}.json"

with open(filename2, "w") as f:
    json.dump(results, f, indent=2)

print(f"Saved structured output → {filename2}")


