import pygame
import random
from math import cos, sin
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Game constants
SCREEN_WIDTH = 850
SCREEN_HEIGHT = 600
PLAYER_SIZE = 0.03
OBSTACLE_SIZE = 0.06
INITIAL_FALL_SPEED = 0.4  # Used with delta time
OBSTACLE_SHAPES = ['square', 'triangle', 'circle', 'hexagon', 'diamond', 'star']
OBSTACLE_COLORS = [
    (1, 0, 0),     # Red
    (0, 0, 1),     # Blue
    (1, 1, 0),     # Yellow
    (1, 0, 1),     # Magenta
    (0, 1, 1),     # Cyan
    (1, 0.5, 0)    # Orange
]

# Game variables
player_x = 0
player_y = -0.8
obstacles = []
score = 0
lives = 3
fall_speed = INITIAL_FALL_SPEED
game_over = False
paused = False

def draw_square(x, y, size, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x - size, y - size)
    glVertex2f(x + size, y - size)
    glVertex2f(x + size, y + size)
    glVertex2f(x - size, y + size)
    glEnd()

def draw_background():
    glColor3f(0.2, 0.6, 0.2)  # Green grass
    glBegin(GL_QUADS)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, 1)
    glVertex2f(-1, 1)
    glEnd()

def draw_text(x, y, text, size=18):
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def draw_shape(x, y, size, color, shape):
    glColor3f(*color)
    if shape == 'square':
        glBegin(GL_QUADS)
        glVertex2f(x - size, y - size)
        glVertex2f(x + size, y - size)
        glVertex2f(x + size, y + size)
        glVertex2f(x - size, y + size)
        glEnd()
    else:
        glBegin(GL_POLYGON)
        if shape == 'triangle':
            glVertex2f(x, y + size)
            glVertex2f(x - size, y - size)
            glVertex2f(x + size, y - size)
        elif shape == 'circle':
            for i in range(20):
                angle = 2 * 3.14159 * i / 20
                glVertex2f(x + size * cos(angle), y + size * sin(angle))
        elif shape == 'hexagon':
            for i in range(6):
                angle = 2 * 3.14159 * i / 6
                glVertex2f(x + size * cos(angle), y + size * sin(angle))
        elif shape == 'diamond':
            glVertex2f(x, y + size)
            glVertex2f(x + size, y)
            glVertex2f(x, y - size)
            glVertex2f(x - size, y)
        elif shape == 'star':
            for i in range(10):
                angle = i * 2 * 3.14159 / 10
                r = size if i % 2 == 0 else size / 2
                glVertex2f(x + r * cos(angle), y + r * sin(angle))
        glEnd()

def spawn_obstacle():
    x_pos = random.uniform(-0.9, 0.9)
    shape = random.choice(OBSTACLE_SHAPES)
    color_index = OBSTACLE_SHAPES.index(shape)
    color = OBSTACLE_COLORS[color_index]
    obstacles.append([x_pos, 1.0, shape, color])

def move_obstacles(dt):
    global lives, game_over, score
    new_obstacles = []
    for obs in obstacles:
        obs[1] -= fall_speed * dt
        collided = abs(obs[0] - player_x) < (PLAYER_SIZE + OBSTACLE_SIZE) and \
                   abs(obs[1] - player_y) < (PLAYER_SIZE + OBSTACLE_SIZE)

        if collided:
            lives -= 1
            if lives <= 0:
                game_over = True
            continue

        if obs[1] < -1:
            score += 1
        else:
            new_obstacles.append(obs)
    obstacles[:] = new_obstacles

def render_overlay():
    draw_text(-0.98, 0.9, f"Score: {score}")
    draw_text(-0.98, 0.8, f"Lives: {lives}")
    if paused:
        draw_text(-0.1, 0.0, "Paused")

def reset_game():
    global player_x, obstacles, score, lives, game_over, fall_speed, paused
    player_x = 0
    obstacles.clear()
    score = 0
    lives = 3
    game_over = False
    paused = False
    fall_speed = INITIAL_FALL_SPEED

def show_start_screen():
    pygame.mixer.music.stop()
    glClear(GL_COLOR_BUFFER_BIT)
    draw_background()
    draw_text(-0.4, 0.1, "Falling Blocks Game")
    draw_text(-0.5, -0.1, "Press Any Key to Start")
    pygame.display.flip()
    wait_for_key()

def show_game_over_screen():
    pygame.mixer.music.stop()
    glClear(GL_COLOR_BUFFER_BIT)
    draw_background()
    draw_text(-0.4, 0.1, f"Game Over! Score: {score}")
    draw_text(-0.55, -0.1, "Press R to Restart or Q to Quit")
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    reset_game()
                    game_loop()
                    return
                elif event.key == K_q:
                    pygame.quit()
                    quit()

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                return

def game_loop():
    global player_x, paused, fall_speed, game_over
    clock = pygame.time.Clock()
    spawn_timer = 0

    pygame.mixer.music.play(-1)  # Play music in loop

    while not game_over:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and player_x > -0.9:
                    player_x -= 0.1
                elif event.key == K_RIGHT and player_x < 0.9:
                    player_x += 0.1
                elif event.key == K_p:
                    paused = not paused

        if paused:
            glClear(GL_COLOR_BUFFER_BIT)
            draw_background()
            render_overlay()
            pygame.display.flip()
            continue

        spawn_timer += dt
        if spawn_timer >= 1.0:
            spawn_obstacle()
            spawn_timer = 0

        fall_speed += 0.0005  # Slow increase over time
        move_obstacles(dt)

        glClear(GL_COLOR_BUFFER_BIT)
        draw_background()
        draw_square(player_x, player_y, PLAYER_SIZE, (0, 1, 0))  # Player

        for obs in obstacles:
            draw_shape(obs[0], obs[1], OBSTACLE_SIZE, obs[3], obs[2])

        render_overlay()
        pygame.display.flip()

    show_game_over_screen()

def main():
    pygame.init()
    glutInit()
    pygame.mixer.init()
    pygame.mixer.music.load("C://Users//Aishaker//Desktop//Runner//image//audio.mp3")  # Load your background music
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    show_start_screen()
    game_loop()

if __name__ == "__main__":
    main()
