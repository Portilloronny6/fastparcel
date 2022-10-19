import {app, getAuth, RecaptchaVerifier, signInWithPhoneNumber} from "./firebase.js";
import {messageAlert} from "./helpers.js";

const auth = getAuth(app);
window.recaptchaVerifier = new RecaptchaVerifier('recaptcha-container', {
    'size': 'invisible',
}, auth);

const getCode = document.querySelector('#get-code');
const verifyCode = document.querySelector('#verify-code');
const changePhone = document.querySelector('#change-phone');

function onVerify(idToken) {
    const form = document.createElement('form');
    form.method = 'post';

    const inputId = document.createElement('input');
    inputId.name = 'id_token';
    inputId.value = idToken;
    form.appendChild(inputId);

    const inputCsrf = document.createElement('input');
    inputCsrf.name = 'csrfmiddlewaretoken';
    inputCsrf.value = document.querySelector('#verify-code input[name="csrfmiddlewaretoken"]').value;
    form.appendChild(inputCsrf);

    const inputCheck = document.createElement('input');
    inputCheck.name = 'phone_check';
    inputCheck.value = 'true';
    form.appendChild(inputCheck);

    document.body.appendChild(form);
    form.submit();
}

// Send the phone number to Firebase
getCode.querySelector('button').addEventListener('click', () => {
    const phoneNumber = getCode.querySelector('input').value;
    const appVerifier = window.recaptchaVerifier;

    if (!phoneNumber) {
        return messageAlert('Invalid phone number, try again', 'error');
    }

    signInWithPhoneNumber(auth, phoneNumber, appVerifier)
        .then((confirmationResult) => {
            // SMS sent. Prompt user to type the code from the message, then sign the
            // user in with confirmationResult.confirm(code).
            console.log(confirmationResult);
            window.confirmationResult = confirmationResult;

            getCode.classList.add('d-none');
            verifyCode.classList.remove('d-none');
        }).catch((error) => {
        return messageAlert(
            error.message, 'error',
            {
                'showConfirmButton': false,
                'timer': 3500,
                'position': 'top-end'
            })
    });

    getCode.classList.add('d-none');
    verifyCode.classList.remove('d-none');
})

// Verify the code sent to the user
verifyCode.querySelector('button').addEventListener('click', () => {
    const code = verifyCode.querySelector('input').value;

    confirmationResult.confirm(code).then((result) => {
        // User signed in successfully.
        const user = result.user;
        user.getIdToken().then((idToken) => {
            onVerify(idToken);
        });
    }).catch((error) => {
        // User couldn't sign in (bad verification code?)
        return messageAlert(
            error.message, 'error',
            {
                'showConfirmButton': false,
                'timer': 3500,
                'position': 'top-end'
            })
    });
})

// Change phone number

changePhone.querySelector('button').addEventListener('click', () => {
    changePhone.classList.add('d-none');
    getCode.classList.remove('d-none');
})