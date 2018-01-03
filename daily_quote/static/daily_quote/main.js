var state = {
    'quote_id': null,
};

document.addEventListener('DOMContentLoaded', function () {
    get_csrf_token();
    recommend_quote();
    console.log("DOM Content Loaded");
    var like_button = document.getElementById('like');
    var dislike_button = document.getElementById('dislike');
    like_button.addEventListener('click', like_quote);
    dislike_button.addEventListener('click', dislike_quote);
});

function recommend_quote() {
    var request = new XMLHttpRequest();

    request.open('GET', 'http://localhost:8000/daily_quote/api/recommend');

    request.onload = function () {
        var data = JSON.parse(request.responseText);
        var quote_string = document.getElementById('quote_string');
        var author = document.getElementById('author');
        state.quote_id = data.id;
        quote_string.innerHTML = data.text;
        author.innerHTML += data.author.name;
        console.log(data);
    };

    request.send();
}

function rank_quote(rank) {
    var request = new XMLHttpRequest();
    var data = JSON.stringify({
        'quote_id': state.quote_id,
        'rank': rank
    });

    request.open('PUT', 'http://localhost:8000/daily_quote/api/quoterank/');

    request.setRequestHeader("Content-type", 'application/json');
    request.setRequestHeader('X-CSRFToken', get_csrf_token());

    request.send(data);
}

function like_quote() {
    rank_quote(1)
}

function dislike_quote() {
    rank_quote(-1)
}

function get_csrf_token() {
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
