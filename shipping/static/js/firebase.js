// Import the functions you need from the SDKs you need
import {initializeApp} from "https://www.gstatic.com/firebasejs/9.11.0/firebase-app.js";
import {
    getAuth,
    RecaptchaVerifier,
    signInWithPhoneNumber
} from "https://www.gstatic.com/firebasejs/9.11.0/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBZnNGYq3o1UuzYBE4v0HcGU0ZhxplMG34",
    authDomain: "fastparcel-970e6.firebaseapp.com",
    projectId: "fastparcel-970e6",
    storageBucket: "fastparcel-970e6.appspot.com",
    messagingSenderId: "111615047450",
    appId: "1:111615047450:web:a59b2402a2f213d51bdea3"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export {app, getAuth, RecaptchaVerifier, signInWithPhoneNumber};