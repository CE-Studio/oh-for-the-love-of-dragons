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

rclickTitles = ("Dialouge/choice",
                "Set variables",
                "var == var (str)",
                "var == var (int)",
                "var == var (float)",
                "var == var (bool)",
                "var == var (inventory)",
                "var == value (str)",
                "var == value (int)",
                "var == value (float)",
                "var == value (bool)",
                "var == value (inventory)",
                "Day transition",
                "Scene transition",
                "Music transition")

rclickClasses = (ui.dialougeNode,
                 ui.setVarNode,             
                 ui.varVarStrNode,
                 ui.varVarIntNode,
                 ui.varVarFloatNode,
                 ui.varVarBoolNode,
                 ui.varVarInvNode,
                 ui.varValStrNode,
                 ui.varValIntNode,
                 ui.varValFloatNode,
                 ui.varValBoolNode,
                 ui.varValInvNode,
                 ui.dayNode,
                 ui.sceneNode,
                 ui.musicNode)

rclickMenu = ui.menu(rclickTitles)
rclick = False
rclickpos = (0, 0)

nodes = [ui.startNode((10, 10), 0)]

def draw():
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
        i.rend(screen, scrollpos, connecting)

    menu.rend(screen)

    if rclick:
        rclickMenu.rend(screen, rclickpos)

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
    ui.spos = scrollpos
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
            if rclick:
                rclick = False
                a = rclickMenu.click(rclickpos, e.pos)
                if not(a is False):
                    nodes.append(rclickClasses[a]((rclickpos[0] - scrollpos[0], rclickpos[1] - scrollpos[1]), len(nodes)))
            else:
                clickcheck(e)
        elif e.button == 2:
            rclick = False
            scroll = True
            scrolltrack = e.pos
            scrollhold = copy.copy(scrollpos)
        elif e.button == 3:
            rclick = True
            rclickpos = e.pos
    elif e.type == pygame.MOUSEBUTTONUP:
        if e.button == 2:
            rclick = False
            scroll = False
    elif e.type == pygame.KEYDOWN:
        if not(e.unicode == ""):
            for i in nodes:
                i.keypress(e.unicode)
        else:
            a = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
            if e.key in a:
                for i in nodes:
                    i.navpress(e.key)
    else:
        pass

    if scroll:
        i = pygame.mouse.get_pos()
        x = scrollhold[0] + (i[0] - scrolltrack[0])
        y = scrollhold[1] + (i[1] - scrolltrack[1])
        scrollpos = (x, y)

    draw()