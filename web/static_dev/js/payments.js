var form = document.querySelector('#payment-form');
var submit = document.querySelector('input[type="submit"]');

braintree.client.create({
    authorization: '{{ client_token }}'
}, function(clientErr, clientInstance) {
    if (clientErr) {
        console.error(clientErr);
        return;
    }

    braintree.hostedFields.create({
        client: clientInstance,
        styles: {
            'input': {
                'font-size': '14px',

            },
            'input.invalid': {
                'color': 'red'
            },
            'input.valid': {
                'color': 'green'
            }
        },
        fields: {
            number: {
                selector: '#card-number',
                placeholder: '4111 1111 1111 1111',
                class: 'auth-form__input',
                border: '1px solid black'
            },
            cvv: {
                selector: '#cvv',
                placeholder: '123'
            },
            expirationDate: {
                selector: '#expiration-date',
                placeholder: '10/2022'
            }
        }
    }, function(hostedFieldsErr, hostedFieldsInstance) {
        if (hostedFieldsErr) {
            console.error(hostedFieldsErr);
            return;
        }

        submit.removeAttribute('disabled');

        form.addEventListener('submit', function(event) {
            event.preventDefault();

            hostedFieldsInstance.tokenize(function(tokenizeErr, payload) {
                if (tokenizeErr) {
                    console.error(tokenizeErr);
                    return;
                }

                // If this was a real integration, this is where you would
                // send the nonce to your server.
                console.log('Got a nonce: ' + payload.nonce);
            });
        }, false);
    });
});