import pygame
import random
import argparse
import socket
import time
import math

TITLE = 'Snake game'
WIDTH = 600
HEIGHT = 600
BLOCK_SIZE = 20
DELAY_TIME = 500
NEXT_LEVEL = 90 # co 5 level
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
FONT_FAMILY = 'Consolas'
FONT_SIZE = 25
SCORE_STEP = 10
RIGHT_SIDEBAR_WIDTH = 200

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
BACKGROUND_COLOR = WHITE
BODY_COLOR = GREEN
HEAD_COLOR = BLUE
APPLE_COLOR = RED
FONT_COLOR = BLACK
BORDER_COLOR = BLACK

screen = None
font = None
snake = None
direction = None
apple = None
old_tail = None
score = []

Client_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client_game.connect((socket.gethostname(), 1234))

def GameSetup():
    global screen, font, snake, direction, apple, old_tail
    screen = pygame.display.set_mode((WIDTH + RIGHT_SIDEBAR_WIDTH, HEIGHT))
    font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
    snake = [
        {'x': WIDTH // 2, 'y': HEIGHT // 2},
        {'x': WIDTH // 2 - BLOCK_SIZE, 'y': HEIGHT // 2},
        {'x': WIDTH // 2 - 2 * BLOCK_SIZE, 'y': HEIGHT // 2},
        {'x': WIDTH // 2 - 3 * BLOCK_SIZE, 'y': HEIGHT // 2},
        {'x': WIDTH // 2 - 4 * BLOCK_SIZE, 'y': HEIGHT // 2}
    ]
    direction = RIGHT
    apple = {'x': 0, 'y': 0}
    old_tail = {'x': 0, 'y': 0}


def init_game():
    pygame.display.set_caption(TITLE)
    screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()


def draw_block(block, color):
    pygame.draw.rect(
        screen,
        color,
        (
            block['x'],
            block['y'],
            BLOCK_SIZE,
            BLOCK_SIZE
        )
    )
    pygame.display.update()


def draw_snake():
    for i in snake:
        draw_block(i, BODY_COLOR)
    draw_block(snake[0], HEAD_COLOR)
    pygame.display.update()


def move():
    old_tail = snake[len(snake) - 1]

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = dict(snake[i - 1])
    if direction == UP:
        snake[0]['y'] -= BLOCK_SIZE
    elif direction == DOWN:
        snake[0]['y'] += BLOCK_SIZE
    elif direction == LEFT:
        snake[0]['x'] -= BLOCK_SIZE
    elif direction == RIGHT:
        snake[0]['x'] += BLOCK_SIZE

    draw_block(old_tail, BACKGROUND_COLOR)
    draw_block(snake[1], BODY_COLOR)
    draw_block(snake[0], HEAD_COLOR)
    pygame.display.update()


def is_bite_itself():
    for i in range(1, len(snake)):
        if snake[0] == snake[i]:
            return True
    return False


def is_hit_wall():
    return (
        snake[0]['x'] == -BLOCK_SIZE or
        snake[0]['y'] == -BLOCK_SIZE or
        snake[0]['x'] == WIDTH or
        snake[0]['y'] == HEIGHT
    )


def generate_apple():
    x = random.randint(0, WIDTH // BLOCK_SIZE - 1)
    y = random.randint(0, HEIGHT // BLOCK_SIZE - 1)
    apple['x'] = x * BLOCK_SIZE
    apple['y'] = y * BLOCK_SIZE
    draw_block(apple, APPLE_COLOR)
    pygame.display.update()


def is_ate_apple():
    for i in snake:
        if i == apple:
            return True
    return False


def grow_up():
    snake.append(old_tail)


def display_score(level_score, level):
    pygame.draw.rect(
        screen,
        BACKGROUND_COLOR,
        (
            WIDTH,
            0,
            RIGHT_SIDEBAR_WIDTH,
            HEIGHT
        )
    )
    # Draw a divider between snakeboard and menu
    pygame.draw.rect(
        screen,
        BORDER_COLOR,
        (
            WIDTH,
            0,
            1,
            HEIGHT
        )
    )
    screen.blit(
        font.render(
            f'Level: {level}',
            True,
            BLUE
        ),
        (WIDTH + 10, 10)
    )
    screen.blit(
        font.render(
            f'Score: {level_score}',
            True,
            FONT_COLOR
        ),
        (WIDTH + 10, 50)
    )
    pygame.display.update()

def RunGameLevel(level):
    GameSetup()
    init_game()
    draw_snake()
    generate_apple()
    display_score(0, level)
    global direction

    level_score = 0
    running = True
    moved = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and moved:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT
                moved = False

        move()
        moved = True

        if is_bite_itself() or is_hit_wall():
            running = False
        elif is_ate_apple():
            level_score += SCORE_STEP
            display_score(level_score, level)
            generate_apple()
            grow_up()

        pygame.time.wait(DELAY_TIME-level*NEXT_LEVEL)

    pygame.display.quit()
    return level_score

def Send_Score_Local_Host(score):
    global Client_game
    try:
        Client_game.send(bytes(str(score), 'utf-8'))
    except:
        print("Send error!")
        

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--level', type=int, default=0, help='Level is a unsigned integer number')
    parser.add_argument('--solo', type=int, default=0, help='solo is 0 or 1')
    opt = parser.parse_args()

    pygame.init()
    pygame.font.init()

    if opt.solo == 0:
        score.append(RunGameLevel(opt.level))
        Send_Score_Local_Host(score[0])
        score.clear()
    elif opt.solo == 1:
        for i in range(0, 6):
            score.append(RunGameLevel(i))
            time.sleep(5) # delay 5 giay
        Send_Score_Local_Host(sum(score))
        score.clear()

    Client_game.close()
    pygame.quit()
    