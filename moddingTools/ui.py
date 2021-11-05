import pygame

textfont = pygame.font.Font("OpenSans-Regular.ttf", 14)

class text():
    def __init__(self, text, color = (255, 255, 255), callback = None):
        self.text = text
        self.w, self.h = textfont.size(text)
        self.color = color
        self.callback = callback

    def rend(self, surface, pos):
        surface.blit(textfont.render(self.text, True, self.color), pos)

    def click(self, pos, cpos):
        if ((cpos[0] >= pos[0]) and
            (cpos[1] >= pos[1]) and
            (cpos[0] <= (pos[0] + self.w)) and
            (cpos[1] <= (pos[1] + self.h))):
            if (type(self.callback) == type(None)):
                return(True)
            else:
                return(self.callback(cpos))
        else:
            return(False)

class button():
    def __init__(self, label, bcol = (120, 120, 120), fcol = (255, 255, 255), scol = (95, 159, 172), callback = None):
        self.label = text(label, fcol, callback)
        self.bcol = bcol
        self.scol = scol
        self.w, self.h = self.label.w, self.label.h

    def rend(self, surface, pos, selected = False):
        i = pygame.Rect(pos, (self.w, self.h))
        if selected:
            h = self.scol
        else:
            h = self.bcol
        pygame.draw.rect(surface, h, i)
        self.label.rend(surface, pos)

    def click(self, pos, cpos):
        return(self.label.click(pos, cpos))

class buttonGang():
    def __init__(self, options, bcol = (120, 120, 120), fcol = (255, 255, 255), scol = (95, 159, 172), default = 0):
        self.options = []
        for i in options:
            self.options.append(button(i, bcol, fcol, scol))
        self.selected = default
        self.w, self.h = 0, 0
        for i in self.options:
            self.w += 2
            self.w += i.w
            if i.h > self.h:
                self.h = i.h

    def rend(self, surface, pos):
        rpos = 0
        h = 0
        for i in self.options:
            i.rend(surface, (rpos + pos[0], pos[1]), h == self.selected)
            rpos += 2
            rpos += i.w
            h += 1

    def click(self, pos, cpos):
        h = 0
        rpos = 0
        for i in self.options:
            if i.click((rpos + pos[0], pos[1]), cpos):
                self.selected = h
                return(True)
            rpos += 2
            rpos += i.w
            h += 1
        return(False)

class menu():
    def __init__(self, options, bcol = (120, 120, 120), fcol = (255, 255, 255)):
        self.labels = []
        self.bcol = bcol
        self.h = 0
        self.w = 0
        for i in options:
            self.labels.append(text(i, fcol))
            self.w = max(self.w, self.labels[-1].w)
            self.h += self.labels[-1].h

    def rend(self, surface, pos):
        i = pygame.Rect(pos, (self.w, self.h))
        pygame.draw.rect(surface, self.bcol, i)
        h = 0
        for i in self.labels:
            i.rend(surface, (pos[0], h + pos[1]))
            h += i.h

class menubar():
    def __init__(self):
        self.menubutton = button("File") 
        self.modeswitch = buttonGang(("Node Graph", "Playtest"))
        self.h = self.menubutton.h
        self.menu = menu(("New", "Save", "Save As", "Complie and Export"))
        self.showmenu = False

    def rend(self, surface):
        i = pygame.display.Info()
        h = pygame.Rect((0, 0), (i.current_w, self.h))
        pygame.draw.rect(surface, (180, 180, 180), h)
        self.menubutton.rend(surface, (2, 0))
        self.modeswitch.rend(surface, (i.current_w - self.modeswitch.w, 0))
        if self.showmenu:
            self.menu.rend(surface, (2, self.h + 2))

    def click(self, pos, button):
        if button == 1:
            if self.showmenu:
                self.showmenu = False
                return(True)
            else:
                if self.menubutton.click((2, 0), pos):
                    self.showmenu = True
                    return(True)
                else:
                    i = pygame.display.Info()
                    return(self.modeswitch.click((i.current_w - self.modeswitch.w, 0), pos))
        return(False)

class socket():
    def __init__(self, input, col = (200, 200, 200), bcol=(200, 200, 200)):
        self.input = input
        self.col = col
        self.bcol = bcol

    def rend(self, surface, pos):
        if self.input:
            p = (pos, (-14 + pos[0], pos[1]),
                 (-14 + pos[0], 4 + pos[1]), (-4 + pos[0], 4 + pos[1]),
                 (-4 + pos[0], 10 + pos[1]), (-14 + pos[0], 10 + pos[1]),
                 (-14 + pos[0], 14 + pos[1]), (pos[0], 14 + pos[1]))
        else:
            p = (pos, (14 + pos[0], pos[1]),
                 (14 + pos[0], 4 + pos[1]), (4 + pos[0], 4 + pos[1]),
                 (4 + pos[0], 10 + pos[1]), (14 + pos[0], 10 + pos[1]),
                 (14 + pos[0], 14 + pos[1]), (pos[0], 14 + pos[1]))
        pygame.draw.polygon(surface, self.col, p)
        pygame.draw.polygon(surface, self.bcol, p, 1)

class output():
    def __init__(self, text, color = (255, 255, 255)):
        self.text = text
        self.w, self.h = textfont.size(text)
        self.w += 4
        self.h += 1
        self.color = color
        self.socket = socket(False)

    def rend(self, surface, pos):
        surface.blit(textfont.render(self.text, True, self.color), (pos[0] + 2, pos[1]))
        self.socket.rend(surface, (pos[0] + self.w, pos[1] + 3))

class node():
    def __init__(self, pos):
        self.parts = []
        self.connections = []
        self.w, self.h = (0, 0)
        self.bgcol = (60, 60, 60)
        self.populate()
        self.update()
        self.pos = pos

    def populate(self):
        pass

    def addPart(self, part):
        part.parent = self
        self.parts.append(part)
        self.w = max(self.w, part.w)
        self.h += part.h

    def update(self):
        for i in self.parts:
            i.w = self.w

    def rend(self, surface, scrollpos):
        rp = (scrollpos[0] + self.pos[0], scrollpos[1] + self.pos[1])
        r = pygame.Rect(rp, (self.w, self.h))
        pygame.draw.rect(surface, self.bgcol, r)
        h = 0
        for i in self.parts:
            i.rend(surface, (rp[0], rp[1] + h))
            h += i.h

class startNode(node):
    def populate(self):
        self.bgcol = (60, 100, 60)
        #self.addPart(text(""))
        self.addPart(output("Start"))
        #self.addPart(text(""))