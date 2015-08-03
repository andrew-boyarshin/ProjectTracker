function ready(fn) {
    if (document.readyState != 'loading'){
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

last = '2000-01-01 00:00:00'
username = ""
admins = []
writers = []

function setusername(uname){
    username = uname;
}
pr_id = ""

function setpr_id(d){
    pr_id = d;
}

function strmax(a, b) {
    for (var i=0; i<a.length; i++) {
        var f = a.charAt(i);
        var s = b.charAt(i);
        if (f < s) {
            return b;
        } else if (f > s) {
            return a;
        }
    }
    return a;
}

function chat_update() {
    $.post('http://localhost:8080/chat_broadcaster/'+last, {pr_id: pr_id}, function(json) {
        json = JSON.parse(json);
        ul = document.getElementById('chat-container');
        if (json.length < 10)
            firstmsg=0;
        else
            firstmsg=json.length-10;

        for (var i=firstmsg; i<json.length; i++) {
            var msg = json[i];
            var li = document.createElement('div');
            

            var color = false;


            for (var j=0; j<admins.length; j++)
            {
                if (admins[j] === msg.author){
                    li.innerHTML = '<b><font color="red">' + msg.author + '</font></b> : ' + msg.msg;
                    color=true;
                }         
            }

            for (var j=0; j<writers.length; j++)
            {
                if (writers[j] === msg.author){
                    li.innerHTML = '<b><font color="green">' + msg.author + '</font></b> : ' + msg.msg;
                    color=true;
                }         
            }
            if (!color){
                li.innerHTML = '<b>' + msg.author + '</b> : ' + msg.msg;
            }


            ul.appendChild(li);

            last = strmax(last, msg.add_time);
        }
    });
}

function chat_schedule() {
    $.post('http://localhost:8080/chat_user_data', {pr_id: pr_id}, function(json) {
        json = JSON.parse(json);
        json.admins.forEach(function(item, i) {
            admins.push(item);
        });
        json.writers.forEach(function(item, i) {
            writers.push(item);
        });
        chat_update();
    });
    timer_id = setInterval(chat_update, 3000);
    var in_field = document.getElementById('chat-input')
    $(in_field).keypress(function (event) {
        if ((event.keyCode === 10) || (event.keyCode === 13)) {
            event.preventDefault();
            chat_send();
        }
    });
}

function chat_send() {
    var in_field = document.getElementById('chat-input')
    var msg = in_field.value;
    in_field.value = '';
    if (msg == "") {
        return;
    }
    var s = "";
    for (var i=0; i<msg.length; i++)
    {
        if (msg[i] == "<") {
            s+="&lt;"
        } else
        if (msg[i] == ">") {
            s+= "&gt;"
        } else
        if (msg[i] == "&") {
            s+= "&amp;"
        } else
        if (msg[i] == "'") {
            s+= "&apos;"
        } else
        if (msg[i] == '"') {
            s+= "&quot;"
        } else
        if (msg[i] == "`") {
            s+= ""
        } else
        s = s+ msg[i]       
    }

    $.post('http://localhost:8080/chat_receiver', {msg: s, author: username, pr_id: pr_id}, function(data) {
        chat_update();
    })
}

ready(chat_schedule)
