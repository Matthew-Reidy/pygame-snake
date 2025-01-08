import pygame
import random
import math
# pygame setup
pygame.init()


screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

pygame.display.set_caption('Snake') 


COLLISION = pygame.USEREVENT + 1

LOSE_CONDITION = pygame.USEREVENT + 2

WIN_CONDITION = pygame.USEREVENT + 3

DEFAULT_CIRCLE_RADIUS = 10

MOVEMENT_SPEED= 20

def main() -> None:

    running = True

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    
    player_prev_pos = pygame.Vector2(player_pos)

    font = pygame.font.SysFont("Arial", 25)

    rand_pos = RandPos(player_pos)

    movement_direction = pygame.K_w

    chain = []

    while running:
        
        screen.fill("black")

        gameCounter(chain, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == COLLISION:

                rand_pos = RandPos(player_pos)

                if len(chain) == 0:
                    # First body segment starts at the player's previous position
                    chain.append({
                        "current_position": pygame.Vector2(player_prev_pos),
                        "previous_position":pygame.Vector2(player_prev_pos),
                        "color": "red"
                    })
                else:
                    # Additional segments follow the last segment's previous position
                    color = ""

                    if len(chain) % 2 == 0:
                        color = "red"
                    else:
                        color = "green"

                    last_segment = chain[-1]
                    chain.append({
                        "current_position": pygame.Vector2(last_segment["previous_position"]),
                        "previous_position": pygame.Vector2(last_segment["previous_position"]),
                        "color": color
                    })

            if event.type == LOSE_CONDITION:

                label = font.render(f"YOU LOSE!", 1, (255,255,225))
                screen.blit(label, (screen.get_width() / 2, screen.get_height() / 2))

                running = False

            if event.type == WIN_CONDITION:
                
                label = font.render(f"YOU WIN!", 1, (255,255,225))
                screen.blit(label, (screen.get_width() / 2, screen.get_height() / 2))

                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    movement_direction = event.key
                    

        #food node
        pygame.draw.circle(screen, "blue", rand_pos, DEFAULT_CIRCLE_RADIUS)
        #body head node
        pygame.draw.circle(screen, "red", player_pos, DEFAULT_CIRCLE_RADIUS)
        
        moveBody(chain, player_prev_pos)

        if movement_direction == pygame.K_w:

            player_pos.y -= MOVEMENT_SPEED

        if movement_direction == pygame.K_s:

            player_pos.y += MOVEMENT_SPEED

        if movement_direction == pygame.K_a:

            player_pos.x -= MOVEMENT_SPEED

        if movement_direction == pygame.K_d:

            player_pos.x += MOVEMENT_SPEED

        if detectCircleCollision(rand_pos, player_pos):
            pygame.event.post(pygame.event.Event(COLLISION)) 

        player_prev_pos = pygame.Vector2(player_pos)
        
        pygame.display.flip()

        clock.tick(10)


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

def detectCircleCollision(rand_pos : pygame.Vector2, player_pos: pygame.Vector2) -> bool:

    # distance between two coordinates on the grid
    inner = (rand_pos.x - player_pos.x)**2 + (rand_pos.y - player_pos.y)**2

    distance = math.sqrt(inner)

    if distance < DEFAULT_CIRCLE_RADIUS * 2:
        return True
    
    return False

def moveBody(chain, player_prev_pos) -> None:

    if len(chain) > 0:

        first_segment = chain[0]
        first_segment_prev_pos = first_segment["current_position"]
        first_segment["previous_position"] = first_segment_prev_pos
        first_segment["current_position"] = pygame.Vector2(player_prev_pos)

        for i in range(1, len(chain)):

            current_segment = chain[i]
            prev_segment = chain[i - 1]
            current_segment_prev_pos = current_segment["current_position"]
            current_segment["previous_position"] = current_segment_prev_pos
            current_segment["current_position"] = prev_segment["previous_position"]

    for segment in chain:
        if detectCircleCollision(segment["current_position"], player_prev_pos):
            pygame.event.post(pygame.event.Event(LOSE_CONDITION)) 
            
        
        pygame.draw.circle(screen, segment["color"], segment["current_position"], DEFAULT_CIRCLE_RADIUS)
    

def gameCounter(chain, font) -> None:
    
    score = len(chain) 
    label = font.render(f"Current score : {score}", 1, (255,255,225))
    screen.blit(label, (50,50))

    if score == 100:
        pygame.event.post(pygame.event.Event(WIN_CONDITION))
    
if __name__ == "__main__":
    main()