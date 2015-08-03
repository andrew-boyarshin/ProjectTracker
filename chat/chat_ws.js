var wsb, wsr;
var send, log, in_area;

function send_msg(msg) {
    msg = 'msg:'+msg;
    wsr.send(msg);
    in_area.value = '';
}
function initialize_socket(pr_id, cur_author) {
    wsb = new WebSocket("ws://localhost:1554/chat_broadcaster");
    wsr = new WebSocket("ws://localhost:1555/chat_receiver");
    send = document.getElementById('chat-send-button');
    log = document.getElementById('chat-container');
    in_area = document.getElementById('chat-input');
    send.onclick = function() {
        send_msg(in_area.value);
    }
    $(in_area).keypress(function(data) {
        if ((data.ctrlKey === true) && ((data.charCode === 10) || (data.charCode === 13))) {
            data.preventDefault();
            send_msg(in_area.value);
        }
    });

    wsb.onopen = function () {
        wsb.send(pr_id);
    }
    wsb.onmessage = function (event) {
        j = JSON.parse(event.data);
        log.innerHTML += '<div class="comment"><div>' + j.msg + '</div><div><b>'+j.author+'</b> написал(а) '+j.add_time+'</div></div>';
    }
    wsb.onerror = function (event) {
        console.log(event);
        log.innerHTML += '<p>' + event + '</p>';
    }
    wsr.onopen = function () {
        wsr.send(pr_id);
        wsr.send(cur_author);
    }
    wsr.onmessage = function (event) {
        log.innerHTML += '<p>' + event.data + '</p>';
    }
    wsr.onerror = function (event) {
        console.log(event);
        log.innerHTML += '<p>' + event + '</p>';
    }
    wsb.onclose = function (event) {
        console.log('Broadcaster closed');
    }
    wsr.onclose = function (event) {
        console.log('Receiver closed');
    }
}