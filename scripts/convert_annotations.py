# Save this as convert_annotations.py
import xml.etree.ElementTree as ET
import os

def convert(xml_folder, label_folder, image_folder):
    os.makedirs(label_folder, exist_ok=True)
    for file in os.listdir(xml_folder):
        if not file.endswith(".xml"):
            continue
        tree = ET.parse(os.path.join(xml_folder, file))
        root = tree.getroot()

        size = root.find("size")
        w = int(size.find("width").text)
        h = int(size.find("height").text)

        label_path = os.path.join(label_folder, file.replace(".xml", ".txt"))
        with open(label_path, "w") as out_file:
            for obj in root.iter("object"):
                cls_id = 0  # Only 1 class: license plate
                xmlbox = obj.find("bndbox")
                xmin = int(xmlbox.find("xmin").text)
                ymin = int(xmlbox.find("ymin").text)
                xmax = int(xmlbox.find("xmax").text)
                ymax = int(xmlbox.find("ymax").text)

                x_center = ((xmin + xmax) / 2) / w
                y_center = ((ymin + ymax) / 2) / h
                width = (xmax - xmin) / w
                height = (ymax - ymin) / h

                out_file.write(f"{cls_id} {x_center} {y_center} {width} {height}\n")

# Correct usage:
convert("../data/xml/train", "../data/labels/train", "../data/images/train")
convert("../data/xml/val", "../data/labels/val", "../data/images/val")
