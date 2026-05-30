@'
# Production Defect Detection QC

Aplikasi web sederhana untuk mendeteksi cacat permukaan baja menggunakan YOLOv8n, FastAPI, dan frontend HTML/CSS/JavaScript.

## Overview

Project ini membangun sistem computer vision untuk mendeteksi cacat pada permukaan baja. Model YOLOv8n dilatih menggunakan dataset NEU-DET, lalu diintegrasikan ke backend FastAPI dan frontend sederhana agar pengguna dapat mengunggah gambar dan melihat hasil deteksi.

## Defect Classes

Model mendeteksi 6 jenis cacat:

- crazing
- inclusion
- patches
- pitted_surface
- rolled-in_scale
- scratches

## Features

- Upload gambar permukaan baja
- Deteksi cacat menggunakan YOLOv8n
- Output bounding box, label kelas, dan confidence score
- API response dalam format JSON
- Tampilan hasil deteksi pada web sederhana

## Tech Stack

- Python
- YOLOv8n / Ultralytics
- FastAPI
- OpenCV
- HTML
- CSS
- JavaScript

## Project Structure

```text
production-defect-detection-qc/
├── backend/
│   ├── app/
│   │   └── index.html
│   ├── results/
│   ├── uploads/
│   ├── weights/
│   │   └── best.pt
│   └── main.py
├── training/
│   └── scripts/
│       ├── prepare_neu_det_yolo.py
│       └── train_yolo.py
├── requirements.txt
├── .gitignore
└── README.md
