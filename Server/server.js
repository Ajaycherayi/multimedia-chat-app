const express = require('express');
const http = require('http')
const socketio = require('socket.io')
const { addUser, removeUser, getUser,
    getUsersInRoom } = require("./utils/manage_user");

const Db = require("./utils/connections")

Db.connectDb()
const app = express();

const server = http.createServer(app)


const io = socketio(server)
const PORT = 3000 || process.env.PORT


const roomChatData = {
'111111': [
    {'id': '1', 'msg' : 'Hai' , 'time' : '1:20 pm', 'user' : 'admin'},
    {'id': '2', 'msg' : 'Haghi' , 'time' : '1:25 pm', 'user' : 'ajay'},
    {'id': '3', 'msg' : 'Hafghi' , 'time' : '1:20 pm', 'user' : 'rahul'},
    {'id': '5', 'msg' : 'Hhgjai' , 'time' : '1:50 pm', 'user' : 'amjad'}
],
    
'22222': [
    {'id': '6', 'msg' : 'Haji' , 'time' : '1:20 pm', 'user' : 'admin'},
    {'id': '6', 'msg' : 'Hafhgi' , 'time' : '1:50 pm', 'user' : 'ajay'}

],
'333333': [
    {'id': '6', 'msg' : 'Hayi' , 'time' : '1:20 pm', 'user' : 'admin'},
    {'id': '6', 'msg' : 'Htai' , 'time' : '1:50 pm', 'user' : 'amjadj'}
],
'55555': [
    {'id': '6', 'msg' : 'Haie' , 'time' : '1:20 pm', 'user' : 'admin'},
    {'id': '6', 'msg' : 'Hair' , 'time' : '1:50 pm', 'user' : 'ajay'}
],
'65488': [],
'98765': []
}

// const activeUsers = {}; 

io.on('connection', socket => {
    
    console.log(`New WebSocket connected... `);

    // authenticate user
    socket.on("authUser",data =>{
        
        let chatUser = data["user"]
        // console.log(chatUser)



        if (!chatUser || chatUser == undefined || chatUser == ""){
            return false
        }

        // if (!activeUsers[user]) {
        //     activeUsers[user] = [];
        // }
        
        // Store the socket in the user's sessions
        // activeUsers[user].push(socket);

        // console.log(activeUsers)
        
        // get user Room details
        socket.on("getallRooms",() => {
            returnData = getAllUserRooms(data)
            socket.emit("getallRooms",returnData);
        })
        

        socket.on("joinRoom",({ user, room }, callback)=>{
            var leaveRoom = removeUser(socket.id);
            if (leaveRoom && leaveRoom.room !== undefined){
                socket.leave(leaveRoom.room);
            }
            const { error, usere } = addUser({ id: socket.id, name:user, room:room });
            if (error) return callback(error);
            
            // let roomId = data['room']
            let roomId = usere.room
            let roomData  = roomChatData[roomId]

            socket.join(roomId)
            console.log("New Join | ",user,room)
            console.log('Joind Room',socket.rooms);

            // Notify other sessions of the same user about the room joining
            // activeUsers[user].forEach((userSocket) => {
            //     if (userSocket !== socket) {
            //     //   userSocket.emit('joinedRoom', room);
            //     userSocket.emit("joinRoom",roomData);
            // }else{
            //     socket.emit("joinRoom",roomData);
                    
            //     }
            // });
            socket.emit("joinRoom",roomData);
            callback();
        });

        socket.on("chatMsg",({ message }) =>{

            const user = getUser(socket.id);

            
            const room = user.room
            const name = user.name
            // Send the message to the connected user
            // socket.emit('notification', ({message, room, name}));
            socket.to(user.room).emit('notification', ({message, room, name}));
            

            // let roomId = data['room']
            // let user = data['user']
            // let msg = data['msg']

            // let roomData  = [{'id': '6', 'msg' : message , 'time' : '1:50 pm', 'user' : user.name}]

            // activeUsers[user].forEach((userSocket) => {
            //     userSocket.to(roomId).emit('chatMsg', [{'id': '6', 'msg' : message , 'time' : '1:50 pm', 'user' : user.name}]);
            // });
            io.to(user.room).emit("chatMsg",[{'id': '6', 'msg' : message , 'time' : '1:50 pm', 'user' : user.name}]);

        });

        socket.on('disconnect', () => {
            // Remove the socket from the user's sessions
            // activeUsers[user] = activeUsers[user].filter((userSocket) => userSocket !== socket);
            
            console.log('Socket Disconnected...');
            const user = removeUser(socket.id);
            if (user) {
                io.to(user.room).emit("chatMsg",[{'id': '6', 'msg' :  `${user.name} had left` , 'time' : '1:50 pm', 'user' : 'admin' }])
            }
        });


    });
});

server.listen(PORT,() => {
console.log(`Server running on port ${PORT}`);
})


function getAllUserRooms(params) {
    const user = params["user"]
    console.log(user);
    room_data = {}
    room_data['ajay'] = ['111111','22222','333333','55555','65488','98765']
    room_data['rahul'] = ['111111']
    room_data['amjad'] = ['111111','333333']
    room_data['admin'] = ['111111','22222','333333','55555']

    rooms = ['111111','22222','333333']
    
    if (user != undefined && room_data[user] != undefined) {
        rooms = room_data[user]
    }

    return rooms
}

