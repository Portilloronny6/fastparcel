import {app, getAuth, RecaptchaVerifier, signInWithPhoneNumber} from "./firebase.js";

const auth = getAuth(app);
window.recaptchaVerifier = new RecaptchaVerifier('recaptcha-container', {}, auth);

const getCode = document.querySelector('#get-code');
const verifyCode = document.querySelector('#verify-code');

getCode.querySelector('button').addEventListener('click', () => {
    const phoneNumber = getCode.querySelector('input').value;
    const appVerifier = window.recaptchaVerifier;
    signInWithPhoneNumber(auth, phoneNumber, appVerifier)
        .then((confirmationResult) => {
            // SMS sent. Prompt user to type the code from the message, then sign the
            // user in with confirmationResult.confirm(code).
            console.log(confirmationResult);
            window.confirmationResult = confirmationResult;

            getCode.classList.add('d-none');
            verifyCode.classList.remove('d-none');
        }).catch((error) => {
        Swal.fire({
            position: 'top-end',
            icon: 'error',
            title: error.message,
            showConfirmButton: false,
            timer: 3500
        })
    });

    getCode.classList.add('d-none');
    verifyCode.classList.remove('d-none');
})

verifyCode.querySelector('button').addEventListener('click', () => {
    const code = verifyCode.querySelector('input').value;

    confirmationResult.confirm(code).then((result) => {
        // User signed in successfully.
        const user = result.user;
        console.log(user.phoneNumber);

        user.getIdToken().then((idToken) => {
            console.log(idToken);
        });
    }).catch((error) => {
        // User couldn't sign in (bad verification code?)
        Swal.fire({
            position: 'top-end',
            icon: 'error',
            title: error.message,
            showConfirmButton: false,
            timer: 3500,
        })
    });

})