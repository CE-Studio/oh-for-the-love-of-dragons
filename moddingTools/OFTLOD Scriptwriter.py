import pygame, pickle, json, sys

if sys.platform == "win32": #I hate that I need to do this to update the taskbar icon on Windows
    import ctypes           #...Fuck Windows
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("cestudio.OFTLODscrpitwriter")

pygame.init()
i = pygame.display.Info()
screen = pygame.display.set_mode((i.current_w - 100, i.current_h - 100), pygame.RESIZABLE)
pygame.display.set_icon(pygame.image.load("icon.png"))
pygame.display.set_caption("Scriptwriter")

import ui

menu = ui.menubar()
menu.rend(screen)
pygame.display.flip()

def clickcheck(e):
    menu.click(e.pos, e.button)

while True:
    e = pygame.event.wait()
    if e.type == pygame.QUIT:
        sys.exit(0)
    elif e.type == pygame.WINDOWRESIZED:
        size = [e.x, e.y]
        if size[0] < 300:
            size[0] = 300
        if size[1] < 300:
            size[1] = 300
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    elif e.type == pygame.MOUSEBUTTONDOWN:
        clickcheck(e)

    screen.fill((15, 15, 15))
    menu.rend(screen)
    pygame.display.flip()