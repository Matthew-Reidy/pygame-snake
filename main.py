# Example file showing a circle moving on screen
import pygame
import random
import math
# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

pygame.display.set_caption('My Game') 

dt = 0

COLLISION = pygame.USEREVENT + 1

DEFAULT_CIRCLE_RADIUS = 10

def main() -> None:

    running = True

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    rand_pos = RandPos()

    chain = []

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == COLLISION:
                rand_pos = RandPos()
                chain.append(pygame.Vector2(player_pos.x - 1, player_pos.y))

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        pygame.draw.circle(screen, "blue", rand_pos, DEFAULT_CIRCLE_RADIUS)
        pygame.draw.circle(screen, "red", player_pos, DEFAULT_CIRCLE_RADIUS)
        
        for cir in chain :
            pygame.draw.circle(screen, "red", cir, DEFAULT_CIRCLE_RADIUS)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        detectCircleCollision(rand_pos, player_pos)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000


    pygame.quit()


def RandPos() -> pygame.Vector2:

    pos_x = random.uniform(screen.get_width(), 0) 
    pos_y = random.uniform(0, screen.get_height())

    return pygame.Vector2(pos_x, pos_y)

def detectCircleCollision(rand_pos : pygame.Vector2, player_pos: pygame.Vector2) -> None:
    # distance between two coordinates on the grid
    inner = (rand_pos.x - player_pos.x)**2 + (rand_pos.y - player_pos.y)**2

    distance = math.sqrt(inner)

    if distance < DEFAULT_CIRCLE_RADIUS * 2:
        print("collision!")
        pygame.event.post(pygame.event.Event(COLLISION)) 


main()