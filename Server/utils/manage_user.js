const users = [];

const addUser = ({ id, name, room }) => {
    name = name.trim().toLowerCase();
	room = room.trim().toLowerCase();
    
	const existingUser = users.find((user) => {
        user.room === room && user.name === name
	});
    
	if (existingUser) {
        return { error: "Username is taken" };
	}
	const usere = { id, name, room };
    
	users.push(usere);
    console.log("total Users ",users);
	return { usere };

}

const removeUser = (id) => {
    console.log('SocketId | ',id)
    
    for (let i = 0; i < users.length; i++) {
        if (users[i].id === id) {
          console.log('index | ',i)
          const user = users[i]
          users.splice(i, 1)
          return user;
        }
      }

    console.log('Remaining Users | ',users)
}

const getUser = (id) => users
	.find((user) => user.id.toString() === id.toString());

const getUsersInRoom = (room) => users
	.filter((user) => user.room === room);

module.exports = {
	addUser, removeUser,
	getUser, getUsersInRoom
};
