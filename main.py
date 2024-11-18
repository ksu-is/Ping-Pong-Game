import pygame, sys, random
 
pygame.init()
 
WIDTH, HEIGHT = 1280, 720
 
FONT = pygame.font.SysFont("Consolas", int(WIDTH/20))
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")
CLOCK = pygame.time.Clock()
 
#PADDLES

player = pygame.Rect(WIDTH-110, HEIGHT/2-50, 10, 100)
opponent = pygame.Rect(110, HEIGHT/2-50, 10, 100)

while True:
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_UP]:
        if player.top > 0:
            player.top -= 2
    if keys_pressed[pygame.K_DOWN]:
        if player.bottom < HEIGHT:
            player.bottom += 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    SCREEN.fill("black")

    pygame.draw.rect(SCREEN, "white", player)
    pygame.draw.rect(SCREEN, "white", opponent)


    pygame.display.update()
    CLOCK.tick(300)
