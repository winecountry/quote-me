// Document ready function
document.addEventListener('DOMContentLoaded', function () {
    recommend_quote();  // GET Quote

    var like_button = document.getElementById('like');
    // PUT QuoteRank
    like_button.addEventListener('click', function () {
        rank_quote(1);
        this.style.backgroundColor = rgba(34, 139, 34, 0.6);
    });

    var dislike_button = document.getElementById('dislike');
    // PUT QuoteRank
    dislike_button.addEventListener('click', function () {
        rank_quote(-1);
        this.style.backgroundColor = rgba(204, 17, 17, 0.6);
        this.style.backgroundOpacity = 0.6;
    });
});

var state = {
    'quote_id': null
};

function recommend_quote() {
    /** GET Quote
     * Populate the quote container with a recommended quote
     */

    // New AJAX request
    var request = new XMLHttpRequest();

    request.open('GET', 'http://localhost:8000/daily_quote/api/recommend');

    request.onload = function () {
        var data = JSON.parse(request.responseText);
        var quote_string = document.getElementById('quote_string');
        var author = document.getElementById('author');
        state.quote_id = data.id;
        quote_string.innerHTML = data.text;
        author.innerHTML += data.author.name;
    };

    request.send();
}

function rank_quote(rank) {
    /** PUT QuoteRank
     * Update (Profile, Quote) relationship with new rank (like or dislike)
     */

    var request = new XMLHttpRequest();
    var data = JSON.stringify({
        'quote_id': state.quote_id,
        'rank': rank
    });

    request.open('PUT', 'http://localhost:8000/daily_quote/api/quoterank/');

    // sending JSON data
    request.setRequestHeader("Content-type", 'application/json');
    // add cross site request forgery protection
    request.setRequestHeader('X-CSRFToken', csrf_token());

    request.send(data);

    var buttons = document.querySelectorAll('.rank button');
    buttons.forEach(function (button) {
        button.disabled = true;
    });
}

function csrf_token() {
    // TODO: Look for a less error-prone solution
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

function rgba(r, g, b, a) {
    return "rgba(" + r.toString() + ", " + g.toString() + ", " + b.toString() + ", " + a.toString() + ")"
}
