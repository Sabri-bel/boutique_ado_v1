
//1. get the stripe public key (slice the quotation marks not needed)
var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);

// 2. get the client secret (slice the quotation marks not needed)
var client_secret = $('#id_client_secret').text().slice(1, -1);

//3. use the stripe js included in the base template 
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();

var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', {style:style});

//4. mount the card element to the given div 
card.mount('#card-element');