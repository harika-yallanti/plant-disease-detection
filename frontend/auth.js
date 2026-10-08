import { auth } from "./firebase.js";

import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    signInWithPopup,
    GoogleAuthProvider,
    sendPasswordResetEmail
} from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";


//    Google Authentication


const googleProvider = new GoogleAuthProvider();



//    Forms


const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

const loginFormElement = document.getElementById("loginFormElement");
const registerFormElement = document.getElementById("registerFormElement");



//    Login Elements


const loginEmail = document.getElementById("loginEmail");
const loginPassword = document.getElementById("loginPassword");



//    Register Elements


const registerEmail = document.getElementById("registerEmail");
const registerPassword = document.getElementById("registerPassword");



//    Navigation Buttons


const showRegisterButton =
    document.getElementById("showRegisterButton");

const showLoginButton =
    document.getElementById("showLoginButton");



//    Show Register Form


showRegisterButton.addEventListener("click", function () {

    loginForm.classList.add("hidden");

    registerForm.classList.remove("hidden");

});



//    Show Login Form


showLoginButton.addEventListener("click", function () {

    registerForm.classList.add("hidden");

    loginForm.classList.remove("hidden");

});



//    Register


registerFormElement.addEventListener("submit", async function (event) {

    event.preventDefault();

    const email = registerEmail.value.trim();

    const password = registerPassword.value;


    if (!email || !password) {

        alert("Please enter your email and password.");

        return;

    }


    if (password.length < 6) {

        alert("Password must contain at least 6 characters.");

        return;

    }


    try {

        await createUserWithEmailAndPassword(
            auth,
            email,
            password
        );


        

        await signOut(auth);


        alert(
            "Account created successfully! Please login with your email and password."
        );


        registerForm.classList.add("hidden");

        loginForm.classList.remove("hidden");


        registerEmail.value = "";

        registerPassword.value = "";

    }

    catch (error) {

        console.error("Registration error:", error);

        alert(getFirebaseErrorMessage(error.code));

    }

});



//    Login


loginFormElement.addEventListener("submit", async function (event) {

    event.preventDefault();

    const email = loginEmail.value.trim();

    const password = loginPassword.value;


    if (!email || !password) {

        alert("Please enter your email and password.");

        return;

    }


    try {

        await signInWithEmailAndPassword(
            auth,
            email,
            password
        );


        alert("Login successful!");

        window.location.href = "index.html";

    }

    catch (error) {

        console.error("Login error:", error);

        alert(getFirebaseErrorMessage(error.code));

    }

});



//    Firebase Error Messages

function getFirebaseErrorMessage(errorCode) {

    switch (errorCode) {

        case "auth/email-already-in-use":

            return "An account with this email already exists.";


        case "auth/invalid-email":

            return "Please enter a valid email address.";


        case "auth/weak-password":

            return "Password must contain at least 6 characters.";


        case "auth/invalid-credential":

            return "Invalid email or password.";


        case "auth/user-not-found":

            return "No account found with this email.";


        case "auth/wrong-password":

            return "Incorrect password.";


        case "auth/too-many-requests":

            return "Too many attempts. Please try again later.";


        default:

            return "Authentication failed. Please try again.";

    }

}


//    Google Login


const googleLoginButton =
    document.getElementById("googleLoginButton");

const googleRegisterButton =
    document.getElementById("googleRegisterButton");


async function loginWithGoogle() {

    try {

        await signInWithPopup(
            auth,
            googleProvider
        );

        alert("Google login successful!");

        window.location.href = "index.html";

    }

    catch (error) {

        console.error("Google login error:", error);

        if (error.code === "auth/popup-closed-by-user") {

            return;

        }

        alert(getFirebaseErrorMessage(error.code));

    }

}


googleLoginButton.addEventListener(
    "click",
    loginWithGoogle
);


googleRegisterButton.addEventListener(
    "click",
    loginWithGoogle
);


//    Forgot Password


const forgotPasswordButton =
    document.getElementById("forgotPasswordButton");


forgotPasswordButton.addEventListener("click", async function () {

    const email = loginEmail.value.trim();


    if (!email) {

        alert("Please enter your email address first.");

        loginEmail.focus();

        return;

    }


    try {

        await sendPasswordResetEmail(
            auth,
            email
        );


        alert(
            "Password reset email sent successfully. Please check your inbox."
        );


    }

    catch (error) {

        console.error("Password reset error:", error);

        alert(getFirebaseErrorMessage(error.code));

    }

});