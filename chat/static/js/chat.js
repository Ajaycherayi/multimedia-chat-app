
const socket = io.connect('http://localhost:3000', {
    transports: ['websocket']
});

socket.on("getallRooms", data => {
    console.log(data);
    outputRoomNames(data);

});

function outputRoomNames(room) {
    roomListSect = $('.chat-list')
    for (i = 0; i < room.length; i++) {
        html = ''
        html += '<li class="clearfix" id="' + room[i] + '">'
        html += '<img src="{% static "img/users/user-4.png" %}" alt="avatar">'
        html += '<div class="about">'
        html += '<div class="name">' + room[i] + '</div>'
        html += '<div class="status">'
        html += '<i class="material-icons offline">fiber_manual_record</i>'
        html += 'left 7 mins ago </div>'
        html += '</div>'
        html += '</li>'
        roomListSect.append(html)
    }
}

$('.chat-list').on('click', 'li', function () {
    $('.chat-list li.active').removeClass('active');
    $(this).addClass('active');
    const room = $(this).attr("id");
    // data = {}
    // data['room'] = roomId
    // socket.emit("joinRoom", data,);
    console.log("user",user,room);
    socket.emit('joinRoom', { user, room }, (error) => {
        if (error) {
            alert(error);
        }
    })
});

socket.on("joinRoom", data => {
    console.log(data);
    outputChats(data)
});

function outputChats(chats) {
    roomChat = $('.chat-content')
    if (chats.length > 1){
        roomChat.empty();
    }
    for (i = 0; i < chats.length; i++) {
        html = ''
        html += '<div class="chat-item chat-left" style = "" > '
        html += '<img src="static/img/users/user-5.png">'
        html += '<div class="chat-details">'
        html += '<div class="chat-user">'+chats[i].user+'</div>'
        html += '<div class="chat-text">'+chats[i].msg+'</div>'
        html += '<div class="chat-time">'+chats[i].time+'</div>'
        html += '</div>'
        roomChat.append(html)
    }
    const chatMessages = document.querySelector('.chat-content');
        chatMessages.scrollTop = chatMessages.scrollHeight
    
}

$('.chat-bnt').on('click', function (){

    if ($('.msg-input').val().trim().length > 0) {
        // var me = user;
        // const roomId = $('.chat-list li.active').attr("id");
        const message = $('.msg-input').val()
        $('.msg-input').val('')
      
        // data = {}
        // data['room'] = roomId
        // data['user'] = me
        // data['msg'] = msg
        socket.emit("chatMsg", {message});

        
        
    }
    
    
});

socket.on("chatMsg", data => {
    console.log(data);
    outputChats(data);

});