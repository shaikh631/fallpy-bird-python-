import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
WIDTH = 1200
HEIGHT = 800
GRAVITY = 0.41
FLAP_STRENGTH = -7.5
PIPE_GAP = 200
PIPE_FREQUENCY = 1500  # milliseconds
GROUND_HEIGHT = 50
CLOUD_FREQUENCY = 3000  # new cloud every 3 seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
SKY_BLUE = (118, 213, 254)
YELLOW = (255, 215, 0)

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Times New', 40)


class Bird:
    def __init__(self):
        self.x = 300
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 25  # in pixels
        self.color = YELLOW

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, int(self.y)), self.radius)
        pygame.draw.polygon(screen, (255, 0, 0), [
            (self.x + self.radius + 10, self.y),
            (self.x + 5 + self.radius - 10, self.y + 14),
            (self.x + 5 + self.radius - 10, self.y - 15)
        ])
        pygame.draw.circle(screen, WHITE, (self.x + 6, int(self.y) - 7), 6)
        pygame.draw.circle(screen, BLACK, (self.x + 7, int(self.y) - 7), 2)

    def get_mask(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)


class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.top_height = random.randint(50, HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50)
        self.bottom_height = HEIGHT - GROUND_HEIGHT - self.top_height - PIPE_GAP
        self.width = 70
        self.passed = False
        self.color = GREEN

    def update(self):
        self.x -= 3

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, self.width, self.top_height), 2)

        pygame.draw.rect(screen, self.color,
                         (self.x, HEIGHT - GROUND_HEIGHT - self.bottom_height,
                          self.width, self.bottom_height))
        pygame.draw.rect(screen, BLACK,
                         (self.x, HEIGHT - GROUND_HEIGHT - self.bottom_height,
                          self.width, self.bottom_height), 2)

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_pipe = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_pipe = pygame.Rect(
            self.x, HEIGHT - GROUND_HEIGHT - self.bottom_height,
            self.width, self.bottom_height)

        return bird_mask.colliderect(top_pipe) or bird_mask.colliderect(bottom_pipe)


class Cloud:
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(50, 250)   # Clouds at random heights
        self.speed = 1.5                   # Slower than pipes
        self.color = WHITE
        self.size = random.randint(25, 50)  # Random size for variation

    def update(self):
        self.x -= self.speed

    def draw(self):
        # Draw fluffy cloud using overlapping circles
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, self.color, (int(self.x + self.size), int(self.y) + 10), self.size)
        pygame.draw.circle(screen, self.color, (int(self.x - self.size), int(self.y) + 10), self.size)


def draw_ground():
    pygame.draw.rect(screen, (222, 184, 135),
                     (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(screen, BLACK,
                     (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT), 2)


def draw_score(score):
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 50))


def game_over_screen(score):
    screen.fill(SKY_BLUE)
    game_over_text = font.render("Game Over", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    restart_text = font.render("Press", True, BLACK)
    red_text = font.render("SPACE",True,(213,0,0))
    r_text = font.render("To Reset", True, BLACK)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2 - 100, HEIGHT // 2 + 60))
    screen.blit(red_text, (WIDTH // 2 - red_text.get_width() // 2, HEIGHT // 2 + 60))
    screen.blit(r_text, (WIDTH // 2 - r_text.get_width() // 2 + 120, HEIGHT // 2 + 60))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def main():
    while True:  # Loop to restart game
        bird = Bird()
        pipes = []
        clouds = []
        score = 0
        last_pipe = pygame.time.get_ticks()
        last_cloud = pygame.time.get_ticks()
        game_active = True

        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.flap()

            screen.fill(SKY_BLUE)

            # Clouds
            time_now = pygame.time.get_ticks()
            if time_now - last_cloud > CLOUD_FREQUENCY:
                clouds.append(Cloud())
                last_cloud = time_now

            for cloud in clouds[:]:
                cloud.update()
                cloud.draw()
                if cloud.x < -100:  # remove off-screen
                    clouds.remove(cloud)

            # Bird
            bird.update()
            bird.draw()

            # Pipes
            if time_now - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = time_now

            for pipe in pipes[:]:
                pipe.update()
                pipe.draw()

                if pipe.x + pipe.width < bird.x and not pipe.passed:
                    pipe.passed = True
                    score += 1

                if pipe.collide(bird):
                    game_active = False

                if pipe.x < -pipe.width:
                    pipes.remove(pipe)

            if bird.y + bird.radius > HEIGHT - GROUND_HEIGHT:
                game_active = False

            if bird.y - bird.radius < 0:
                bird.y = bird.radius
                bird.velocity = 0

            draw_score(score)
            draw_ground()
            pygame.display.update()
            clock.tick(60)

        # Game over screen and wait for restart
        game_over_screen(score)


if __name__ == "__main__":
    main()
