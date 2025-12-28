import pygame
import random
import sys

# ---------- INITIAL SETUP ----------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pro Racing Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

# ---------- COLORS ----------
WHITE = (255, 255, 255)
RED = (220, 20, 60)
GRAY = (60, 60, 60)
BLACK = (0, 0, 0)

# ---------- PLAYER CAR ----------
class PlayerCar:
    def __init__(self):
        self.width = 50
        self.height = 90
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 6

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 100:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 150:
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))


# ---------- ENEMY CAR ----------
class EnemyCar:
    def __init__(self, speed):
        self.width = 50
        self.height = 90
        self.x = random.randint(120, WIDTH - 170)
        self.y = -100
        self.speed = speed

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.y > HEIGHT


# ---------- GAME ----------
def game():
    player = PlayerCar()
    enemies = []
    score = 0
    enemy_speed = 4

    running = True
    while running:
        clock.tick(60)
        screen.fill(GRAY)

        # Road
        pygame.draw.rect(screen, WHITE, (100, 0, 10, HEIGHT))
        pygame.draw.rect(screen, WHITE, (WIDTH - 110, 0, 10, HEIGHT))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.move(keys)

        # Spawn enemies
        if random.randint(1, 50) == 1:
            enemies.append(EnemyCar(enemy_speed))

        # Update enemies
        for enemy in enemies[:]:
            enemy.update()
            enemy.draw()

            # Collision
            if pygame.Rect(player.x, player.y, player.width, player.height).colliderect(
                pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            ):
                running = False

            if enemy.off_screen():
                enemies.remove(enemy)
                score += 1
                if score % 5 == 0:
                    enemy_speed += 0.5

        # Draw player
        player.draw()

        # Score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (20, 20))

        pygame.display.update()

    game_over(score)


# ---------- GAME OVER ----------
def game_over(score):
    screen.fill(BLACK)
    text1 = font.render("GAME OVER", True, RED)
    text2 = font.render(f"Final Score: {score}", True, WHITE)
    text3 = font.render("Press ENTER to Restart", True, WHITE)

    screen.blit(text1, (WIDTH//2 - 80, HEIGHT//2 - 60))
    screen.blit(text2, (WIDTH//2 - 90, HEIGHT//2))
    screen.blit(text3, (WIDTH//2 - 150, HEIGHT//2 + 40))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game()


# ---------- START ----------
game()





