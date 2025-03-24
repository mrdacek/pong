import turtle
import random
import sqlite3
import subprocess
import sys


# Nastavení databáze
conn = sqlite3.connect("hardcore.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY CHECK (id = 1), 
        player_a_wins INTEGER DEFAULT 0, 
        player_b_wins INTEGER DEFAULT 0
    )
''')
conn.commit()

# Funkce pro načtení skóre z databáze
def load_scores():
    global total_wins_a, total_wins_b
    cursor.execute("SELECT player_a_wins, player_b_wins FROM scores WHERE id = 1")
    row = cursor.fetchone()
    if row:
        total_wins_a, total_wins_b = row
    else:
        total_wins_a, total_wins_b = 0, 0
        cursor.execute("INSERT INTO scores (id, player_a_wins, player_b_wins) VALUES (1, 0, 0)")
        conn.commit()

# Funkce pro uložení skóre do databáze
def save_scores():
    cursor.execute("UPDATE scores SET player_a_wins = ?, player_b_wins = ? WHERE id = 1", (total_wins_a, total_wins_b))
    conn.commit()

# Načíst skóre při spuštění hry
load_scores()

# Setup window
wn = turtle.Screen()
wn.title("Pong by honza")
wn.bgcolor("purple")
wn.setup(width=800, height=600)
wn.tracer(0)

# Global variables
score_a = 0
score_b = 0
total_wins_a = 0
total_wins_b = 0
game_running = False
paused = False

# Paddle and ball objects
paddle_a = None
paddle_b = None
ball = None
pen = None
buttons = {}
obstacles = []

def create_obstacle():
    obstacle = turtle.Turtle()
    obstacle.speed(0)
    obstacle.shape("square")
    obstacle.color("white")
    obstacle.shapesize(stretch_wid=1, stretch_len=5)
    obstacle.penup()
    obstacle.goto(random.randint(-200, 200), random.randint(-200, 200))
    obstacles.append(obstacle)

def clear_obstacles():
    """Odstraní všechny překážky"""
    global obstacles
    for obstacle in obstacles:
        obstacle.hideturtle()  # Skryje překážku
    obstacles.clear()  # Vymaže seznam překážek

def random_direction():
    speed = 0.8 # Fixed speed
    dx = random.choice([-3, 3]) * speed
    dy = dy = random.randint(-10, 10) * speed
    return dx, dy

def score_display():
    pen.clear()
    pen.goto(0, 260)
    pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 22, "bold"))
    pen.goto(0, 230)
    pen.write(f"Total Wins - Player A: {total_wins_a}  Player B: {total_wins_b}", align="center", font=("Courier", 16, "normal"))

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



def reset_round():
    global ball
    score_display()
    ball.goto(0, 0)
    ball.dx, ball.dy = random_direction()
    create_obstacle()


def check_collision_with_obstacles():
    for obstacle in obstacles:
        if obstacle.xcor() - 50 < ball.xcor() < obstacle.xcor() + 50 and obstacle.ycor() - 50 < ball.ycor() < obstacle.ycor() + 50:
            if abs(ball.dx) > abs(ball.dy):  
                ball.dx *= -1  # Odrážení horizontální
            else:
                ball.dy *= -1  # Odrážení vertikální


def reset_game():
    global score_a, score_b, total_wins_a, total_wins_b, game_running, paused
    if score_a > score_b:
        total_wins_a += 1
    elif score_b > score_a:
        total_wins_b += 1
    save_scores()
    score_a = 0
    score_b = 0
    paused = False
    score_display()
    ball.goto(0, 0)
    ball.dx, ball.dy = random_direction()
    paddle_a.goto(-350, 0)
    paddle_b.goto(350, 0)
    game_running = True
    clear_buttons()
    create_button("pause", "Pause", 350, 260, 16, toggle_pause)
    game_loop()
    clear_obstacles()
    
def toggle_pause():
    global paused
    paused = not paused
    buttons["pause"][0].clear()
    create_button("pause", "Resume" if paused else "Pause", 350, 260, 16, toggle_pause)
    if not paused:
        game_loop()

def back_to_main_menu():
    wn.bye()  # Zavře aktuální okno hry
    subprocess.Popen([sys.executable, __file__])  # Restartuje skript od začátku
    sys.exit()  # Ukončí aktuální běžící proces

def add_menu_button():
    create_button("back", " Menu", -350, 260, 16, back_to_main_menu)
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
    ball.dx, ball.dy = random_direction()

    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    score_display()
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
    check_collision_with_obstacles()

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

    for obstacle in obstacles:
        if obstacle.xcor() - 20 < ball.xcor() < obstacle.xcor() + 20 and obstacle.ycor() - 20 < ball.ycor() < obstacle.ycor() + 20:
            ball.setx(obstacle.xcor() + 50 if ball.dx < 0 else obstacle.xcor() - 50)
            ball.dx *= -1
        if obstacle.ycor() - 20 < ball.ycor() < obstacle.ycor() + 20 and obstacle.xcor() - 20 < ball.xcor() < obstacle.xcor() + 20:
            ball.sety(obstacle.ycor() + 20 if ball.dy < 0 else obstacle.ycor() - 20)
            ball.dy *= -1

    if score_a == 3 or score_b == 3:
        pen.clear()
        pen.write(f"{'Player A' if score_a == 3 else 'Player B'} wins!!!", align="center", font=("Courier", 32, "normal"))
        game_running = False
        create_button("reset", "play again", 0, -50, 24, reset_game)
        return
    add_menu_button()

    wn.ontimer(game_loop, 10)

def start_hardcore_game():
    global game_running
    game_running = True
    clear_buttons()
    draw_game()


wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")
wn.onclick(handle_click)

wn.listen()
wn.onclick(handle_click)
create_button("start", "Start Hardcore", 0, 0, 24, start_hardcore_game)
wn.mainloop()

conn.close()

# Close database connection on exit
conn.close()