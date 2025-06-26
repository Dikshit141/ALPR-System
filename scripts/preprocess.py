import os
import xml.etree.ElementTree as ET
import pandas as pd

def xml_to_csv(xml_folder):
    rows = []
    for file in os.listdir(xml_folder):
        if file.endswith('.xml'):
            tree = ET.parse(os.path.join(xml_folder, file))
            root = tree.getroot()
            filename = root.find('filename').text
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)
            for obj in root.iter('object'):
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)
                x_center = ((xmin + xmax) / 2) / width
                y_center = ((ymin + ymax) / 2) / height
                w = (xmax - xmin) / width
                h = (ymax - ymin) / height
                rows.append([filename, 0, x_center, y_center, w, h])
    return pd.DataFrame(rows, columns=['filename', 'class', 'x_center', 'y_center', 'width', 'height'])

df = xml_to_csv('data/xml_annotations')
df.to_csv('data/annotations.csv', index=False)
