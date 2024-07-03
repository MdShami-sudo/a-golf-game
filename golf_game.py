import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quirky Mini Golf")

GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

ball_radius = 10
ball_pos = [100, 300]
ball_speed = [random.uniform(-2, 2), random.uniform(-2, 2)]
ball_acceleration = 0.5

hole_radius = 15
hole_pos = [700, 300]

obstacles = [
    {"pos": [400, 150], "size": [50, 50], "color": RED, "movement": "horizontal"},
    {"pos": [500, 400], "size": [70, 70], "color": BLUE, "movement": "vertical"},
    {"pos": [300, 250], "size": [60, 60], "color": YELLOW, "movement": "circular", "radius": 50, "angle": 0}
]

font = pygame.font.SysFont(None, 55)

def draw_ball(screen, pos):
    pygame.draw.circle(screen, WHITE, pos, ball_radius)

def draw_hole(screen, pos):
    pygame.draw.circle(screen, BLACK, pos, hole_radius)

def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        if obstacle["movement"] == "horizontal":
            obstacle["pos"][0] += random.choice([-1, 1])
            if obstacle["pos"][0] <= 0 or obstacle["pos"][0] >= WIDTH:
                obstacle["pos"][0] = WIDTH // 2
        elif obstacle["movement"] == "vertical":
            obstacle["pos"][1] += random.choice([-1, 1])
            if obstacle["pos"][1] <= 0 or obstacle["pos"][1] >= HEIGHT:
                obstacle["pos"][1] = HEIGHT // 2
        elif obstacle["movement"] == "circular":
            obstacle["angle"] += 0.05
            obstacle["pos"][0] = int(400 + obstacle["radius"] * math.cos(obstacle["angle"]))
            obstacle["pos"][1] = int(300 + obstacle["radius"] * math.sin(obstacle["angle"]))
        
        pygame.draw.rect(screen, obstacle["color"], (*obstacle["pos"], *obstacle["size"]))

def display_text(screen, text, color, pos):
    img = font.render(text, True, color)
    screen.blit(img, pos)

def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

running = True
dragging = False
start_pos = (0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
            dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                end_pos = event.pos
                ball_speed = [end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]]
                speed = math.hypot(ball_speed[0], ball_speed[1])
                if speed > 0:
                    ball_speed[0] = ball_speed[0] / speed * ball_acceleration
                    ball_speed[1] = ball_speed[1] / speed * ball_acceleration
                dragging = False

    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    ball_speed[0] *= 1
    ball_speed[1] *= 0.99

    if not dragging and random.random() < 0.01:
        ball_speed[0] = random.uniform(-2, 2)
        ball_speed[1] = random.uniform(-2, 2)

    if ball_pos[0] < ball_radius or ball_pos[0] > WIDTH - ball_radius:
        ball_speed[0] = -ball_speed[0]
    if ball_pos[1] < ball_radius or ball_pos[1] > HEIGHT - ball_radius:
        ball_speed[1] = -ball_speed[1]

    if calculate_distance(ball_pos, hole_pos) < hole_radius + ball_radius:
        display_text(screen, "You Win!", WHITE, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        ball_pos = [100, 300]
        ball_speed = [random.uniform(-2, 2), random.uniform(-2, 2)]

    screen.fill(GREEN)
    draw_hole(screen, hole_pos)
    draw_ball(screen, ball_pos)
    draw_obstacles(screen, obstacles)
    
    if dragging:
        pygame.draw.line(screen, WHITE, start_pos, pygame.mouse.get_pos(), 2)
    
    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
