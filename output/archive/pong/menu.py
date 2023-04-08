# Import necessary libraries
import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up font
font = pygame.font.SysFont("calibri", 40)

# Set up game variables
player1_score = 0
player2_score = 0
game_over = False
player1_wins = False
player2_wins = False

# Set up paddles
paddle_width = 15
paddle_height = 60
paddle_speed = 5
player1_paddle_x = 25
player1_paddle_y = screen_height / 2 - paddle_height / 2
player2_paddle_x = screen_width - 25 - paddle_width
player2_paddle_y = screen_height / 2 - paddle_height / 2

# Set up ball
ball_width = 15
ball_height = 15
ball_speed = 5
ball_x_direction = 1
ball_y_direction = 1
ball_x = screen_width / 2 - ball_width / 2
ball_y = screen_height / 2 - ball_height / 2

# Set up AI
ai_speed = 3
ai_paddle_up = False
ai_paddle_down = False

# Define function to draw paddles
def draw_paddles():
    global player1_paddle_y, player2_paddle_y, ai_paddle_up, ai_paddle_down

    # Move AI paddle
    if ball_x_direction == 1:
        if ball_y + ball_height / 2 > player2_paddle_y + paddle_height / 2:
            ai_paddle_down = True
        else:
            ai_paddle_down = False
        if ball_y + ball_height / 2 < player2_paddle_y + paddle_height / 2:
            ai_paddle_up = True
        else:
            ai_paddle_up = False
    else:
        ai_paddle_up = False
        ai_paddle_down = False

    # Move player 1 paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_paddle_y > 0:
        player1_paddle_y -= paddle_speed
    if keys[pygame.K_s] and player1_paddle_y < screen_height - paddle_height:
        player1_paddle_y += paddle_speed

    # Move player 2 paddle with AI or manually
    if ai_paddle_up and player2_paddle_y > 0:
        player2_paddle_y -= ai_speed
    if ai_paddle_down and player2_paddle_y < screen_height - paddle_height:
        player2_paddle_y += ai_speed

    # Draw player 1 paddle
    pygame.draw.rect(screen, white, (player1_paddle_x, player1_paddle_y, paddle_width, paddle_height))

    # Draw player 2 paddle
    pygame.draw.rect(screen, white, (player2_paddle_x, player2_paddle_y, paddle_width, paddle_height))

# Define function to draw ball
def draw_ball():
    global ball_x, ball_y, ball_x_direction, ball_y_direction, player1_score, player2_score, game_over, player1_wins, player2_wins

    # Move ball
    ball_x += ball_speed * ball_x_direction
    ball_y += ball_speed * ball_y_direction

    # Bounce ball off walls
    if ball_y < 0 or ball_y > screen_height - ball_height:
        ball_y_direction = -ball_y_direction
    if ball_x < 0:
        player2_score += 1
        ball_x = screen_width / 2 - ball_width / 2
        ball_y = screen_height / 2 - ball_height / 2
        ball_x_direction = -ball_x_direction
    if ball_x > screen_width - ball_width:
        player1_score += 1
        ball_x = screen_width / 2 - ball_width / 2
        ball_y = screen_height / 2 - ball_height / 2
        ball_x_direction = -ball_x_direction

    # Bounce ball off paddles
    if ball_x_direction == -1 and player1_paddle_x + paddle_width >= ball_x >= player1_paddle_x and player1_paddle_y + paddle_height >= ball_y >= player1_paddle_y:
        ball_x_direction = 1
    if ball_x_direction == 1 and player2_paddle_x <= ball_x + ball_width <= player2_paddle_x + paddle_width and player2_paddle_y + paddle_height >= ball_y >= player2_paddle_y:
        ball_x_direction = -1

    # Check for end game condition
    if player1_score >= 10:
        game_over = True
        player1_wins = True
    elif player2_score >= 10:
        game_over = True
        player2_wins = True

    # Draw ball
    pygame.draw.rect(screen, white, (ball_x, ball_y, ball_width, ball_height))# Import necessary libraries
import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Set up colors and font
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.SysFont("calibri", 40)

# Set up game variables
player1_score = 0
player2_score = 0
game_over = False
player1_wins = False
player2_wins = False

# Set up paddles and ball
paddle_width = 15
paddle_height = 60
paddle_speed = 5
player1_paddle_x = 25
player1_paddle_y = screen_height / 2 - paddle_height / 2
player2_paddle_x = screen_width - 25 - paddle_width
player2_paddle_y = screen_height / 2 - paddle_height / 2
ball_width = 15
ball_height = 15
ball_speed = 5
ball_x_direction = 1
ball_y_direction = 1
ball_x = screen_width / 2 - ball_width / 2
ball_y = screen_height / 2 - ball_height / 2

# Set up AI
ai_speed = 3
ai_paddle_up = False
ai_paddle_down = False

# Define function to draw paddles
def draw_paddles():
    global player1_paddle_y, player2_paddle_y, ai_paddle_up, ai_paddle_down

    # Move AI paddle
    if ball_x_direction == 1:
        if ball_y + ball_height / 2 > player2_paddle_y + paddle_height / 2:
            ai_paddle_down = True
        else:
            ai_paddle_down = False
        if ball_y + ball_height / 2 < player2_paddle_y + paddle_height / 2:
            ai_paddle_up = True
        else:
            ai_paddle_up = False
    else:
        ai_paddle_up = False
        ai_paddle_down = False

    # Move player 1 paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_paddle_y > 0:
        player1_paddle_y -= paddle_speed
    if keys[pygame.K_s] and player1_paddle_y < screen_height - paddle_height:
        player1_paddle_y += paddle_speed

    # Move player 2 paddle with AI or manually
    if ai_paddle_up and player2_paddle_y > 0:
        player2_paddle_y -= ai_speed
    if ai_paddle_down and player2_paddle_y < screen_height - paddle_height:
        player2_paddle_y += ai_speed

    # Draw player 1 paddle
    pygame.draw.rect(screen, white, (player1_paddle_x, player1_paddle_y, paddle_width, paddle_height))

    # Draw player 2 paddle
    pygame.draw.rect(screen, white, (player2_paddle_x, player2_paddle_y, paddle_width, paddle_height))

# Define function to draw ball
def draw_ball():
    global ball_x, ball_y, ball_x_direction, ball_y_direction, player1_score, player2_score, game_over, player1_wins, player2_wins

    # Move ball
    ball_x += ball_speed * ball_x_direction
    ball_y += ball_speed * ball_y_direction

    # Bounce ball off walls
    if ball_y < 0 or ball_y > screen_height - ball_height:
        ball_y_direction = -ball_y_direction
    if ball_x < 0:
        player2_score += 1
        ball_x = screen_width / 2 - ball_width / 2
        ball_y = screen_height / 2 - ball_height / 2
        ball_x_direction = -ball_x_direction
    if ball_x > screen_width - ball_width:
        player1_score += 1
        ball_x = screen_width / 2 - ball_width / 2
        ball_y = screen_height / 2 - ball_height / 2
        ball_x_direction = -ball_x_direction

    # Bounce ball off paddles
    if ball_x_direction == -1 and player1_paddle_x + paddle_width >= ball_x >= player1_paddle_x and player1_paddle_y + paddle_height >= ball_y >= player1_paddle_y:
        ball_x_direction = 1
    if ball_x_direction == 1 and player2_paddle_x <= ball_x + ball_width <= player2_paddle_x + paddle_width and player2_paddle_y + paddle_height >= ball_y >= player2_paddle_y:
        ball_x_direction = -1

    # Check for end game condition
    if player1_score >= 10:
        game_over = True
        player1_wins = True
    elif player2_score >= 10:
        game_over = True
        player2_wins = True

    # Draw ball
    pygame.draw.rect(screen, white, (ball_x, ball_y, ball_width, ball_height))

# Define function to display score
def display_score():
    player1_text = font.render(str(player1_score), True, white)
    player2_text = font.render(str(player2_score), True, white)
    screen.blit(player1_text, (screen_width / 4, 10))
    screen.blit(player2_text, (screen_width * 3 / 4 - player2_text.get_width(), 10))

# Run game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Draw screen
    screen.fill(black)
    draw_paddles()
    draw_ball()
    display_score()

    # Update display
    pygame.display.update()

# Display winner
if player1_wins:
    winner_text = font.render("Player 1 wins!", True, white)
else:
    winner_text = font.render("Player 2 wins!", True, white)
screen.blit(winner_text, (screen_width / 2 - winner_text.get_width() / 2, screen_height / 2 - winner_text.get_height() / 2))

# Update display and wait for user to quit
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

##JOB_COMPLETE##