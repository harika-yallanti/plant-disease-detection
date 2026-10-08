#  Plant Disease Detection AI

An AI-powered web application that identifies plant diseases from uploaded leaf images and provides the predicted disease, basic information, treatment recommendations, and prevention measures.

The application also includes a separate leaf-image validation model to prevent unrelated images from being sent to the disease detection model.

##  Project Overview

Plant diseases can negatively affect crop health and productivity. Identifying diseases at an early stage can help users take appropriate action.

This project uses Deep Learning and Transfer Learning to analyze plant leaf images and classify them into different disease categories.

The application provides:

-  Plant leaf image upload
-  Leaf/non-leaf image validation
-  AI-based disease prediction
-  Prediction confidence
-  Disease information
-  Treatment recommendations
-  Prevention measures
-  Firebase email/password authentication
-  Login, registration, and logout
-  Web-based user interface

## Features

### User Authentication

The application uses Firebase Authentication for user authentication.

Users can:

- Create an account
- Login using email and password
- Logout from the application
- Access the disease detection page only after authentication

### Leaf Image Validation

Before disease prediction, the uploaded image is checked using a separate leaf validation model.

This prevents unrelated images from being passed to the disease classification model.

Examples:

- Plant leaf → Accepted
- ID card → Rejected
- Personal photo → Rejected
- Other unrelated image → Rejected

If the uploaded image is not considered a valid leaf image, the application displays:

> Please upload a clear plant leaf image for disease detection.

### Plant Disease Classification

The application uses a MobileNetV2-based transfer learning model to classify plant leaf images.

The model currently supports 10 classes:

1. Apple – Apple Scab
2. Apple – Healthy
3. Corn – Common Rust
4. Corn – Healthy
5. Potato – Early Blight
6. Potato – Late Blight
7. Potato – Healthy
8. Tomato – Early Blight
9. Tomato – Late Blight
10. Tomato – Healthy

### Disease Information

After prediction, the application displays:

- Predicted disease
- Confidence score
- Disease description
- Treatment recommendations
- Prevention measures

Treatment and prevention information is maintained as controlled application data rather than being generated directly by the prediction model.

## Machine Learning

### Model Architecture

The disease classification model uses:

**MobileNetV2 + Transfer Learning**

MobileNetV2 is used as the feature extraction backbone with ImageNet pretrained weights.

The base model is frozen during the initial training process, and a custom classification head is added for the 10 plant classes.

### Disease Detection Pipeline

```text
Input Leaf Image
       ↓
Image Resize (224 × 224)
       ↓
MobileNetV2
       ↓
Feature Extraction
       ↓
Global Average Pooling
       ↓
Dropout
       ↓
Dense Layer
       ↓
Softmax
       ↓
Disease Prediction
