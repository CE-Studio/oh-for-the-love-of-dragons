import pygame, pickle, json, sys

pygame.init()
i = pygame.display.Info()
screen = pygame.display.set_mode((i.current_w - 100, i.current_h - 100), pygame.RESIZABLE)

import ui

test = ui.buttonGang(["this be test", "Also test", "AAAAAAAAA"])
test.rend(screen, (10, 10))
pygame.display.flip()

while True:
    e = pygame.event.wait()
    if e.type == pygame.QUIT:
        sys.exit(0)
    elif e.type == pygame.WINDOWRESIZED:
        print(e)
    elif e.type == pygame.MOUSEBUTTONDOWN:
        print(e)
        test.click((10, 10), e.pos)

    test.rend(screen, (10, 10))
    pygame.display.flip()