import pygame, pickle, json, sys
import ui

pygame.init()
i = pygame.display.Info()
screen = pygame.display.set_mode((i.current_w - 100, i.current_h - 100), pygame.RESIZABLE)
pygame.display

while True:
    e = pygame.event.wait()
    if e.type == pygame.QUIT:
        sys.exit(0)
    elif e.type == pygame.WINDOWRESIZED:
        print(e)