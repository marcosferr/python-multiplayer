import socketio
import customtkinter as tk
import pygame


tk.set_appearance_mode("light")

#Initialize socketio

sio = socketio.Client()
#Initialize pygame
pygame.init()

#Definir variable de jugadores
enemies = {}


#Definir nuestro jugador
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.image = pygame.image.load("tanque.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rotated_image = [pygame.transform.rotate(self.image, 0), pygame.transform.rotate(self.image, 90), pygame.transform.rotate(self.image, 180), pygame.transform.rotate(self.image, 270)]
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def move(self, direction):
        if direction == "up":
            self.y -= 10
            self.image = self.rotated_image[0]
        elif direction == "down":
            self.y +=10
            self.image = self.rotated_image[2]
        elif direction == "left":
            self.x -= 10
            self.image = self.rotated_image[1]
        elif direction == "right":
            self.x += 10
            self.image = self.rotated_image[3]
#Definir nuestro enemigo
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.image = pygame.image.load("tanque.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rotated_image = [pygame.transform.rotate(self.image, 0), pygame.transform.rotate(self.image, 90), pygame.transform.rotate(self.image, 180), pygame.transform.rotate(self.image, 270)]
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def move(self,direction, x,y):
        self.x = x
        self.y = y
        if direction == "up":
            
            self.image = self.rotated_image[0]
        elif direction == "down":
        
            self.image = self.rotated_image[2]
        elif direction == "left":

            self.image = self.rotated_image[1]
        elif direction == "right":

            self.image = self.rotated_image[3]

#Definir los eventos de socketio
@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on("join")
def join(data):
    print(f"{data['username']} joined the game")
    enemies[data["username"]] = Enemy(100, 100)

@sio.on("move")
def move(data):
    if data["username"] not in enemies:
        enemies[data["username"]] = Enemy(100, 100)
    username = data["username"]
    direction = data["direction"]
    enemies[username].move(direction, data['x'], data['y'])


#Definir lo necesario para el juego
def handle_events(jugador):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sio.disconnect()
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sio.emit("move", {"x" : jugador.x, "y":jugador.y, "direction" : 'up'} )
                jugador.move("up")
            elif event.key == pygame.K_DOWN:
                sio.emit("move", {"x" : jugador.x, "y":jugador.y, "direction" : 'down'} )
                jugador.move("down")
            elif event.key == pygame.K_LEFT:
                sio.emit("move", {"x" : jugador.x, "y":jugador.y, "direction" : 'left'})
                jugador.move("left")
            elif event.key == pygame.K_RIGHT:
                sio.emit("move", {"x" : jugador.x, "y":jugador.y, "direction" : 'right'})
                jugador.move("right")

#Definir el game loop
def game_loop(screen):
    jugador = Player(100, 100)
    while True:
        handle_events(jugador)
        
        #Dibujar el fondo
        screen.fill((0, 128, 0))
        jugador.draw(screen)
        for enemy in enemies.values():
            enemy.draw(screen)
        pygame.display.flip()


#Definir la funcion de login
def iniciar_juego():
    screen = pygame.display.set_mode((500, 500))
    jugadorNombre = jugador_entry.get()
    sio.connect("http://localhost:3000")
    sio.emit("join", jugadorNombre)
    root.withdraw()
    game_loop(screen)


root = tk.CTk()
root.title("Login juego")
root.geometry("500x500")

jugador_label = tk.CTkLabel(root, text="Jugador")
jugador_label.pack()

jugador_entry = tk.CTkEntry(root)
jugador_entry.pack()

login_button = tk.CTkButton(root, text="Login", command=iniciar_juego)
login_button.pack()

root.mainloop()