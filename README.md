# PlantCare AI

PlantCare AI is an AI based web application that identifies common plant diseases from uploaded leaf images. The application uses deep learning to analyze plant leaves and provides the predicted condition, confidence score, basic disease information, treatment, and prevention guidance.

## Project Overview

PlantCare AI uses a two stage image analysis process. First, a leaf validation model checks whether the uploaded image is a plant leaf. If the image is a valid leaf, the disease classification model predicts the plant condition.

The application currently supports four plant types and ten conditions using a selected subset of the PlantVillage dataset.

## Features

User authentication using Firebase Authentication

Email and password registration and login

Google authentication

Password reset functionality

Plant leaf image upload

Leaf and non leaf image validation

AI based plant disease prediction

Prediction confidence score

Disease description

Treatment information

Prevention information

Prediction history

Individual history deletion

Clear prediction history

User profile management

Profile name editing

Profile image management

Responsive web interface

FastAPI based backend API

Swagger API documentation

## Supported Plants

Apple

Corn or Maize

Potato

Tomato

## Supported Conditions

Apple Scab

Apple Healthy

Corn Common Rust

Corn Healthy

Potato Early Blight

Potato Late Blight

Potato Healthy

Tomato Early Blight

Tomato Late Blight

Tomato Healthy

## Machine Learning

The project uses MobileNetV2 with transfer learning for image classification.

The disease classification model was trained using selected images from the PlantVillage dataset.

The model accepts RGB images resized to 224 by 224 pixels.

The final classification layer contains ten output classes.

The disease classification model achieved approximately 95.91 percent validation accuracy on the selected validation dataset.

## Leaf Validation Model

A separate binary classification model is used before disease prediction.

The purpose of this model is to determine whether the uploaded image is a plant leaf.

The validation process works as follows.

Uploaded image

Leaf validation

If the image is not a leaf, the application rejects it

If the image is a leaf, it is passed to the disease classification model

This additional validation helps prevent irrelevant images from being incorrectly classified as plant diseases.

## Technologies Used

Python

TensorFlow

Keras

MobileNetV2

PlantVillage Dataset

Pillow

NumPy

FastAPI

Uvicorn

HTML

CSS

JavaScript

Firebase Authentication

LocalStorage

Git

GitHub

Visual Studio Code

## Project Structure

plant-disease-detection

backend

main.py

requirements.txt

frontend

index.html

style.css

script.js

firebase.js

login.html

auth.js

training

prepare_dataset.py

split_dataset.py

train_model.py

evaluate_model.py

prepare_validator_dataset.py

train_validator.py

test_validator.py

dataset

processed

split

validator

models

plant_disease_model.keras

leaf_validator.keras

class_names.json

validator_class_names.json

## Application Workflow

The user logs into the application using Firebase Authentication.

The user uploads a plant leaf image.

The frontend sends the image to the FastAPI backend.

The backend validates the uploaded image.

The leaf validation model checks whether the image is a plant leaf.

If the image is not a leaf, the application returns a validation message.

If the image is a valid leaf, the disease classification model analyzes it.

The model predicts the most likely plant condition.

The backend returns the prediction and confidence score.

The application displays disease information, treatment, and prevention guidance.

The prediction can be stored in the user's local prediction history.

## Backend API

The backend is developed using FastAPI.

Main prediction endpoint

POST /predict

The endpoint accepts an uploaded image and returns the prediction result as JSON.

FastAPI also provides interactive API documentation through Swagger.

Local Swagger URL

http://127.0.0.1:8000/docs

## Frontend

The frontend is developed using HTML, CSS, and JavaScript.

The dashboard contains the following sections.

Analyze

Used to upload plant images and view predictions.

Overview

Provides information about the project, supported plants, supported conditions, and workflow.

History

Displays previous predictions stored for the current user.

Profile

Displays user information and allows the user to update the profile name and profile image.

## Authentication

Firebase Authentication is used for user authentication.

The application supports email and password authentication, Google authentication, and password reset functionality.

## Storage

Prediction history and profile images are stored using browser LocalStorage.

Each user's prediction history is associated with their Firebase user ID.

Firebase Cloud Storage is not used in the current version.

## Model Training

The disease model uses the following general training process.

Dataset collection

Class selection

Image preprocessing

Train and validation split

Data augmentation

Transfer learning using MobileNetV2

Model training

Early stopping

Model checkpointing

Model evaluation

The training process uses image augmentation techniques such as random flipping, rotation, and zooming.

## Model Evaluation

The disease classification model achieved approximately 95.91 percent validation accuracy.

Evaluation was performed using validation images that were not used for model weight updates during training.

The model was also evaluated using precision, recall, F1 score, and a confusion matrix.

Some visually similar conditions, particularly tomato early blight and tomato late blight, can still be confused.

## Limitations

The current application supports only four plant types.

The current model supports ten conditions.

Prediction accuracy can be affected by image quality, lighting, background, and leaf orientation.

Diseases with similar visual symptoms can sometimes be confused.

The model was trained using a selected PlantVillage dataset and real world performance may differ from validation performance.

Prediction history and profile images are stored locally in the browser.

## Future Enhancements

Add more plant species and disease classes.

Train using a larger and more diverse real world dataset.

Improve detection of visually similar diseases.

Add image quality validation.

Add cloud based prediction history storage.

Add cloud based profile image storage.

Deploy the application to a production environment.

Add multilingual support.

Improve model explainability.

## How to Run the Project

Clone the repository.

Open the project directory in Visual Studio Code.

Create and activate the Python virtual environment.

Install the required Python packages.

Start the FastAPI backend.

Run the frontend using a local development server.

Open the application in a web browser.

## Backend Setup

Open PowerShell in the project directory.

Activate the virtual environment.

Run the following command.

uvicorn backend.main:app --reload

The backend will be available at

http://127.0.0.1:8000

Swagger documentation will be available at

http://127.0.0.1:8000/docs

## Security Notes

Personal images used during testing should not be uploaded to GitHub.

The virtual environment should not be committed to the repository.

Sensitive credentials and private configuration values should not be committed.

Production deployment should use appropriate CORS restrictions and additional API security controls.

## Project Result

PlantCare AI provides an end to end plant disease detection workflow using deep learning, image validation, REST API integration, authentication, and a user friendly web interface.

The current system successfully validates uploaded images, predicts supported plant conditions, provides basic treatment and prevention information, and maintains user specific prediction history.
