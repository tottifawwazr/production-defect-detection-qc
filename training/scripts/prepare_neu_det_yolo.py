from pathlib import Path
import shutil
import random
import xml.etree.ElementTree as ET


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "NEU-DET"
OUTPUT_DIR = PROJECT_ROOT / "dataset"

CLASSES = [
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches",
]


def reset_output_dir():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    for split in ["train", "val", "test"]:
        (OUTPUT_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
        (OUTPUT_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)


def voc_to_yolo_bbox(width, height, xmin, ymin, xmax, ymax):
    x_center = ((xmin + xmax) / 2) / width
    y_center = ((ymin + ymax) / 2) / height
    box_width = (xmax - xmin) / width
    box_height = (ymax - ymin) / height

    return x_center, y_center, box_width, box_height


def convert_xml_to_yolo(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    yolo_lines = []

    for obj in root.findall("object"):
        class_name = obj.find("name").text.strip()

        if class_name not in CLASSES:
            print(f"[WARNING] Unknown class: {class_name} in {xml_path.name}")
            continue

        class_id = CLASSES.index(class_name)

        bbox = obj.find("bndbox")
        xmin = float(bbox.find("xmin").text)
        ymin = float(bbox.find("ymin").text)
        xmax = float(bbox.find("xmax").text)
        ymax = float(bbox.find("ymax").text)

        x_center, y_center, box_width, box_height = voc_to_yolo_bbox(
            width, height, xmin, ymin, xmax, ymax
        )

        yolo_lines.append(
            f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"
        )

    return yolo_lines


def collect_pairs(split_name):
    image_dir = RAW_DATA_DIR / split_name / "images"
    annotation_dir = RAW_DATA_DIR / split_name / "annotations"

    if not image_dir.exists():
        raise FileNotFoundError(f"Image folder not found: {image_dir}")

    if not annotation_dir.exists():
        raise FileNotFoundError(f"Annotation folder not found: {annotation_dir}")

    image_paths = []

    for extension in [".jpg", ".jpeg", ".png", ".bmp"]:
        image_paths.extend(
            [
                path
                for path in image_dir.rglob("*")
                if path.is_file() and path.suffix.lower() == extension
            ]
        )

    pairs = []

    for image_path in sorted(image_paths):
        xml_path = annotation_dir / f"{image_path.stem}.xml"

        if xml_path.exists():
            pairs.append((image_path, xml_path))
        else:
            print(f"[WARNING] Missing XML for image: {image_path.name}")

    print(f"[INFO] Found {len(image_paths)} images in {split_name}")
    print(f"[INFO] Matched {len(pairs)} image-annotation pairs in {split_name}")

    return pairs


def save_pairs(pairs, target_split):
    for image_path, xml_path in pairs:
        target_image = OUTPUT_DIR / "images" / target_split / image_path.name
        target_label = OUTPUT_DIR / "labels" / target_split / f"{image_path.stem}.txt"

        shutil.copy2(image_path, target_image)

        yolo_lines = convert_xml_to_yolo(xml_path)
        target_label.write_text("\n".join(yolo_lines), encoding="utf-8")

    print(f"[INFO] Saved {len(pairs)} samples to {target_split}")


def create_dataset_yaml():
    yaml_path = OUTPUT_DIR / "dataset.yaml"

    content = f"""path: {OUTPUT_DIR.resolve().as_posix()}
train: images/train
val: images/val
test: images/test

names:
"""

    for idx, class_name in enumerate(CLASSES):
        content += f"  {idx}: {class_name}\n"

    yaml_path.write_text(content, encoding="utf-8")
    print(f"[INFO] Created dataset.yaml at: {yaml_path}")


def main():
    print("[INFO] Starting NEU-DET to YOLO dataset preparation...")
    print(f"[INFO] Raw dataset path: {RAW_DATA_DIR}")
    print(f"[INFO] Output dataset path: {OUTPUT_DIR}")

    reset_output_dir()

    train_pairs = collect_pairs("train")
    validation_pairs = collect_pairs("validation")

    random.seed(42)
    random.shuffle(validation_pairs)

    val_count = len(validation_pairs) // 2
    val_pairs = validation_pairs[:val_count]
    test_pairs = validation_pairs[val_count:]

    print(f"[INFO] Train pairs: {len(train_pairs)}")
    print(f"[INFO] Val pairs: {len(val_pairs)}")
    print(f"[INFO] Test pairs: {len(test_pairs)}")

    save_pairs(train_pairs, "train")
    save_pairs(val_pairs, "val")
    save_pairs(test_pairs, "test")

    create_dataset_yaml()

    print("[DONE] Dataset is ready for YOLO training.")


if __name__ == "__main__":
    main()