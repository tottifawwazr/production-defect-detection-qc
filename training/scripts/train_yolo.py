from pathlib import Path
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_YAML = PROJECT_ROOT / "dataset" / "dataset.yaml"

def main():
    print("[INFO] Starting YOLO training...")
    print(f"[INFO] Dataset config: {DATASET_YAML}")

    model = YOLO("yolov8n.pt")

    model.train(
        data=str(DATASET_YAML),
        epochs=30,
        imgsz=416,
        batch=8,
        device="cpu",
        workers=0,
        project=str(PROJECT_ROOT / "runs" / "train"),
        name="neu_det_yolov8n_baseline",
        exist_ok=True,
    )

    print("[DONE] Training completed.")


if __name__ == "__main__":
    main()