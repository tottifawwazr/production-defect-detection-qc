# Model Card - YOLOv8n Steel Surface Defect Detection

## Model

This project uses a **YOLOv8n object detection model** for steel surface defect detection.

YOLOv8n is the lightweight variant of YOLOv8. It was selected for this MVP because it provides fast inference and is suitable for baseline object detection experiments.

---

## Intended Use

The model is intended to detect and classify surface defects from steel surface images.

This model is designed for:

* computer vision experimentation
* quality-control prototype development
* AI engineering portfolio demonstration
* baseline defect detection research

This model is not yet intended for direct production deployment.

---

## Dataset

The model was trained using the **NEU Surface Defect Database / NEU-DET**.

The dataset contains steel surface defect images with six defect classes.

---

## Classes

The model predicts the following classes:

1. `crazing`
2. `inclusion`
3. `patches`
4. `pitted_surface`
5. `rolled-in_scale`
6. `scratches`

---

## Training Setup

The dataset annotations were converted into YOLO format and split into training, validation, and test sets.

Final dataset split:

| Split      | Samples |
| ---------- | ------: |
| Train      |    1439 |
| Validation |     180 |
| Test       |     180 |

One image was skipped because it did not have a matching XML annotation file.

---

## Metrics

Global baseline performance:

| Metric    | Score |
| --------- | ----: |
| Precision | 0.696 |
| Recall    | 0.713 |
| mAP50     | 0.761 |
| mAP50-95  | 0.420 |

---

## Per-Class Metrics

| Class           | mAP50 | mAP50-95 |
| --------------- | ----: | -------: |
| crazing         | 0.467 |    0.219 |
| inclusion       | 0.874 |    0.516 |
| patches         | 0.932 |    0.604 |
| pitted_surface  | 0.842 |    0.466 |
| rolled-in_scale | 0.560 |    0.232 |
| scratches       | 0.891 |    0.485 |

---

## Strengths

The model performs relatively well on:

* `patches`
* `scratches`
* `inclusion`

These classes achieved stronger mAP50 results compared to other classes.

---

## Limitations

Current model limitations:

* Baseline model only
* Lower performance on `crazing`
* Lower performance on `rolled-in_scale`
* Not trained on real OPPO manufacturing data
* Not validated in a real production environment
* No production monitoring pipeline yet
* No drift detection or continuous evaluation
* No database-backed prediction audit trail yet

---

## Ethical and Operational Considerations

This model should not be used as the only decision-making tool for production quality control.

For real manufacturing deployment, the model should be validated with domain-specific production data and used as a decision-support system alongside human quality-control review.

---

## Future Improvements

Recommended improvements:

* Use YOLOv8s or YOLOv8m for higher accuracy
* Train with more epochs
* Add stronger data augmentation
* Collect real production defect images
* Add database logging for prediction history
* Add Docker support
* Add production monitoring dashboard
* Add model versioning
* Add confidence-threshold calibration
* Evaluate false positives and false negatives per defect class

---

## Status

Current status: **MVP / Demo Baseline**

The model is functional for prototype demonstration and portfolio use, but further validation is required before production deployment.
