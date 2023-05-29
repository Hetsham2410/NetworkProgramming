"""
There are some lags due to send and receive a alot of values of changing position of the ball
Please lock on the fastest screen and move from both.
Press "w" button to move up and "s" to move down

"""
from turtle import Turtle, Screen
from socket import socket, AF_INET, SOCK_STREAM
import threading
from time import sleep


def receive_thread(client_socket):
    while True:
        message = client_socket.recv(500).decode('UTF-8')
        paddle_a.sety(int(message))


def PingPongGUI():
    # Score
    score_a = 0
    score_b = 0

    # Sleeping for 10 seconds
    sleep(3)
    # Main game loop
    while True:
        window.update()

        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Border checking
        if ball.ycor() > 140:
            ball.sety(140)
            ball.dy *= -1

        if ball.ycor() < -140:
            ball.sety(-140)
            ball.dy *= -1

        if ball.xcor() > 190:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            pen.clear()
            pen.write("Player A: {}\t\tPlayer B: {}".format(score_a, score_b),
                      align="center",
                      font=("algerian", 15, "normal"))

        if ball.xcor() < -190:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            pen.clear()
            pen.write("Player A: {}\t\tPlayer B: {}".format(score_a, score_b),
                      align="center",
                      font=("algerian", 15, "normal"))

        # Paddle and ball collisions
        if ball.xcor() > 140 \
                and ball.xcor() < 150 \
                and ball.ycor() < paddle_b.ycor() + 40 \
                and ball.ycor() > paddle_b.ycor() - 40:
            ball.setx(140)
            ball.dx *= -1.2

        if ball.xcor() < -140 \
                and ball.xcor() > -150 \
                and ball.ycor() < paddle_a.ycor() + 40 \
                and ball.ycor() > paddle_a.ycor() - 40:
            ball.setx(-140)
            ball.dx /= -1.2


def move_up():
    y_position = paddle_b.ycor()
    y_position += 20
    paddle_b.sety(y_position)
    client_socket.send(str(y_position).encode('UTF-8'))

def move_down():
    y_position = paddle_b.ycor()
    y_position -= 20
    paddle_b.sety(y_position)
    client_socket.send(str(y_position).encode('UTF-8'))

window = Screen()
window.title("Ping Pong: Client Side")
window.bgcolor("#005B5E")
window.setup(width=450, height=350)
window.tracer(0)


# Paddle A
paddle_a = Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("#A74F4F")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-150, 0)

# Paddle B
paddle_b = Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("#E7DF65")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(150, 0)

# Ball
ball = Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 1
ball.dy = -1

# Pen
pen = Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 150)
pen.write("Player A: 0\t\tPlayer B: 0", align="center", font=("algerian", 15, "normal"))
# Keyboard binding
window.listen()
window.onkeypress(move_up, "w")
window.onkeypress(move_down, "s")

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('127.0.0.1', 7002))

receive_thread = threading.Thread(target=receive_thread, args=(client_socket,))
receive_thread.start()

game_thread = threading.Thread(target=PingPongGUI)
game_thread.start()

window.mainloop()