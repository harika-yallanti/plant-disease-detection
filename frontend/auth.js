import { auth } from "./firebase.js";

import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut
} from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";


/* =========================
   Elements
========================= */

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

const loginEmail = document.getElementById("loginEmail");
const loginPassword = document.getElementById("loginPassword");

const registerEmail = document.getElementById("registerEmail");
const registerPassword = document.getElementById("registerPassword");

const loginButton = document.getElementById("loginButton");
const registerButton = document.getElementById("registerButton");

const loginError = document.getElementById("loginError");
const registerError = document.getElementById("registerError");

const showRegister = document.getElementById("showRegister");
const showLogin = document.getElementById("showLogin");


/* =========================
   Show Register Form
========================= */

showRegister.addEventListener("click", function () {

    loginForm.classList.add("hidden");

    registerForm.classList.remove("hidden");

    loginError.textContent = "";
});


/* =========================
   Show Login Form
========================= */

showLogin.addEventListener("click", function () {

    registerForm.classList.add("hidden");

    loginForm.classList.remove("hidden");

    registerError.textContent = "";
});


/* =========================
   Register
========================= */

registerButton.addEventListener("click", async function () {

    const email = registerEmail.value.trim();

    const password = registerPassword.value;


    if (!email || !password) {

        registerError.textContent =
            "Please enter your email and password.";

        return;
    }


    if (password.length < 6) {

        registerError.textContent =
            "Password must contain at least 6 characters.";

        return;
    }


    registerButton.disabled = true;

    registerError.textContent = "";


    try {

        const userCredential =
    await createUserWithEmailAndPassword(
        auth,
        email,
        password
    );


// Firebase automatically signs the new user in.
// Sign them out so they must explicitly login.
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

        console.error(error);

        registerError.textContent =
            getFirebaseErrorMessage(error.code);

    }

    finally {

        registerButton.disabled = false;

    }

});


/* =========================
   Login
========================= */

loginButton.addEventListener("click", async function () {

    const email = loginEmail.value.trim();

    const password = loginPassword.value;


    if (!email || !password) {

        loginError.textContent =
            "Please enter your email and password.";

        return;
    }


    loginButton.disabled = true;

    loginError.textContent = "";


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

        console.error(error);

        loginError.textContent =
            getFirebaseErrorMessage(error.code);

    }

    finally {

        loginButton.disabled = false;

    }

});


/* =========================
   Firebase Error Messages
========================= */

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