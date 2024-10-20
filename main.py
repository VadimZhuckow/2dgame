import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 30
ENEMY_SIZE = 50
ENEMY_FALL_SPEED = 5
FPS = 30
NUM_ENEMIES = 5
BOSS_SIZE = 100
BOSS_HEALTH = 3

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bug Defender")

# Загрузка изображений
player_image = pygame.image.load('Preview_63.png')  # Изображение Боба
enemy_image = pygame.image.load('bug1_0.png')  # Изображение врага
boss_image = pygame.image.load('prew_2.png')  # Изображение босса

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
font = pygame.font.SysFont("Arial", 30)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        keys = pygame.key.get_pressed()

    # Управление игроком
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 10
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE:
        player_pos[0] += 10

    # Обновление врагов
    for enemy_pos in enemies:
        enemy_pos[1] += ENEMY_FALL_SPEED
        if enemy_pos[1] >= HEIGHT:
            enemy_pos[1] = random.randint(-100, -ENEMY_SIZE)
            enemy_pos[0] = random.randint(0, WIDTH - ENEMY_SIZE)
            score += 1  # Увеличиваем счет за избегание врагов

        # Проверка на столкновение с врагами
        if (enemy_pos[1] >= player_pos[1] and enemy_pos[1] < player_pos[1] + PLAYER_SIZE) and \
           (enemy_pos[0] >= player_pos[0] and enemy_pos[0] < player_pos[0] + PLAYER_SIZE):
            player_lives -= 1
            enemy_pos[1] = random.randint(-100, -ENEMY_SIZE)  # Перемещаем врага
            if player_lives <= 0:
                game_over = True

    # Проверка появления босса
    if score >= 10 and not boss_defeated:
        boss_pos[1] += 2  # Босс движется вниз
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
    screen.blit(player_image, (player_pos[0], player_pos[1]))  # Отрисовка игрока
    for enemy_pos in enemies:
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))  # Отрисовка врагов

    if not boss_defeated and score >= 10:
        screen.blit(boss_image, (boss_pos[0], boss_pos[1]))  # Отрисовка босса

    # Отображение счета и жизней
    score_text = font.render(f"Score: {score}", True, BLUE)
    lives_text = font.render(f"Lives: {player_lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
