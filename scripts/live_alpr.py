import cv2
import torch
import easyocr
from datetime import datetime
import csv

model = torch.hub.load('yolov5', 'custom', path='runs/train/exp/weights/best.pt', source='local')
reader = easyocr.Reader(['en'])

csv_file = open('log.csv', 'a', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'License Number'])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    results = model(frame)
    preds = results.xyxy[0]

    for *box, conf, cls in preds:
        x1, y1, x2, y2 = map(int, box)
        roi = frame[y1:y2, x1:x2]
        ocr = reader.readtext(roi)
        text = ocr[0][1] if ocr else "N/A"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        csv_writer.writerow([timestamp, text])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        print(f"[{timestamp}] Detected: {text}")

    cv2.imshow("Live ALPR", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
csv_file.close()
cv2.destroyAllWindows()
