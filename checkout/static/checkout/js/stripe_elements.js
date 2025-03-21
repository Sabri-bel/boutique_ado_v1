
//1. get the stripe public key (slice the quotation marks not needed)
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);

// 2. get the client secret (slice the quotation marks not needed)
var clientSecret = $('#id_client_secret').text().slice(1, -1);

//3. use the stripe js included in the base template 
var stripe = Stripe(stripePublicKey);
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


// handle real time validation errors on the card elements using the
//eventlistener event on change card

card.addEventListener('change', function(event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
        <span class="icon" role="alert">
            <i class="fas fa-times"></i>
        </span>
        <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = ''
    }
});


// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    // 1. prevent default action (POST) and execute a different code
    ev.preventDefault();

    // disable submit button and card element to prevent multiple submission during checkout
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // 2. send the info securely on stripe
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            // stuff the form data into payment intent
            billing_details: {
                // trim method will remove the whitespace
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                email: $.trim(form.email.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    state: $.trim(form.county.value),
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            }
        },
    }).then(function(result) {
        if (result.error) {
            // add the error message in the appropriate div
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);

            // re-enable the card and submit button for a correction
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);

        } else {
            // if successfull, submit the form
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});