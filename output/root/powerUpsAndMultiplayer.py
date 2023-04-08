import pygame
import random

# Powerup variables
POWERUP_SPEED_CHANGE = 2
POWERUP_PADDLE_SIZE_CHANGE = 50
POWERUP_DURATION_SECONDS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Paddle variables
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Ball variables
BALL_WIDTH = 10
BALL_HEIGHT = 10
BALL_SPEED = 5

# Multiplayer variables
PLAYER_ONE_CONTROLS = {
    "up": pygame.K_w,
    "down": pygame.K_s
}
PLAYER_TWO_CONTROLS = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN
}

class Paddle:
    def __init__(self, x, y, up_key, down_key):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        self.up_key = up_key
        self.down_key = down_key
    
    def move_up(self):
        self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0
    
    def move_down(self):
        self.rect.y += self.speed
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH/2-BALL_WIDTH/2, WINDOW_HEIGHT/2-BALL_HEIGHT/2, BALL_WIDTH, BALL_HEIGHT)
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED
        self.last_hit = None
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.speed_x *= -1
        
        if self.rect.top < 0 or self.rect.bottom > WINDOW_HEIGHT:
            self.speed_y *= -1
            
    def detect_collision(self, paddles):
        for paddle in paddles:
            if self.rect.colliderect(paddle.rect) and paddle != self.last_hit:
                self.speed_x *= -1
                self.last_hit = paddle
                return True
        
        return False

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = 2
        self.type = random.choice(["increase_speed", "decrease_speed", "increase_paddle_size", "decrease_paddle_size"])
        self.start_time = 0
    
    def move(self):
        self.rect.y += self.speed
        
        if self.rect.bottom > WINDOW_HEIGHT:
            self.kill()
            
    def activate(self, player_one, player_two, ball):
        if self.type == "increase_speed":
            ball.speed_x += POWERUP_SPEED_CHANGE
            ball.speed_y += POWERUP_SPEED_CHANGE
        
        elif self.type == "decrease_speed":
            ball.speed_x -= POWERUP_SPEED_CHANGE
            ball.speed_y -= POWERUP_SPEED_CHANGE
        
        elif self.type == "increase_paddle_size":
            if self.rect.colliderect(player_one.rect):
                player_one.rect.h += POWERUP_PADDLE_SIZE_CHANGE
                
            elif self.rect.colliderect(player_two.rect):
                player_two.rect.h += POWERUP_PADDLE_SIZE_CHANGE
                
        elif self.type == "decrease_paddle_size":
            if self.rect.colliderect(player_one.rect):
                player_one.rect.h -= POWERUP_PADDLE_SIZE_CHANGE
                
            elif self.rect.colliderect(player_two.rect):
                player_two.rect.h -= POWERUP_PADDLE_SIZE_CHANGE
                
        self.start_time = pygame.time.get_ticks()
                
    def kill(self):
        self.rect.y = -1000
        
    def expired(self):
        return (pygame.time.get_ticks() - self.start_time)/1000 >= POWERUP_DURATION_SECONDS

##JOB_COMPLETE##