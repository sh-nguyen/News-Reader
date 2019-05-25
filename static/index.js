var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function () {
    socket.emit('next_article');
});

socket.on('article', function (data) {
    $('#article-img').attr('src', data.data['media_content']['0']['url'])
    $('#article-title').html(data.data['title'])
    $('#article-text').html(data.data['content']['0']['value'])
    $('#article-read').attr('href', data.data['link'])
    console.log(data.data);
});

$('#next-btn').click(function () {
    socket.emit('next_article');
});