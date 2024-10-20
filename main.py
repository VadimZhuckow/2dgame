import pygame
import random


pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 50
ENEMY_FALL_SPEED = 5
FPS = 30
NUM_ENEMIES = 10
BOSS_SIZE = 100
BOSS_HEALTH = 3

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Action Game")

# Игрок
player_pos = [WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE]
player_lives = 3
score = 0

# Враги
enemies = [[random.randint(0, WIDTH - ENEMY_SIZE), random.randint(-HEIGHT, 0)] for _ in range(NUM_ENEMIES)]

# Босс
boss_pos = [WIDTH // 2 - BOSS_SIZE // 2, -BOSS_SIZE]
boss_health = BOSS_HEALTH
boss_defeated = False

# Игровой цикл
clock = pygame.time.Clock()
game_over = False

# Шрифт для текста
font = pygame.font.SysFont("Arial", 30)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Получение состояния клавиш
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 10
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE:
        player_pos[0] += 10

    # Обновление врагов
    for enemy_pos in enemies:
        enemy_pos[1] += ENEMY_FALL_SPEED

        if (enemy_pos[1] >= player_pos[1] and enemy_pos[1] < player_pos[1] + PLAYER_SIZE) and \
           (enemy_pos[0] >= player_pos[0] and enemy_pos[0] < player_pos[0] + PLAYER_SIZE):
            player_lives -= 1
            enemy_pos[1] = random.randint(-100, -ENEMY_SIZE)
            enemy_pos[0] = random.randint(0, WIDTH - ENEMY_SIZE)
            if player_lives <= 0:
                game_over = True
                # Если враг выходит за пределы экрана, создаем нового
        if enemy_pos[1] > HEIGHT:
                    enemy_pos[1] = random.randint(-100, -ENEMY_SIZE)
                    enemy_pos[0] = random.randint(0, WIDTH - ENEMY_SIZE)
                    score += 1


    if score >= 10 and not boss_defeated:
        boss_pos[1] += 2


        if (boss_pos[1] >= player_pos[1] and boss_pos[1] < player_pos[1] + PLAYER_SIZE) and \
           (boss_pos[0] >= player_pos[0] and boss_pos[0] < player_pos[0] + PLAYER_SIZE):
            player_lives -= 1
            if player_lives <= 0:
                game_over = True

        # Если босс выходит за пределы экрана, он возвращается
        if boss_pos[1] > HEIGHT:
            boss_pos[1] = -BOSS_SIZE

    # Отрисовка
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))
    for enemy_pos in enemies:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], ENEMY_SIZE, ENEMY_SIZE))

    if not boss_defeated and score >= 10:
        pygame.draw.rect(screen, GREEN, (boss_pos[0], boss_pos[1], BOSS_SIZE, BOSS_SIZE))

    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
