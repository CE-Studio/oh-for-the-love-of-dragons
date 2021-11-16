import pygame, os

font = pygame.font.Font("OpenSans-Regular.ttf", 16)
screen = pygame.display.get_surface()
listSurf = pygame.Surface((100, 100))
itemlist = []
curdir = "./"

dico = pygame.image.load("fbico/derg.png")
fico = pygame.image.load("fbico/folder.png")
jico = pygame.image.load("fbico/json.png")
oico = pygame.image.load("fbico/other.png")

class listitem():
    def __init__(self, file):
        self.sel = False
        self.file = file
        self.h = font.size(self.file)[1]
        if os.path.isdir(curdir + file):
            self.type = "dir"
            self.file += "/"
        else:
            self.type = file.split(".")[-1]

    def rend(self, surface, pos):
        if self.sel:
            r = pygame.Rect(pos, (surface.get_size()[0] - 4, self.h))
            pygame.draw.rect(surface, (50, 50, 255), r)

        if self.type == "dir":
            surface.blit(fico, pos)
        elif self.type == "derg":
            surface.blit(dico, pos)
        elif self.type == "json":
            surface.blit(jico, pos)
        else:
            surface.blit(oico, pos)
        surface.blit(font.render(self.file, True, (0, 0, 0)), (pos[0] + 18, pos[1] - 3))

    def click(self, pos, cpos):
        w = listSurf.get_size()[0] - 4
        if ((cpos[0] >= pos[0]) and
            (cpos[1] >= pos[1]) and
            (cpos[0] <= (pos[0] + w)) and
            (cpos[1] <= (pos[1] + self.h))):
            if self.sel:
                pass
            else:
                self.sel = True
        else:
            self.sel = False

def __draw__():
    screen.fill((200, 200, 200))
    listSurf.fill((255, 255, 255))

    h = 2
    for i in itemlist:
        i.rend(listSurf, (2, h))
        h += i.h

    screen.blit(listSurf, (135, 60))
    pygame.display.flip()

def __nav__(dir):
    global itemlist
    global curdir
    curdir = dir
    itemlist = []
    for i in ([".", ".."] + os.listdir(dir)):
        itemlist.append(listitem(i))

def browse(startpath = "./"):
    global screen
    global listSurf

    __nav__(startpath)

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