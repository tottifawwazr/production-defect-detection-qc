from pathlib import Path
from uuid import uuid4

import cv2
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from ultralytics import YOLO
from fastapi.staticfiles import StaticFiles


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "backend" / "weights" / "best.pt"

UPLOAD_DIR = BASE_DIR / "backend" / "uploads"
RESULT_DIR = BASE_DIR / "backend" / "results"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

APP_DIR = BASE_DIR / "backend" / "app"


app = FastAPI(
    title="Steel Defect Detection API",
    description="Backend API untuk deteksi cacat permukaan baja menggunakan YOLOv8n.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/app", StaticFiles(directory=str(APP_DIR), html=True), name="app")

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model tidak ditemukan: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))


@app.get("/")
def root():
    return {
        "message": "Steel Defect Detection API is running",
        "model": str(MODEL_PATH),
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": True,
    }


@app.post("/predict")
async def predict_defect(file: UploadFile = File(...), conf: float = 0.25):
    allowed_extensions = {".jpg", ".jpeg", ".png"}

    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Format file tidak didukung. Gunakan JPG, JPEG, atau PNG."
            },
        )

    input_filename = f"{uuid4().hex}{file_ext}"
    input_path = UPLOAD_DIR / input_filename

    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())

    results = model.predict(
        source=str(input_path),
        imgsz=640,
        conf=conf,
        save=False,
    )

    result = results[0]

    output_filename = f"{Path(input_filename).stem}_result.jpg"
    output_path = RESULT_DIR / output_filename

    annotated_image = result.plot()
    cv2.imwrite(str(output_path), annotated_image)

    detections = []

    for box in result.boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        detections.append(
            {
                "class_id": class_id,
                "class_name": class_name,
                "confidence": round(confidence, 4),
                "bbox": {
                    "x1": round(x1, 2),
                    "y1": round(y1, 2),
                    "x2": round(x2, 2),
                    "y2": round(y2, 2),
                },
            }
        )

    return {
        "filename": file.filename,
        "total_detections": len(detections),
        "detections": detections,
        "result_image_url": f"/results/{output_filename}",
    }


@app.get("/results/{filename}")
def get_result_image(filename: str):
    image_path = RESULT_DIR / filename

    if not image_path.exists():
        return JSONResponse(
            status_code=404,
            content={"error": "Result image tidak ditemukan."},
        )

    return FileResponse(image_path)