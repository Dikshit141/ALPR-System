import os
import shutil
import random

def split_dataset(image_dir, xml_dir, output_dir, split_ratio=0.8):
    os.makedirs(f"{output_dir}/images/train", exist_ok=True)
    os.makedirs(f"{output_dir}/images/val", exist_ok=True)
    os.makedirs(f"{output_dir}/xml/train", exist_ok=True)
    os.makedirs(f"{output_dir}/xml/val", exist_ok=True)

    all_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    random.shuffle(all_files)

    split_index = int(len(all_files) * split_ratio)
    train_files = all_files[:split_index]
    val_files = all_files[split_index:]

    def move_files(file_list, split):
        for xml_file in file_list:
            base = xml_file.rsplit('.', 1)[0]
            img_file = base + ".jpg"  # or .png depending on your dataset

            xml_src = os.path.join(xml_dir, xml_file)
            img_src = os.path.join(image_dir, img_file)

            xml_dst = os.path.join(output_dir, "xml", split, xml_file)
            img_dst = os.path.join(output_dir, "images", split, img_file)

            if os.path.exists(xml_src) and os.path.exists(img_src):
                shutil.copy(xml_src, xml_dst)
                shutil.copy(img_src, img_dst)

    move_files(train_files, "train")
    move_files(val_files, "val")

# Adjust these paths as needed
split_dataset(
    image_dir="../data/images", 
    xml_dir="../data/xml", 
    output_dir="../data", 
    split_ratio=0.8
)
