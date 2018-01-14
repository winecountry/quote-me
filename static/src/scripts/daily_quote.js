// global.$ = require("jquery");

// Document ready function
document.addEventListener('DOMContentLoaded', function () {
    var buttons = document.getElementById('buttons');

    if (buttons) {
        var like_button = buttons.children[0];
        var dislike_button = buttons.children[1];

        like_button.addEventListener('click', function () {
            rank_quote(1);
        });

        dislike_button.addEventListener('click', function () {
            rank_quote(-1);
        });
    }
});

var state = {
    'quote_id': null,
    'rank': 0
};

function recommend_quote() {
    /** GET QuoteRank
     * Populate the quote container with a recommended quote
     */

    // New AJAX request
    var request = new XMLHttpRequest();

    request.open('GET', 'http://localhost:8000/api/recommend');

    request.onload = function () {
        /* Update State */
        var data = JSON.parse(request.responseText);
        state.quote_id = data.quote.id;
        state.rank = data.rank;

        /* Update HTML */
        // quote not ranked
        if (state.rank !== 0) {
            disable_buttons()
        }
        // inject quote
        $('#quote_string').innerHTML = data.quote.text;
        $('#author').innerHTML += data.quote.author.name;
    };

    request.send();
}

// function rank_quote(rank) {
//     /** PUT QuoteRank
//      * Update (Profile, Quote) relationship with new rank (like or dislike)
//      */
//
//     $.ajax({
//         url: 'http://localhost:8000/api/quoterank/',
//         method: 'PUT',
//         credentials: 'include',
//         headers: {
//             "Content-type": "application/json",
//             "X-CSRFToken": csrf_token()
//         },
//         data: {
//             rank: rank
//         },
//         statusCode: {
//             400: function() {
//                 console.log("here")
//             }
//         },
//         success: function (data) {
//             /* Update state */
//             state.rank = data.rank;
//
//             /* Update HTML */
//             disable_buttons()
//         }
//     }).fail(function (err) {
//             console.log("hello");
//             console.log(err)
//         });
// }

function rank_quote(rank) {
    /** PUT QuoteRank
     * Update (Profile, Quote) relationship with new rank (like or dislike)
     */

    var request = new XMLHttpRequest();
    var payload = JSON.stringify({
        'rank': rank
    });

    // New AJAX request
    request.open('PUT', 'http://localhost:8000/api/quoterank/');

    /* Set Headers */
    // sending JSON data
    request.setRequestHeader("Content-type", 'application/json');
    // cross site request forgery
    request.setRequestHeader('X-CSRFToken', csrf_token());

    request.onload = function () {
        if (request.status === 200) {
            /* Update state */
            var data = JSON.parse(request.responseText);
            state.rank = data.rank;

            /* Update HTML */
            disable_buttons()
        }
    };

    request.send(payload);
}

function disable_buttons() {
    var like_button = document.getElementById('like');
    var dislike_button = document.getElementById('dislike');

    if (state.rank === 1) {
        like_button.classList.add('selected')
    } else if (state.rank === -1) {
        dislike_button.classList.add('selected')
    }

    [like_button, dislike_button].forEach(function (button) {
        button.disabled = true;
    });
}

function csrf_token() {
    // TODO: Look for a less error-prone implementation
    var token = null;
    var cookies = document.cookie.split(';');
    cookies.forEach(function (cookie) {
        if (cookie.trim().startsWith('csrftoken')) {
            var start = cookie.indexOf('=') + 1;
            token = cookie.substring(start);
        }
    });
    return token
}
