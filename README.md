# Production Defect Detection QC

Aplikasi web sederhana untuk mendeteksi cacat permukaan baja menggunakan **YOLOv8n**, **FastAPI**, dan frontend berbasis **HTML/CSS/JavaScript**.

Project ini dibuat sebagai prototype sistem quality control berbasis computer vision. Pengguna dapat mengunggah gambar permukaan baja, lalu sistem akan menampilkan hasil deteksi berupa **bounding box**, **jenis cacat**, dan **confidence score**.

---

## Overview

Pada proses produksi, pemeriksaan cacat permukaan material masih sering dilakukan secara manual. Cara manual membutuhkan waktu, bergantung pada ketelitian manusia, dan berpotensi menghasilkan inkonsistensi.

Project ini membangun prototype sistem deteksi cacat permukaan baja menggunakan model object detection **YOLOv8n**. Model dilatih menggunakan dataset **NEU-DET**, kemudian diintegrasikan ke backend **FastAPI** dan frontend sederhana agar hasil deteksi dapat digunakan melalui aplikasi web.

---

## Defect Classes

Model mendeteksi 6 jenis cacat permukaan baja:

1. `crazing`
2. `inclusion`
3. `patches`
4. `pitted_surface`
5. `rolled-in_scale`
6. `scratches`

---

## Features

* Upload gambar permukaan baja
* Deteksi cacat menggunakan YOLOv8n
* Menampilkan hasil gambar dengan bounding box
* Menampilkan label kelas cacat
* Menampilkan confidence score
* API response dalam format JSON
* Frontend web sederhana untuk demo

---

## Tech Stack

* Python
* YOLOv8n / Ultralytics
* FastAPI
* OpenCV
* HTML
* CSS
* JavaScript

---

## Project Structure

```text
production-defect-detection-qc/
├── backend/
│   ├── app/
│   │   └── index.html
│   ├── results/
│   │   └── .gitkeep
│   ├── uploads/
│   │   └── .gitkeep
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
```

---

## Model

Model yang digunakan adalah **YOLOv8n**.

YOLOv8n dipilih karena ringan, cepat, dan cocok untuk prototype object detection. Model ini digunakan untuk mendeteksi lokasi cacat pada gambar permukaan baja sekaligus mengklasifikasikan jenis cacatnya.

Model hasil training disimpan di:

```text
backend/weights/best.pt
```

---

## Model Performance

Hasil evaluasi baseline model:

| Metric    | Score |
| --------- | ----: |
| Precision | 0.696 |
| Recall    | 0.713 |
| mAP50     | 0.761 |
| mAP50-95  | 0.420 |

Model sudah dapat digunakan untuk demo baseline. Namun, model belum sepenuhnya production-ready. Beberapa kelas seperti `crazing` masih memiliki confidence yang relatif rendah dan dapat ditingkatkan dengan tuning lanjutan.

---

## How to Run

### 1. Clone Repository

```bash
git clone https://github.com/tottifawwazr/production-defect-detection-qc.git
cd production-defect-detection-qc
```

---

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

---

### 3. Activate Virtual Environment

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Command Prompt:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Run Backend

```bash
uvicorn backend.main:app --reload
```

Jika berhasil, terminal akan menampilkan server berjalan di:

```text
http://127.0.0.1:8000
```

---

### 6. Open Web App

Buka browser:

```text
http://127.0.0.1:8000/app
```

---

### 7. Open API Documentation

FastAPI menyediakan dokumentasi API otomatis di:

```text
http://127.0.0.1:8000/docs
```

Endpoint utama:

```text
POST /predict
```

Endpoint ini digunakan untuk mengunggah gambar dan mendapatkan hasil deteksi.

---

## API Response Example

Contoh response dari endpoint `/predict`:

```json
{
  "filename": "pitted_surface_245.jpg",
  "total_detections": 2,
  "detections": [
    {
      "class_id": 3,
      "class_name": "pitted_surface",
      "confidence": 0.8818,
      "bbox": {
        "x1": 44.52,
        "y1": 12.84,
        "x2": 187.61,
        "y2": 154.23
      }
    },
    {
      "class_id": 2,
      "class_name": "patches",
      "confidence": 0.8119,
      "bbox": {
        "x1": 0.0,
        "y1": 23.15,
        "x2": 45.63,
        "y2": 65.77
      }
    }
  ],
  "result_image_url": "/results/example_result.jpg"
}
```

---

## Web App Preview

Alur penggunaan aplikasi:

1. Buka halaman web app
2. Pilih gambar permukaan baja
3. Klik tombol **Detect Defect**
4. Sistem menampilkan gambar hasil deteksi
5. Sistem menampilkan tabel class dan confidence score

---

## Dataset

Dataset yang digunakan pada tahap training adalah **NEU Surface Defect Database / NEU-DET**.

Dataset mentah tidak disertakan di repository ini agar ukuran repository tetap ringan. Folder dataset, hasil training, dan file prediksi lokal dikecualikan melalui `.gitignore`.

---

## Training Pipeline

Alur training model:

```text
Raw NEU-DET Dataset
        ↓
Convert annotation to YOLO format
        ↓
Split dataset into train, validation, and test
        ↓
Train YOLOv8n model
        ↓
Evaluate model
        ↓
Save best model
        ↓
Integrate model into FastAPI backend
```

Script training tersedia di:

```text
training/scripts/
```

---

## Notes

Repository ini difokuskan untuk demo prototype. Beberapa file besar tidak disertakan, seperti:

* dataset mentah
* folder hasil training `runs/`
* virtual environment `.venv/`
* hasil upload user
* hasil prediksi sementara

Model utama yang digunakan untuk inference berada di:

```text
backend/weights/best.pt
```

---

## Limitations

Beberapa batasan project saat ini:

* Model masih baseline
* Confidence pada beberapa kelas masih relatif rendah
* Belum ada database untuk menyimpan riwayat deteksi
* Belum ada sistem login user
* Belum ada deployment cloud
* Belum ada evaluasi real-time pada data produksi asli

---

## Future Improvements

Pengembangan berikutnya yang dapat dilakukan:

* Melatih model dengan epoch lebih banyak
* Menggunakan varian YOLO yang lebih besar seperti YOLOv8s atau YOLOv8m
* Menambahkan data augmentasi
* Menambahkan confusion matrix dan visualisasi evaluasi di dashboard
* Menambahkan database untuk menyimpan histori deteksi
* Membuat frontend menggunakan React
* Melakukan deployment ke cloud server
* Menambahkan Docker agar project lebih mudah dijalankan

---

## Author

**Totti Fawwaz Reda**

Project: Production Defect Detection QC

---

## Status

Project status: **MVP / Demo Baseline Completed**

Fitur utama sudah berjalan:

* Model training selesai
* Model inference berhasil
* Backend FastAPI berjalan
* Endpoint `/predict` berhasil
* Frontend upload image berhasil
* Result image dengan bounding box berhasil ditampilkan
