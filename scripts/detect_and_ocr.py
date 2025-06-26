import torch
import cv2
import easyocr

model = torch.hub.load('yolov5', 'custom', path='runs/train/exp/weights/best.pt', source='local')
reader = easyocr.Reader(['en'])

def detect_plate(img_path):
    img = cv2.imread(img_path)
    results = model(img_path)
    preds = results.xyxy[0]

    for *box, conf, cls in preds:
        x1, y1, x2, y2 = map(int, box)
        roi = img[y1:y2, x1:x2]
        ocr_result = reader.readtext(roi)
        text = ocr_result[0][1] if ocr_result else "N/A"
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(img, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        print(f"Detected: {text}")

    cv2.imshow("Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detect_plate("sample.jpg")
