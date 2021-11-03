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
                print(h)
                self.selected = h
                return(True)
            rpos += 2
            rpos += i.w
            h += 1
        return(False)