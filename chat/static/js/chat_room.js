


function clearRoomChat(room) {
    $('.chat').find('li').remove()
}






/** 
 ===================================================================
 Room Notification
 ===================================================================
 */

// Send Notification
socket.on('chatRoomNotification', ({response, room, uid}) => {

    if (response['room_chat'] != undefined && room != undefined){
        console.log('Notification | ',response['room_chat'])
        const messageData = response['room_chat']

        updateNotifications(room, messageData)
        sendRoomNotification(room, messageData)
    
    }
 });

// Rearrange Room List
function rearrangeRoomList(roomId) {
    const listItem = $("li[data-room='" + roomId + "']");
    if (listItem.length > 0) {
        listItem.prependTo('.chat-room-list');
    }
}

// Clear Room Notification Data
function clearNotifications(roomId) {
    const activeChatId = $('.item-room.active').attr('data-room')
    if (activeChatId === roomId){
        const countDiv = $('li[data-room="' + roomId + '"] .chat-alert')
        if (countDiv) {
            countDiv.text('');
        }
    }
}

// Update Room Notification Data
function updateNotifications(roomId, messageData) {
    if (messageData != undefined){
        const activeChatId = $('.item-room.active').attr('data-room')
        if (activeChatId !== roomId){
    
            const countDiv = $('li[data-room="' + roomId + '"] .chat-alert')
            const msgDiv = $('li[data-room="' + roomId + '"] .last-message')
            const timeDiv = $('li[data-room="' + roomId + '"] .time')
    
            if (countDiv) {
                let existCount = countDiv.text();
                let intCount = 0;
                if (existCount){
                    intCount = parseInt(existCount)
                }
                intCount = intCount + 1;
                countDiv.text(intCount > 0 ? intCount.toString() : '0');
            }
    
            for (key in messageData){
    
                if (msgDiv) {
                    msgDiv.text(messageData[key]['message']);
                }
        
                if (timeDiv) {
                    timeDiv.text(messageData[key]['time']);
                }
            }
            rearrangeRoomList(roomId)
        }
    }
}

function sendRoomNotification(room,messageData) {
    for (key in messageData){
        // Display a browser notification
        
        if (!("Notification" in window)) {

            debug("This browser does not support system notifications");
            alert("This browser does not support system notifications");

        }else if (Notification.permission === 'granted') {
            title = "Capital-Ax Room Chat"
            const notification = new Notification(title, { body:messageData[key]['message'] });

            notification.addEventListener('click', () => {
            window.open(window.location.href, '_blank');
        
            });
        }
    }
}



