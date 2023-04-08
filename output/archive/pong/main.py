# Pygame Pong: Deliverable 1

import pygame
import random

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the height and width of the screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

# Create the ball class
class Ball(object):
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.radius = 10
        self.speedx = 5
        self.speedy = 5

    def update(self):
        # Update the ball's position based on its speed
        self.x += self.speedx
        self.y += self.speedy

        # Bounce off the top and bottom walls
        if self.y <= self.radius or self.y >= SCREEN_HEIGHT - self.radius:
            self.speedy = -self.speedy

        # Bounce off the paddles
        if (self.speedx < 0 and self.x - self.radius <= player1.x + player1.width and
                    player1.y <= self.y <= player1.y + player1.height):
            self.speedx = -self.speedx
        elif (self.speedx > 0 and self.x + self.radius >= player2.x and
                          player2.y <= self.y <= player2.y + player2.height):
            self.speedx = -self.speedx

        # If the ball goes off the screen, reset it
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.__init__()

    def display(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

    def collide(self):
        self.speedx = -self.speedx

# Create the paddle class
class Paddle(object):
    def __init__(self, x):
        self.x = x
        self.y = SCREEN_HEIGHT / 2
        self.width = 10
        self.height = 75
        self.speed = 5

    def update(self):
        # Move the paddle up or down depending on the arrow key pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= self.speed
        elif keys[pygame.K_DOWN]:
            self.y += self.speed

        # Make sure the paddle doesn't go off the top or bottom of the screen
        if self.y < 0:
            self.y = 0
        elif self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height

    def display(self, screen):
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.x, self.y, self.width, self.height))

# Initialize Pygame
pygame.init()

# Set the size of the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the caption of the window
pygame.display.set_caption("Pygame Pong")

# Create the ball and paddles
ball = Ball()
player1 = Paddle(25)
player2 = Paddle(SCREEN_WIDTH - 35)

# Set up the clock
clock = pygame.time.Clock()

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the score
score1 = 0
score2 = 0

# Set up the game loop
done = False
while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Update the ball and paddles
    ball.update()
    player1.update()
    player2.update()

    # Check for ball collision with the walls
    if ball.x <= ball.radius:
        score2 += 1
        ball.collide()
    elif ball.x >= SCREEN_WIDTH - ball.radius:
        score1 += 1
        ball.collide()

    # Draw the background
    screen.fill(BLACK)

    # Draw the ball and paddles
    ball.display(screen)
    player1.display(screen)
    player2.display(screen)

    # Draw the score
    score_text = font.render(str(score1) + " - " + str(score2), True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH / 2 - score_text.get_width() / 2, 10))

    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

##JOB_COMPLETE##