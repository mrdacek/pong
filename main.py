import turtle

# Setup window
wn = turtle.Screen()
wn.title("Pong by honza")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Global variables
score_a = 0
score_b = 0
game_running = False
paused = False

# Paddle and ball objects
paddle_a = None
paddle_b = None
ball = None
pen = None
buttons = {}

# Function to create buttons
def create_button(name, text, x, y, size=24, action=None):
    btn = turtle.Turtle()
    btn.speed(0)
    btn.color("white")
    btn.penup()
    btn.hideturtle()
    btn.goto(x, y)
    btn.write(text, align="center", font=("Courier", size, "normal"))
    buttons[name] = (btn, action, x, y, size)

def handle_click(x, y):
    global game_running, paused
    for name, (btn, action, bx, by, size) in buttons.items():
        if bx - 50 < x < bx + 50 and by - 20 < y < by + 20:
            if action:
                action()

def start_game():
    global game_running
    if not game_running:
        game_running = True
        clear_buttons()
        draw_game()

def reset_game():
    global score_a, score_b, game_running, paused
    score_a = 0
    score_b = 0
    paused = False
    pen.clear()
    pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))
    ball.goto(0, 0)
    ball.dx, ball.dy = 3, -3
    paddle_a.goto(-350, 0)
    paddle_b.goto(350, 0)
    game_running = True
    clear_buttons()
    create_button("pause", "Pause", 350, 260, 16, toggle_pause)
    game_loop()

def toggle_pause():
    global paused
    paused = not paused
    buttons["pause"][0].clear()
    create_button("pause", "Resume" if paused else "Pause", 350, 260, 16, toggle_pause)
    if not paused:
        game_loop()

def clear_buttons():
    for btn, _, _, _, _ in buttons.values():
        btn.clear()
    buttons.clear()

def draw_game():
    global paddle_a, paddle_b, ball, pen
    paddle_a = turtle.Turtle()
    paddle_a.speed(0)
    paddle_a.shape("square")
    paddle_a.color("white")
    paddle_a.shapesize(stretch_wid=5, stretch_len=1)
    paddle_a.penup()
    paddle_a.goto(-350, 0)

    paddle_b = turtle.Turtle()
    paddle_b.speed(0)
    paddle_b.shape("square")
    paddle_b.color("white")
    paddle_b.shapesize(stretch_wid=5, stretch_len=1)
    paddle_b.penup()
    paddle_b.goto(350, 0)

    ball = turtle.Turtle()
    ball.speed(3)
    ball.shape("circle")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    ball.dx, ball.dy = 3, -3

    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

    create_button("pause", "Pause", 350, 260, 16, toggle_pause)
    game_loop()

def paddle_a_up():
    if paddle_a.ycor() < 250:
        paddle_a.sety(min(250, paddle_a.ycor() + 20))

def paddle_a_down():
    if paddle_a.ycor() > -240:
        paddle_a.sety(max(-240, paddle_a.ycor() - 20))

def paddle_b_up():
    if paddle_b.ycor() < 250:
        paddle_b.sety(min(250, paddle_b.ycor() + 20))

def paddle_b_down():
    if paddle_b.ycor() > -240:
        paddle_b.sety(max(-240, paddle_b.ycor() - 20))

def game_loop():
    global score_a, score_b, game_running, paused
    if not game_running or paused:
        return

    wn.update()
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    if ball.ycor() > 290 or ball.ycor() < -290:
        ball.sety(290 if ball.ycor() > 290 else -290)
        ball.dy *= -1

    if ball.xcor() > 390:
        score_a += 1
        reset_round()
    elif ball.xcor() < -390:
        score_b += 1
        reset_round()

    if (340 < ball.xcor() < 350 and paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50) or \
       (-350 < ball.xcor() < -340 and paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.dx *= -1.1  # Increase speed after hitting paddle

    if score_a == 3 or score_b == 3:
        pen.clear()
        pen.write(f"{'Player A' if score_a == 3 else 'Player B'} wins!!!", align="center", font=("Courier", 32, "normal"))
        game_running = False
        create_button("reset", "Reset", 0, -50, 24, reset_game)
        return

    wn.ontimer(game_loop, 10)

def reset_round():
    global ball
    pen.clear()
    pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))
    ball.goto(0, 0)
    ball.dx, ball.dy = 3, -3

wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")
wn.onclick(handle_click)

create_button("start", "Start", 0, 0, 24, start_game)
wn.mainloop()
