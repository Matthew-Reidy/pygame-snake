# Example file showing a circle moving on screen
import pygame
import random
import math
# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

pygame.display.set_caption('Snake') 

dt = 0

COLLISION = pygame.USEREVENT + 1

DEFAULT_CIRCLE_RADIUS = 10

MOVEMENT_SPEED = 100

def main() -> None:

    running = True

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    rand_pos = RandPos(player_pos)

    pygame.key.set_repeat(500, 100) 

    chain = []

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == COLLISION:
                rand_pos = RandPos(player_pos)

                if len(chain) == 0:
                    chain.append(pygame.Vector2(player_pos.x , player_pos.y + 20))

                else:
                    chain.append(pygame.Vector2(chain[len(chain) - 1 ].x, chain[len(chain) - 1 ].y + 20))
                    print(chain)

        screen.fill("black")

        pygame.draw.circle(screen, "blue", rand_pos, DEFAULT_CIRCLE_RADIUS)
        pygame.draw.circle(screen, "red", player_pos, DEFAULT_CIRCLE_RADIUS)
        
        #this moves one snake body node each frame
        moveBody(chain)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:

            player_pos.y -= MOVEMENT_SPEED * dt

            if len(chain) != 0:
                chain[0].y = player_pos.y + 20
                chain[0].x = player_pos.x 

        if keys[pygame.K_s]:

            player_pos.y += MOVEMENT_SPEED * dt

        if keys[pygame.K_a]:

            player_pos.x -= MOVEMENT_SPEED * dt

            if len(chain) != 0:
                chain[0].y = player_pos.y 
                chain[0].x = player_pos.x + 20

        if keys[pygame.K_d]:

            player_pos.x += MOVEMENT_SPEED * dt

            if len(chain) != 0:
                chain[0].y = player_pos.y 
                chain[0].x = player_pos.x - 20

        detectCircleCollision(rand_pos, player_pos)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000


    pygame.quit()


def RandPos(player_pos : pygame.Vector2 ) -> pygame.Vector2:
    #produce X,Y coordinates until the coordinates are valid
    #valid coordinates are coordinates that do not match the snake head node
    invalidCoordinates = True
    while invalidCoordinates:

        pos_x = random.uniform(screen.get_width(), 0) 
        pos_y = random.uniform(0, screen.get_height())

        if pygame.Vector2(pos_x, pos_y) != player_pos :
            invalidCoordinates = False
            return pygame.Vector2(pos_x, pos_y)

def detectCircleCollision(rand_pos : pygame.Vector2, player_pos: pygame.Vector2) -> None:
    # distance between two coordinates on the grid
    inner = (rand_pos.x - player_pos.x)**2 + (rand_pos.y - player_pos.y)**2

    distance = math.sqrt(inner)

    if distance <= DEFAULT_CIRCLE_RADIUS * 2:
        pygame.event.post(pygame.event.Event(COLLISION)) 


def moveBody(chain) -> None:
    for vec in chain :
        pygame.draw.circle(screen, "red", vec, DEFAULT_CIRCLE_RADIUS)

def gameCounter(chain) -> None:
    #keeps track of how much snake food has been eaten 
    #and increases movement speed with each bite taken
    pass

main()