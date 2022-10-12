import {messageAlert} from "./helpers.js";

const stripe = Stripe(context.stripeApiPublicKey);
const options = {
    clientSecret: context.clientSecret,
    // Fully customizable with appearance API.
    appearance: {
        theme: 'night',
        labels: 'floating'
    },
};

// Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in step 3
const elements = stripe.elements(options);

// Create and mount the Payment Element
const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');

const form = document.getElementById('payment-form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    messageAlert(
        'Agregando!', 'success',
        {
            'showConfirmButton': false,
            'timer': 1500,
            'position': 'top-end'
        })
    const {error} = await stripe.confirmSetup({
        //`Elements` instance that was used to create the Payment Element
        elements,
        confirmParams: {
            return_url: 'http://127.0.0.1:8000/customer/profile/payment-method/',
        }
    });
    if (error) {
        // This point will only be reached if there is an immediate error when
        // confirming the payment. Show error to your customer (for example, payment
        // details incomplete)
        const messageContainer = document.querySelector('#error-message');
        messageContainer.textContent = error.message;
    } else {
        // Your customer will be redirected to your `return_url`. For some payment
        // methods like iDEAL, your customer will be redirected to an intermediate
        // site first to authorize the payment, then redirected to the `return_url`.
    }
});