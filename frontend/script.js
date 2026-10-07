import {
    signOut,
    onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";

import {
    auth
} from "./firebase.js";

/* =========================
   Authentication Protection
========================= */

onAuthStateChanged(auth, function (user) {

    if (!user) {

        window.location.href = "login.html";

    }

});

const API_URL = "http://127.0.0.1:8000";

const imageInput = document.getElementById("imageInput");
const fileText = document.getElementById("fileText");

const imagePreview = document.getElementById("imagePreview");
const previewContainer = document.getElementById("previewContainer");

const predictButton = document.getElementById("predictButton");

const loadingMessage = document.getElementById("loadingMessage");

const resultSection = document.getElementById("resultSection");

const diseaseName = document.getElementById("diseaseName");
const confidence = document.getElementById("confidence");

const description = document.getElementById("description");
const treatment = document.getElementById("treatment");
const prevention = document.getElementById("prevention");

const errorMessage = document.getElementById("errorMessage");

const resetButton = document.getElementById("resetButton");

let selectedImage = null;


/* =========================
   Initial State
========================= */

resetButton.classList.add("hidden");


/* =========================
   Image Selection
========================= */

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }


    if (!file.type.startsWith("image/")) {

        showError("Please select a valid image file.");

        return;
    }


    selectedImage = file;

    fileText.textContent = file.name;


    const imageURL = URL.createObjectURL(file);

    imagePreview.src = imageURL;

    previewContainer.classList.remove("hidden");

    resultSection.classList.add("hidden");

    errorMessage.classList.add("hidden");

    resetButton.classList.add("hidden");

    predictButton.disabled = false;

});


/* =========================
   Prediction
========================= */

predictButton.addEventListener("click", async function () {

    if (!selectedImage) {

        showError("Please select a leaf image first.");

        return;
    }


    const formData = new FormData();

    formData.append("file", selectedImage);


    predictButton.disabled = true;

    loadingMessage.classList.remove("hidden");

    resultSection.classList.add("hidden");

    errorMessage.classList.add("hidden");


    try {

        const response = await fetch(
            `${API_URL}/predict`,
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Prediction failed."
            );

        }


        /* =========================
           Leaf Validation
        ========================= */

        if (!data.valid_leaf) {

            showError(
                data.message ||
                "Please upload a clear plant leaf image."
            );

            resultSection.classList.add("hidden");

            resetButton.classList.remove("hidden");

            return;
        }


        /* =========================
           Display Prediction Result
        ========================= */

        diseaseName.textContent = data.disease;

        confidence.textContent =
            `${data.confidence}%`;

        description.textContent =
            data.description;

        treatment.textContent =
            data.treatment;

        prevention.textContent =
            data.prevention;


        resultSection.classList.remove("hidden");

        resetButton.classList.remove("hidden");


        resultSection.scrollIntoView({
            behavior: "smooth"
        });

    }


    catch (error) {

        console.error(error);

        showError(
            error.message ||
            "Unable to connect to the prediction server."
        );

    }


    finally {

        predictButton.disabled = false;

        loadingMessage.classList.add("hidden");

    }

});


/* =========================
   Reset
========================= */

resetButton.addEventListener("click", function () {

    selectedImage = null;

    imageInput.value = "";

    fileText.textContent =
        "Click to choose a leaf image";

    imagePreview.src = "";

    previewContainer.classList.add("hidden");

    resultSection.classList.add("hidden");

    errorMessage.classList.add("hidden");

    resetButton.classList.add("hidden");

    predictButton.disabled = true;

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

});


/* =========================
   Error
========================= */

function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");

}

/* =========================
   Logout
========================= */

const logoutButton = document.getElementById("logoutButton");

logoutButton.addEventListener("click", async function () {

    try {

        await signOut(auth);

        alert("Logged out successfully!");

        window.location.href = "login.html";

    }

    catch (error) {

        console.error(error);

        alert("Unable to logout. Please try again.");

    }

});