const express = require('express');
const fs = require('fs');
const http = require('http')
const socketio = require('socket.io')
const Db = require("./utils/connections");
const { ok } = require('assert');

// Db.connectDb()
const app = express();

const server = http.createServer(app)


const io = socketio(server)
const PORT = 3000 || process.env.PORT


// const activeUsers = {}; 

io.on('connection', socket => {
    
    console.log(`New WebSocket connected... `,socket.id);
        
    socket.emit('connected')
        
    socket.on("setAllRooms",(roomList) => {
            
            console.log("Room List",roomList)
            for (index in roomList) {
                socket.join(roomList[index])
                
            }
        })
        
    socket.on("broadcastMessage",( data ) =>{

        let message = data['response']
        let room = data['room']

        io.to(room).emit('receiveMessage', message);
        socket.to(room).emit('chatRoomNotification', ({response:message, room:room}));
    });

    socket.on("connect_error", (err) => {
        console.log(`connect_error due to ${err.message}`);
    });

    socket.on('disconnect', (reason) => {
        
        console.log('Socket Disconnected...',reason);
    });

});

server.listen(PORT,() => {
    console.log(`Server running on port ${PORT}`);
})

