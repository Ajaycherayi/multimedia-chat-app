/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 * 
 */

"use strict";

var roomId = $(this).data('room-id');
    $.ajax({
        url: `/room/${roomId}/`,  // New URL pattern for room chat
        success: function(data) {
            // Update chat-messages div with the fetched messages
            $('#chat-messages').html(data);
        }
    });

