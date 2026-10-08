import {
    signOut,
    onAuthStateChanged,
    updateProfile
} from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";

import {
    auth
} from "./firebase.js";


//    Authentication Protection


onAuthStateChanged(auth, function (user) {

    if (!user) {

        window.location.href = "login.html";

        return;
    }


    displayUserProfile(user);

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



//    Initial State


resetButton.classList.add("hidden");



//    Image Selection


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



//    Prediction


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


        
        //    Leaf Validation
        

        if (!data.valid_leaf) {

            showError(
                data.message ||
                "Please upload a clear plant leaf image."
            );

            resultSection.classList.add("hidden");

            resetButton.classList.remove("hidden");

            return;
        }
        
        

        
        //    Display Prediction Result
        

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

        await savePredictionHistory(data);

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



//    Reset


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



//    Error


function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");

}


//    Logout


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


//    Dashboard Navigation


const navButtons = document.querySelectorAll(".nav-button");

const dashboardSections = document.querySelectorAll(
    ".dashboard-section"
);


navButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        const targetSection =
            button.getAttribute("data-section");


        
        //    Remove Active State
        

        navButtons.forEach(function (navButton) {

            navButton.classList.remove("active");

        });


       
        //    Hide All Sections
       

        dashboardSections.forEach(function (section) {

            section.classList.add("hidden");

            section.classList.remove("active-section");

        });


        
        //    Activate Selected Button
        

        button.classList.add("active");


        
        //    Show Selected Section
        

        const selectedSection =
            document.getElementById(targetSection);


        if (selectedSection) {

            selectedSection.classList.remove("hidden");

            selectedSection.classList.add("active-section");

        }


        /*
           Scroll to Top
        */

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    });

});


//    Prediction History


function getHistoryKey() {

    const user = auth.currentUser;

    if (!user) {
        return null;
    }

    return `plantCareHistory_${user.uid}`;
}



//    Get History


function getPredictionHistory() {

    const historyKey = getHistoryKey();

    if (!historyKey) {
        return [];
    }

    const history =
        localStorage.getItem(historyKey);

    if (!history) {
        return [];
    }

    try {

        return JSON.parse(history);

    } catch (error) {

        console.error(
            "Unable to read prediction history:",
            error
        );

        return [];

    }

}


//    Convert Image to Data URL


function convertImageToDataURL(file) {

    return new Promise(function (resolve, reject) {

        const reader = new FileReader();

        reader.onload = function () {

            resolve(reader.result);

        };

        reader.onerror = function () {

            reject(
                new Error("Unable to process the image.")
            );

        };

        reader.readAsDataURL(file);

    });

}

//    Save Prediction


async function savePredictionHistory(data) {

    const historyKey = getHistoryKey();

    if (!historyKey || !selectedImage) {
        return;
    }


    try {

        const imageData =
            await convertImageToDataURL(selectedImage);


        const now = new Date();


        const historyItem = {

            id: Date.now(),

            image: imageData,

            disease: data.disease,

            confidence: data.confidence,

            description: data.description,

            treatment: data.treatment,

            prevention: data.prevention,

            date: now.toLocaleDateString(),

            time: now.toLocaleTimeString()

        };


        const history =
            getPredictionHistory();


        history.unshift(historyItem);


        localStorage.setItem(
            historyKey,
            JSON.stringify(history)
        );


        displayPredictionHistory();

    }

    catch (error) {

        console.error(
            "Unable to save prediction history:",
            error
        );

    }

}



//    Display History


function displayPredictionHistory() {

    const historyContainer =
        document.getElementById("historyContainer");

    if (!historyContainer) {
        return;
    }

    const history =
        getPredictionHistory();

    if (history.length === 0) {

        historyContainer.innerHTML = `

            <div class="empty-history">

                <div class="empty-history-icon">
                    🌱
                </div>

                <h3>
                    No Prediction History
                </h3>

                <p>
                    Your analyzed plant images will
                    appear here after you make predictions.
                </p>

            </div>

        `;

        return;
    }

    historyContainer.innerHTML = "";

    history.forEach(function (item) {

        const historyCard =
            document.createElement("div");

        historyCard.className =
            "history-card";

        historyCard.innerHTML = `

            <div class="history-image-container">

                <img
                    src="${item.image}"
                    alt="Analyzed plant leaf"
                    class="history-image"
                >

            </div>


            <div class="history-details">

                <span class="history-label">
                    AI Prediction
                </span>

                <h3>
                    ${item.disease}
                </h3>

                <p>
                    <strong>Confidence:</strong>
                    ${item.confidence}%
                </p>

                <p>
                    <strong>Date:</strong>
                    ${item.date}
                </p>

                <p>
                    <strong>Time:</strong>
                    ${item.time}
                </p>


                <!-- History Actions -->

                <div class="history-actions">

                    <!-- Read More Button -->

                    <button
                        class="history-read-more"
                        data-history-id="${item.id}"
                    >
                        Read More
                    </button>


                    <!-- Delete Button -->

                    <button
                        class="history-delete-button"
                        data-history-id="${item.id}"
                    >
                        🗑️ Delete
                    </button>

                </div>


                <!-- Additional Details -->

                <div
                    id="history-details-${item.id}"
                    class="history-extra-details hidden"
                >

                    <div class="history-info">

                        <h4>
                            🌱 About the Condition
                        </h4>

                        <p>
                            ${item.description}
                        </p>

                    </div>


                    <div class="history-info">

                        <h4>
                            💊 Recommended Treatment
                        </h4>

                        <p>
                            ${item.treatment}
                        </p>

                    </div>


                    <div class="history-info">

                        <h4>
                            🛡️ Prevention
                        </h4>

                        <p>
                            ${item.prevention}
                        </p>

                    </div>

                </div>

            </div>

        `;

        historyContainer.appendChild(
            historyCard
        );

    });

}

//    Load History After Login


onAuthStateChanged(auth, function (user) {

    if (!user) {
        return;
    }

    displayPredictionHistory();

});

//    History Read More / Less + Delete


document.addEventListener("click", function (event) {

    

    const readMoreButton =
        event.target.closest(".history-read-more");

    if (readMoreButton) {

        const historyId =
            readMoreButton.getAttribute("data-history-id");

        const details =
            document.getElementById(
                `history-details-${historyId}`
            );

        if (!details) {
            return;
        }

        if (details.classList.contains("hidden")) {

            details.classList.remove("hidden");

            readMoreButton.textContent = "Read Less";

        } else {

            details.classList.add("hidden");

            readMoreButton.textContent = "Read More";
        }

        return;
    }


    
    //    Delete Individual History
    

    const deleteButton =
        event.target.closest(".history-delete-button");

    if (!deleteButton) {
        return;
    }

    const historyId =
        deleteButton.getAttribute("data-history-id");

    if (!historyId) {
        return;
    }

    const confirmed = confirm(
        "Are you sure you want to delete this prediction from your history?"
    );

    if (!confirmed) {
        return;
    }


    const historyKey = getHistoryKey();

    if (!historyKey) {
        alert("Please login first.");
        return;
    }


    const history =
        getPredictionHistory();


    const updatedHistory =
        history.filter(function (item) {
            return String(item.id) !== String(historyId);
        });


    localStorage.setItem(
        historyKey,
        JSON.stringify(updatedHistory)
    );


    displayPredictionHistory();


    alert("Prediction removed from history.");
});

//    Display User Profile


function displayUserProfile(user) {
    const profileAvatar = document.getElementById("profileAvatar");
    const profileName = document.getElementById("profileName");
    const profileEmail = document.getElementById("profileEmail");
    const profileDisplayName = document.getElementById("profileDisplayName");
    const profileProfileEmail = document.getElementById("profileProfileEmail");
    const profileUserId = document.getElementById("profileUserId");
    const profileAccountType = document.getElementById("profileAccountType");

    if (!user) return;

    const displayName = user.displayName || "";
    const email = user.email || "";

    let userName = displayName;

    if (!userName && email) {
        userName = email.split("@")[0];
    }

    if (!userName) {
        userName = "User";
    }

    const initial = userName.trim().charAt(0).toUpperCase();

    
    const profileImageKey = `profileImage_${user.uid}`;
    const savedProfileImage = localStorage.getItem(profileImageKey);

    if (savedProfileImage) {
        profileAvatar.innerHTML = "";

        const image = document.createElement("img");
        image.src = savedProfileImage;
        image.alt = "Profile picture";

        image.style.width = "100%";
        image.style.height = "100%";
        image.style.objectFit = "cover";
        image.style.borderRadius = "50%";

        profileAvatar.appendChild(image);
    } else {
        profileAvatar.textContent = initial;
    }

    profileName.textContent = userName;
    profileEmail.textContent = email || "Not available";

    profileDisplayName.textContent =
        displayName || "Not provided";

    profileProfileEmail.textContent =
        email || "Not available";

    profileUserId.textContent =
        user.uid || "Not available";

    if (user.providerData && user.providerData.length > 0) {
        const provider = user.providerData[0].providerId;

        if (provider === "google.com") {
            profileAccountType.textContent = "Google Account";
        } else {
            profileAccountType.textContent = "Email & Password";
        }
    } else {
        profileAccountType.textContent =
            "Firebase Authentication";
    }
}

const clearHistoryButton = document.getElementById("clearHistoryButton");

clearHistoryButton.addEventListener("click", function () {
    const historyKey = getHistoryKey();

    if (!historyKey) {
        alert("Please login to clear your history.");
        return;
    }

    const history = getPredictionHistory();

    if (history.length === 0) {
        alert("There is no prediction history to clear.");
        return;
    }

    const confirmed = confirm(
        "Are you sure you want to clear all your prediction history?"
    );

    if (!confirmed) {
        return;
    }

    localStorage.removeItem(historyKey);

    displayPredictionHistory();

    alert("Prediction history cleared successfully!");
});

const editProfileButton = document.getElementById("editProfileButton");
const editProfileForm = document.getElementById("editProfileForm");
const cancelEditProfileButton = document.getElementById("cancelEditProfileButton");

editProfileButton.addEventListener("click", function () {
    const user = auth.currentUser;

    if (!user) {
        alert("Please login first.");
        return;
    }

    document.getElementById("editProfileName").value = user.displayName || "";

    // Reset the image file input
    editProfileImage.value = "";

    // Clear old preview
    profilePreviewImage.src = "";
    profileImagePreview.classList.add("hidden");

    editProfileForm.classList.remove("hidden");
});

cancelEditProfileButton.addEventListener("click", function () {
    // Clear selected image
    editProfileImage.value = "";

    // Clear preview
    profilePreviewImage.src = "";
    profileImagePreview.classList.add("hidden");

    editProfileForm.classList.add("hidden");
});

const saveProfileButton =
    document.getElementById("saveProfileButton");


//    Profile Image Preview


const editProfileImage =
    document.getElementById("editProfileImage");

const profileImagePreview =
    document.getElementById("profileImagePreview");

const profilePreviewImage =
    document.getElementById("profilePreviewImage");


editProfileImage.addEventListener("change", function () {

    const selectedFile =
        editProfileImage.files[0];

    if (!selectedFile) {

        profileImagePreview.classList.add("hidden");

        profilePreviewImage.src = "";

        return;
    }


    /* Validate image type */

    if (!selectedFile.type.startsWith("image/")) {

        alert("Please select a valid image file.");

        editProfileImage.value = "";

        profileImagePreview.classList.add("hidden");

        return;
    }


    /* Validate image size */

    if (selectedFile.size > 2 * 1024 * 1024) {

        alert("Profile image must be smaller than 2 MB.");

        editProfileImage.value = "";

        profileImagePreview.classList.add("hidden");

        return;
    }


    const reader = new FileReader();


    reader.onload = function (event) {

        profilePreviewImage.src =
            event.target.result;

        profileImagePreview.classList.remove("hidden");
    };


    reader.onerror = function () {

        alert("Unable to preview the selected image.");

        profileImagePreview.classList.add("hidden");
    };


    reader.readAsDataURL(selectedFile);

});

saveProfileButton.addEventListener("click", async function () {

    const user = auth.currentUser;

    if (!user) {
        alert("Please login first.");
        return;
    }

    const nameInput =
        document.getElementById("editProfileName");

    const imageInput =
        document.getElementById("editProfileImage");

    const newName = nameInput.value.trim();

    if (!newName) {
        alert("Please enter your name.");
        nameInput.focus();
        return;
    }

    try {

        
        //    Update Firebase display name
        

        await updateProfile(user, {
            displayName: newName
        });


        
        //    Save profile image locally
        

        const selectedFile = imageInput.files[0];

        if (selectedFile) {

            if (!selectedFile.type.startsWith("image/")) {
                alert("Please select a valid image file.");
                return;
            }

            if (selectedFile.size > 2 * 1024 * 1024) {
                alert("Profile image must be smaller than 2 MB.");
                return;
            }

            const reader = new FileReader();

            reader.onload = function (event) {

                const profileImageKey =
                    `profileImage_${user.uid}`;

                localStorage.setItem(
                    profileImageKey,
                    event.target.result
                );

                displayUserProfile(user);

                editProfileForm.classList.add("hidden");

                imageInput.value = "";

                alert("Profile updated successfully!");
            };

            reader.onerror = function () {
                alert("Unable to read the selected image.");
            };

            reader.readAsDataURL(selectedFile);

        } else {

            /* No new image selected */

            displayUserProfile(user);

            editProfileForm.classList.add("hidden");

            alert("Profile updated successfully!");
        }

    } catch (error) {

        console.error(
            "Profile update error:",
            error
        );

        alert(
            "Unable to update your profile. Please try again."
        );
    }
});

const removeProfileImageButton =
    document.getElementById("removeProfileImageButton");

removeProfileImageButton.addEventListener("click", function () {

    const user = auth.currentUser;

    if (!user) {
        alert("Please login first.");
        return;
    }

    const profileImageKey =
        `profileImage_${user.uid}`;

    const savedImage =
        localStorage.getItem(profileImageKey);

    if (!savedImage) {
        alert("There is no profile image to remove.");
        return;
    }

    const confirmed = confirm(
        "Are you sure you want to remove your profile image?"
    );

    if (!confirmed) {
        return;
    }

    localStorage.removeItem(profileImageKey);

    displayUserProfile(user);

    document.getElementById("editProfileImage").value = "";

    alert("Profile image removed successfully!");
});