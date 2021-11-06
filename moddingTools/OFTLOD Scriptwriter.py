import pygame, pickle, json, sys, copy
def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))

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

scrollpos = (100, 100)
scroll = False
scrolltrack = ()
scrollhold = (100, 100)
connecting = False
connector = False

nodes = [ui.startNode((10, 10), 0), ui.testNode((200, 50), 1), ui.testNode((200, 10), 2)]

def draw():
    ui.spos = scrollpos
    a = pygame.display.Info()
    screen.fill((15, 15, 15))
    pygame.draw.line(screen, (255, 0, 0), (scrollpos[0], 0), (scrollpos[0], a.current_h))
    pygame.draw.line(screen, (0, 0, 255), (0, scrollpos[1]), (a.current_w, scrollpos[1]))
    tx = ui.textfont.render(str(scrollpos[0]), True, (255, 100, 100))
    txw = ui.textfont.size(str(scrollpos[0]))[0] + 2
    ty = ui.textfont.render(str(scrollpos[1]), True, (100, 100, 255))
    screen.blit(tx, (clamp(scrollpos[0] + 2, 2, a.current_w - txw), 19))
    screen.blit(ty, (2, clamp(scrollpos[1] + 2, 32, a.current_h - 19)))

    for i in nodes:
        i.rend(screen, scrollpos)

    menu.rend(screen)
    pygame.display.flip()

def clickcheck(e):
    global connecting
    global connector
    if menu.click(e.pos, e.button):
        return
    if connecting:
        for i in nodes:
            h = i.click(e.pos, True, scrollpos)
            if h == True:
                return
            if h == False:
                pass
            else:
                connector.connectTo = h
                connecting = False
                return
        connecting = False
    else:
        for i in nodes:
            h = i.click(e.pos, False, scrollpos)
            if h == True:
                return
            if h == False:
                pass
            else:
                connecting = True
                connector = h
                return

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
        if e.button == 1:
            clickcheck(e)
        elif e.button == 2:
            scroll = True
            scrolltrack = e.pos
            scrollhold = copy.copy(scrollpos)
    elif e.type == pygame.MOUSEBUTTONUP:
        if e.button == 2:
            scroll = False
    else:
        pass

    if scroll:
        i = pygame.mouse.get_pos()
        x = scrollhold[0] + (i[0] - scrolltrack[0])
        y = scrollhold[1] + (i[1] - scrolltrack[1])
        scrollpos = (x, y)

    draw()