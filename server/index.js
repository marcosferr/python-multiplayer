const express = require("express");
const http = require("http");
const socketIO = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

// Define a route for the homepage
app.get("/", (req, res) => {
  res.send("Welcome to the multiplayer game!");
});

// Define a Socket.IO connection handler
io.on("connection", (socket) => {
  console.log("A user connected");

  // Handle the 'join' event
  socket.on("join", (username) => {
    console.log(`${username} joined the game`);
    socket.username = username;
    socket.broadcast.emit("join", { username });
  });

  // Handle the 'move' event
  socket.on("move", (data) => {
    console.log(`${socket.username} moved ${data.direction}`);
    console.log(`x: ${data.x}, y: ${data.y}`);
    socket.broadcast.emit("move", {
      username: socket.username,
      direction: data.direction,
      x: data.x,
      y: data.y,
    });
  });

  // Handle the 'disconnect' event
  socket.on("disconnect", () => {
    console.log(`${socket.username} left the game`);
  });
});

// Start the server
const port = process.env.PORT || 3000;
server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
