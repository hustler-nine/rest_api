const text_box = '<div class="card-panel right" style="width: 75%; position: relative">' +
    '<div style="position: absolute; top: 0; left:3px; font-weight: bolder" class="title">{sender}</div>' +
    '{message}' +
    '</div>';

let userState = ''




function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}



function send(sender, receiver, message) {
    $.ajax({
    type: 'POST',
    headers: {
      'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val(),

    },
    data: '{"sender": "' + sender + '", "receiver": "' + receiver + '","message": "' + message + '" }',
    url: "/api/v1/chat/messages/",
    dataType: "json",
    contentType: "application/json",
    success: function (data) {
                console.log(data);
                var box = text_box.replace('{sender}', "You");
                box = box.replace('{message}', message);
                $('#board').append(box);
                scrolltoend();
                }
    })
}


function receive() {
    $.get('/api/v1/chat/messages/' + sender_id + '/' + receiver_id + '/', function (data) {
        console.log(data);
        if (data.length !== 0) {
            for (var i = 0; i < data.length; i++) {
                console.log(data[i]);
                var box = text_box.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('right', 'left blue lighten-5');
                $('#board').append(box);
                scrolltoend();
            }
        }
    })
}

function getUsers(senderId, callback) {
    return $.get('/api/v1/chat/chat/', function (data) {
        if (userState !== JSON.stringify(data)) {
            userState = JSON.stringify(data);
            const doc = data.reduce((res, user) => {
                if (user.id === senderId) {
                    return res
                } else {
                    return [userDiv(senderId, user.id, user.username, user.online), ...res]
                }
            }, [])
            callback(doc)
        }
    })
}

function register(username, password) {
    $.post('/api/v1/chat/users/', '{"username": "' + username + '", "password": "' + password + '"}',
        function (data) {
            console.log(data);
            window.location = '/';
        }).fail(function (response) {
            $('#id_username').addClass('invalid');
        })
}







