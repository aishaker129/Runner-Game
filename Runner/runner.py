import pygame
import random
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Game constants
SCREEN_WIDTH = 850
SCREEN_HEIGHT = 600
PLAYER_SIZE = 0.03
OBSTACLE_SIZE = 0.06
INITIAL_FALL_SPEED = 0.07

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

def draw_text(x, y, text, size=18):
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def spawn_obstacle():
    x_pos = random.uniform(-0.9, 0.9)
    obstacles.append([x_pos, 1.0])

def move_obstacles():
    global lives, game_over, score
    new_obstacles = []
    for obs in obstacles:
        obs[1] -= fall_speed
        collided = abs(obs[0] - player_x) < 0.1 and abs(obs[1] - player_y) < 0.1

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


def reset_game():
    global player_x, obstacles, score, lives, game_over, fall_speed
    player_x = 0
    obstacles.clear()
    score = 0
    lives = 3
    game_over = False
    fall_speed = INITIAL_FALL_SPEED

def render_overlay():
    draw_text(-0.98, 0.9, f"Score: {score}")
    draw_text(-0.98, 0.8, f"Lives: {lives}")

def show_start_screen():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_text(-0.4, 0.1, "Falling Blocks Game")
    draw_text(-0.5, -0.1, "Press Any Key to Start")
    pygame.display.flip()
    wait_for_key()

def show_game_over_screen():
    glClear(GL_COLOR_BUFFER_BIT)
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

def wait_for_restart_or_quit():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    reset_game()
                    return
                elif event.key == K_q:
                    pygame.quit()
                    quit()

def game_loop():
    global player_x, paused, fall_speed, game_over

    clock = pygame.time.Clock()
    spawn_timer = 0
    difficulty_timer = 0

    while not game_over:
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
            continue

        spawn_timer += 1
        difficulty_timer += 1

        if spawn_timer % 30 == 0:
            spawn_obstacle()

        if difficulty_timer % 600 == 0:
            fall_speed += 0.005 

        move_obstacles()

        glClear(GL_COLOR_BUFFER_BIT)
        draw_square(player_x, player_y, PLAYER_SIZE, (0, 1, 0))

        for obs in obstacles:
            draw_square(obs[0], obs[1], OBSTACLE_SIZE, (1, 0, 0))

        render_overlay()

        pygame.display.flip()
        clock.tick(30)

    show_game_over_screen()

def main():
    pygame.init()
    glutInit()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    show_start_screen()
    game_loop()

if __name__ == "__main__":
    main()