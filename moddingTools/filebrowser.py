import pygame, os

font = pygame.font.Font("OpenSans-Regular.ttf", 16)
screen = pygame.display.get_surface()
listSurf = pygame.Surface((100, 100))

def __draw__():
    screen.fill((200, 200, 200))
    listSurf.fill((100, 100, 100))
    screen.blit(listSurf, (135, 60))
    pygame.display.flip()

def browse(startpath = "."):
    global screen
    global listSurf

    print(os.listdir())

    screen = pygame.display.get_surface()

    h = pygame.display.get_window_size()
    listSurf = pygame.Surface((h[0] - 155, h[1] - 120))

    __draw__()

    while True:
        e = pygame.event.wait()

        if e.type == pygame.QUIT:
            return(None)
        elif e.type == pygame.WINDOWRESIZED:
            size = [e.x, e.y]
            if size[0] < 300:
                size[0] = 300
            if size[1] < 300:
                size[1] = 300
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            listSurf = pygame.Surface((size[0] - 155, size[1] - 120))

        __draw__()