import pygame
import os


class Sound:
    def __init__(self, file_path, volume=0.5):
        self.sound = pygame.mixer.Sound(file_path)
        self.sound.set_volume(volume)

    def play(self):
        self.sound.play()


class Music:
    def __init__(self, file_path, volume=0.5):
        self.file_path = file_path
        self.volume = volume
        self.playing = False

    def play(self):
        if not self.playing:
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
            self.playing = True


class Ball(pygame.sprite.Sprite):
    def __init__(self, image_path, speed, bounds):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(bounds.centerx, bounds.centery))
        self.speed = speed
        self.bounds = bounds
        self.direction = pygame.math.Vector2(1, 1).normalize()

    def update(self, dt, paddles):
        self.rect.move_ip(self.speed * dt * self.direction.x, self.speed * dt * self.direction.y)

        if self.rect.left < self.bounds.left or self.rect.right > self.bounds.right:
            self.direction.x *= -1
            self.rect.clamp_ip(self.bounds)
            Sound('bounce.wav').play()

        if self.rect.top < self.bounds.top or self.rect.bottom > self.bounds.bottom:
            self.direction.y *= -1
            self.rect.clamp_ip(self.bounds)
            Sound('bounce.wav').play()

        paddle_collision = pygame.sprite.spritecollideany(self, paddles)
        if paddle_collision:
            self.direction.y *= -1

            if isinstance(paddle_collision, AI):
                self.direction.x = (self.rect.centerx - paddle_collision.rect.centerx) / paddle_collision.rect.width
                Sound('bounce.wav').play()

            elif isinstance(paddle_collision, Player):
                self.direction.x = (self.rect.centerx - paddle_collision.rect.centerx) / (paddle_collision.rect.width * 1.5)
                Sound('bounce.wav').play()


class Paddle(pygame.sprite.Sprite):
    def __init__(self, image_path, bounds):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(bounds.centerx, bounds.bottom))
        self.bounds = bounds
        self.speed = 0

    def update(self, dt, ball=None):
        self.rect.move_ip(self.speed * dt, 0)
        self.rect.clamp_ip(self.bounds)

        if ball:
            if ball.rect.colliderect(self.rect):
                ball.rect.clamp_ip(self.rect.left, self.rect.top, self.rect.right, self.rect.top)
                ball.direction.y *= -1


class Player(Paddle):
    def __init__(self, image_path, bounds, controls):
        super().__init__(image_path, bounds)
        self.score = 0
        self.controls = controls

    def update(self, dt, ball=None):
        self.speed = 0

        key_state = pygame.key.get_pressed()

        if key_state[self.controls['LEFT']]:
            self.speed = -500 * dt

        elif key_state[self.controls['RIGHT']]:
            self.speed = 500 * dt

        super().update(dt, ball)


class AI(Paddle):
    def __init__(self, image_path, bounds, difficulty):
        super().__init__(image_path, bounds)
        self.difficulty = difficulty
        self.target_x = self.rect.centerx

    def update(self, dt, ball=None):
        if ball:
            if self.difficulty == 'easy':
                self.target_x = ball.rect.centerx

            elif self.difficulty == 'medium':
                if ball.rect.centery < self.bounds.bottom / 2:
                    self.target_x = ball.rect.centerx
                else:
                    self.target_x = self.bounds.centerx

            elif self.difficulty == 'hard':
                offset = ball.rect.centerx - self.rect.centerx
                self.target_x += offset * 0.3

            self.speed = min(max(self.target_x - self.rect.centerx, -500 * dt), 500 * dt)

        super().update(dt)


def main(difficulty='medium'):
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    bounds = screen.get_rect()
    clock = pygame.time.Clock()

    background = pygame.image.load(os.path.join('assets', 'background.png')).convert()

    font = pygame.font.Font(os.path.join('assets', 'Pixeltype.ttf'), 50)

    players = pygame.sprite.Group(
        Player(os.path.join('assets', 'paddle.png'), bounds.inflate(-50, 0), {'LEFT': pygame.K_a, 'RIGHT': pygame.K_d}),
        AI(os.path.join('assets', 'paddle.png'), bounds.inflate(-50, 0), difficulty)
    )

    ball = Ball(os.path.join('assets', 'ball.png'), 500, bounds)
    sprites = pygame.sprite.Group(ball, *players)

    Music(os.path.join('assets', 'music.mp3')).play()

    def handle_event(event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            elif event.key == pygame.K_SPACE:
                reset()

    def update(dt):
        sprites.update(dt, paddles=players.sprites())

        if ball.rect.bottom > bounds.bottom:
            players.sprites()[0].score += 1
            reset()

        elif ball.rect.top < bounds.top:
            players.sprites()[1].score += 1
            reset()

    def draw():
        screen.blit(background, bounds)

        for sprite in sprites:
            screen.blit(sprite.image, sprite.rect)

        score_surface = font.render(f'{players.sprites()[0].score}  {players.sprites()[1].score}', True, (255, 255, 255))
        screen.blit(score_surface, score_surface.get_rect(midtop=bounds.midtop).move(0, 10))

        pygame.display.flip()

    def reset():
        ball.rect.center = bounds.center
        ball.direction = pygame.math.Vector2(1, 1).rotate(pygame.math.Vector2(1, 0).angle_to(pygame.math.Vector2(-1, 0)))
        players.update(0, ball)
        pygame.time.wait(1000)

    while True:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            handle_event(event)

        update(dt)
        draw()
##JOB_COMPLETE##