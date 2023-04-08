import pygame
import random

# Initialize the game
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Set up the clock
clock = pygame.time.Clock()

# Set up the colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up the fonts
font_small = pygame.font.SysFont(None, 30)
font_medium = pygame.font.SysFont(None, 50)
font_large = pygame.font.SysFont(None, 80)

# Set up the sound effects
#bounce_sound = pygame.mixer.Sound("bounce.wav")
#wall_sound = pygame.mixer.Sound("wall.wav")

# Set up the variables for the game
ball_speed = 7
paddle_speed = 7
difficulty = "easy"
ball_x_speed = ball_speed
ball_y_speed = ball_speed
player_score = 0
ai_score = 0

# Set up the paddle dimensions
paddle_width = 15
paddle_height = 100

# Set up the ball dimensions
ball_width = 15
ball_height = 15

# Set up the paddles
player_paddle_x = 50
player_paddle_y = (screen_height / 2) - (paddle_height / 2)
ai_paddle_x = screen_width - 50 - paddle_width
ai_paddle_y = (screen_height / 2) - (paddle_height / 2)

##JOB_COMPLETE##