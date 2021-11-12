import pygame, weakref, json, gc

textfont = pygame.font.Font("OpenSans-Regular.ttf", 14)

class text():
    def __init__(self, text, color = (255, 255, 255), callback = None):
        self.text = str(text)
        self.w, self.h = textfont.size(self.text)
        self.color = color
        self.callback = callback

    def update(self):
        self.w, self.h = textfont.size(self.text)

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

    def keypress(self, inp):
        pass

    def compile(self, d):
        pass

class button():
    def __init__(self, label, bcol = (120, 120, 120), fcol = (255, 255, 255), scol = (95, 159, 172), callback = None):
        self.label = text(label, fcol, callback)
        self.bcol = bcol
        self.scol = scol
        self.w, self.h = self.label.w, self.label.h

    def update(self):
        self.label.update()
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

    def keypress(self, inp):
        pass

    def compile(self, d):
        pass

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

    def compile(self, d):
        pass

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

    def click(self, pos, cpos):
        h = 0
        j = 0
        for i in self.labels:
            if i.click((pos[0], pos[1] + h), cpos):
                return(j)
            h += i.h
            j += 1
        return(False)

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
                return(self.menu.click((2, self.h + 2), pos))
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
    def __init__(self, text, obj, obj2 = "nextType", color = (255, 255, 255)):
        self.text = text
        self.obj = obj
        self.obj2 = obj2
        self.w, self.h = textfont.size(self.text)
        self.w += 4
        self.h += 1
        self.color = color
        self.socket = socket(False)
        self.connectTo = False

    def update(self):
        self.w, self.h = textfont.size(self.text)
        self.w += 4
        self.h += 1
        if not (self.connectTo == False):
            if self.connectTo() == None:
                self.connectTo = False

    def rend(self, surface, pos):
        surface.blit(textfont.render(self.text, True, self.color), (pos[0] + 2, pos[1]))
        self.socket.rend(surface, (pos[0] + self.w, pos[1] + 3))
        if not(self.connectTo == False):
            i = self.connectTo()
            pygame.draw.line(surface, (0, 255, 0), (pos[0] + self.w + 7, pos[1] + 11), (i.pos[0] + spos[0] - 7, i.pos[1] + spos[1] + 11))

    def click(self, pos, cpos):
        pos = (pos[0] + self.w, pos[1] + 3)
        if ((cpos[0] >= pos[0]) and
            (cpos[1] >= pos[1]) and
            (cpos[0] <= (pos[0] + 14)) and
            (cpos[1] <= (pos[1] + 14))):
            if self.connectTo == False:
                return("con")
            else:
                self.connectTo = False
                return(True)
        return(False)

    def keypress(self, inp):
        pass

    def compile(self, d):
        if self.connectTo == False:
            d[str(self.obj)] = "END"
            d[str(self.obj2)] = "END"
        else:
            d[str(self.obj)] = str(self.connectTo().id)
            d[str(self.obj2)] = str(self.connectTo().type)

class textBox():
    def __init__(self, label, obj, col = (255, 255, 255), bcol = (100, 100, 100), fcol = (255, 255, 255), scol = (60, 120, 120)):
        self.label = text(label, col)
        self.initcon()
        self.text = text(self.content, fcol)
        self.obj = obj
        self.h = self.label.h
        self.w = self.label.w + max(50, self.text.w) + 5
        self.bcol = bcol
        self.fcol = fcol
        self.scol = scol
        self.hlight = False
        self.conthold = ""
    
    def initcon(self):
        self.content = ""

    def sanitize(self, inp):
        return(str(inp))

    def update(self):
        self.label.update()
        self.text.update()
        self.h = self.label.h
        self.w = self.label.w + max(50, self.text.w) + 5

    def rend(self, surface, pos):
        self.label.rend(surface, pos)
        r = pygame.Rect((pos[0] + self.label.w + 5, pos[1]), (self.w - self.label.w - 5, self.h))
        if self.hlight:
            pygame.draw.rect(surface, self.scol, r)
        else:
            pygame.draw.rect(surface, self.bcol, r)
        self.text.rend(surface, (pos[0] + self.label.w + 5, pos[1]))

    def click(self, pos, cpos):
        ht = bool(self.hlight)
        self.hlight = ((cpos[0] >= pos[0]) and
                       (cpos[1] >= pos[1]) and
                       (cpos[0] <= (pos[0] + self.w)) and
                       (cpos[1] <= (pos[1] + self.h)))
        if not(ht == self.hlight):
            if self.hlight:
                self.conthold = str(self.content)
                self.text.text = self.conthold + "|"
            else:
                self.content = self.sanitize(self.conthold)
                self.text.text = str(self.content)
        return(self.hlight)

    def keypress(self, key):
        if self.hlight:
            if key == "\b":
                self.conthold = self.conthold[:-1]
                self.text.text = self.conthold + "|"
            elif key == "\r":
                pass
            else:
                self.conthold += key
                self.text.text = self.conthold + "|"

    def compile(self, d):
        d[str(self.obj)] = self.content

class floatBox(textBox):
    def initcon(self):
        self.content = 0.0

    def sanitize(self, inp):
        try:
            return(float(inp))
        except:
            return(self.content)

class intBox(textBox):
    def initcon(self):
        self.content = 0

    def sanitize(self, inp):
        try:
            return(int(inp))
        except:
            return(self.content)

class boolBox(textBox):
    def initcon(self):
        self.content = True

    def sanitize(self, inp):
        inp = inp.lower()
        if inp in ("true", "tru", "tr", "t", "yes", "ye", "y", "1"):
            return(True)
        elif inp in ("false", "fals", "fal", "fa", "f", "no", "n", "0"):
            return(False)
        else:
            return(self.content)

class textList():
    def __init__(self, label, obj, col = (255, 255, 255), bcol = (100, 100, 100), fcol = (255, 255, 255), scol = (60, 120, 120)):
        self.col = col
        self.label = text(label, col)
        self.items = []
        self.obj = obj
        self.h = self.label.h
        self.w = self.label.w + 2 + self.label.h
        self.bcol = bcol
        self.fcol = fcol
        self.scol = scol
        self.hlight = False
        self.conthold = ""

    def getblank(self):
        return(textBox("", ""))

    def click(self, pos, cpos):
        h = self.label.h + 1
        j = False
        if ((cpos[0] >= pos[0] + (self.w - self.label.h)) and
            (cpos[1] >= pos[1]) and
            (cpos[0] <= (pos[0] + self.w)) and
            (cpos[1] <= (pos[1] + self.label.h))):
            j = True
            self.items.append(self.getblank())
        else:
            for i in self.items:
                if i.click((pos[0], pos[1] + h), cpos):
                    j = True
                h += (i.h + 1)
        return(j)

    def keypress(self, key):
        h = 1
        for i in self.items:
            if i.hlight:
                if key == "\r":
                    self.items.insert(h, self.getblank())
                elif key == "": #There's a character for "delete" in this string but VS isn't rendering it
                    self.items.remove(i)
                elif (i.content == "") and (key == "\b"):
                    self.items.remove(i)
                else:
                    i.keypress(key)
            h += 1

    def update(self):
        self.w = self.label.w + 2 + self.label.h
        self.h = self.label.h
        for i in self.items:
            i.update()
            self.h += (i.h + 1)
            self.w = max(self.w, i.w)

    def rend(self, surface, pos):
        self.label.rend(surface, pos)
        ppos = ((pos[0] + self.w) - self.label.h, pos[1])
        r = pygame.Rect(ppos, (self.label.h, self.label.h))
        pygame.draw.rect(surface, self.bcol, r)
        pygame.draw.line(surface, self.col, (ppos[0] + round(self.label.h / 2) - 1, ppos[1] + 2), (ppos[0] + round(self.label.h / 2) - 1, ppos[1] - 3 + self.label.h), 2)
        pygame.draw.line(surface, self.col, (ppos[0] + 2, ppos[1] + round(self.label.h / 2) - 1), (ppos[0] - 3 + self.label.h, ppos[1] + round(self.label.h / 2) - 1), 2)
        h = self.label.h + 1
        for i in self.items:
            i.rend(surface, (pos[0], pos[1] + h))
            h += (i.h + 1)

    def compile(self, d):
        h = []
        for i in self.items:
            h.append(i.content)
        d[str(self.obj)] = h

class boolList(textList):
    def getblank(self):
        return(boolBox("", ""))

class node():
    def __init__(self, pos, id):
        self.type = "default"
        self.id = id
        self.connectable = True
        self.deleteable = True 
        self.parts = []
        self.connections = []
        self.w, self.h = (0, 0)
        self.bgcol = (60, 60, 60)
        self.ccol = (20, 70, 70)
        self.populate()
        self.update()
        self.pos = pos
        self.socket = socket(True)

    def populate(self):
        pass

    def addPart(self, part):
        self.parts.append(part)
        self.w = max(self.w, part.w)
        self.h += (part.h + 1)

    def update(self):
        self.w = 0
        self.h = 0
        for i in self.parts:
            i.update()
            self.w = max(self.w, i.w)
            self.h += (i.h + 1)
        for i in self.parts:
            i.w = self.w

    def rend(self, surface, scrollpos, con):
        self.update()
        rp = (scrollpos[0] + self.pos[0], scrollpos[1] + self.pos[1])
        r = pygame.Rect(rp, (self.w, self.h))
        if self.connectable and con:
            pygame.draw.rect(surface, self.ccol, r)
        else:
            pygame.draw.rect(surface, self.bgcol, r)
        if self.deleteable:
            r = pygame.Rect((rp[0], rp[1] - 14), (14, 14))
            pygame.draw.rect(surface, (255, 0, 0), r)
        h = 0
        for i in self.parts:
            i.rend(surface, (rp[0], rp[1] + h))
            h += (i.h + 1)
        if self.connectable:
            self.socket.rend(surface, (rp[0], rp[1] + 3))

    def click(self, cpos, con, spos):
        t = False
        if ((cpos[0] >= (self.pos[0] + spos[0] - 14)) and
            (cpos[1] >= (self.pos[1] + spos[1] - 14)) and
            (cpos[0] <= ((self.pos[0] + spos[0]) + self.w + 14)) and
            (cpos[1] <= ((self.pos[1] + spos[1]) + self.h))):
            if con:
                if self.connectable:
                    return(weakref.ref(self))
                else:
                    return(False)
            else:
                if self.deleteable and ((cpos[0] >= (self.pos[0] + spos[0])) and
                                        (cpos[1] >= (self.pos[1] + spos[1] - 14)) and
                                        (cpos[0] <= ((self.pos[0] + spos[0]) + 14)) and
                                        (cpos[1] <= (self.pos[1] + spos[1]))):
                    del(self.parts)
                    #h = gc.get_referrers(self)
                    #for i in h:
                    #    print(type(i))
                    return("del")
                j = 0
                for i in self.parts:
                    h = i.click((self.pos[0] + spos[0], self.pos[1] + spos[1] + j), cpos)
                    if h == "con":
                        return(i)
                    elif h:
                        t = True
                    else:
                        pass
                    j += (i.h + 1)
        return(t)

    def keypress(self, inp):
        cpos = pygame.mouse.get_pos()
        if ((cpos[0] >= (self.pos[0] + spos[0])) and
            (cpos[1] >= (self.pos[1] + spos[1])) and
            (cpos[0] <= ((self.pos[0] + spos[0]) + self.w + 14)) and
            (cpos[1] <= ((self.pos[1] + spos[1]) + self.h))):
            for i in self.parts:
                i.keypress(inp)

    def navpress(self, inp):
        cpos = pygame.mouse.get_pos()
        if ((cpos[0] >= (self.pos[0] + spos[0])) and
            (cpos[1] >= (self.pos[1] + spos[1])) and
            (cpos[0] <= ((self.pos[0] + spos[0]) + self.w + 14)) and
            (cpos[1] <= ((self.pos[1] + spos[1]) + self.h))):
            if inp == pygame.K_LEFT:
                self.pos = (self.pos[0] - 10, self.pos[1])
            elif inp == pygame.K_RIGHT:
                self.pos = (self.pos[0] + 10, self.pos[1])
            elif inp == pygame.K_UP:
                self.pos = (self.pos[0], self.pos[1] - 10)
            elif inp == pygame.K_DOWN:
                self.pos = (self.pos[0], self.pos[1] + 10)

    def compile(self):
        data = {}
        for i in self.parts:
            i.compile(data)
        print(json.dumps(data))

class startNode(node):
    def populate(self):
        self.type = "start"
        self.connectable = False
        self.deleteable = False
        self.bgcol = (60, 100, 60)
        self.addPart(text(""))
        self.addPart(output("     Start     ", "default"))
        self.addPart(text(""))

class dialogueNode(node):
    def populate(self):
        self.type = "dia"
        self.addPart(text("Dialogue/choice"))
        self.addPart(textBox("Character", "character"))
        self.addPart(textBox("Animation", "animation"))
        self.addPart(floatBox("Timeout", "timeout"))
        self.addPart(textList("dialogue", "dialogue"))
        self.addPart(textBox("Question", "question"))
        self.addPart(textBox("Answer A", "option1"))
        self.addPart(textBox("Answer B", "option2"))
        self.addPart(textBox("Answer C", "option3"))
        self.addPart(textBox("Answer D", "option4"))
        self.addPart(output("Option A", "target1", "nextType1"))
        self.addPart(output("Option B", "target2", "nextType2"))
        self.addPart(output("Option C", "target3", "nextType3"))
        self.addPart(output("Option D", "target4", "nextType4"))
        self.addPart(output("Timeout target", "targetDefault"))

class setVarNode(node):
    def populate(self):
        self.type = "setvar"
        self.addPart(text("Set Variables"))
        self.addPart(text(""))
        self.addPart(intBox("Str variable ID", "strID"))
        self.addPart(textBox("Value", "strValue"))
        self.addPart(text(""))
        self.addPart(intBox("Int variable ID", "intID"))
        self.addPart(intBox("Value", "intValue"))
        self.addPart(text(""))
        self.addPart(intBox("Float variable ID", "floatID"))
        self.addPart(floatBox("Value", "floatValue"))
        self.addPart(text(""))
        self.addPart(intBox("Bool variable ID", "boolID"))
        self.addPart(boolBox("Value", "boolValue"))
        self.addPart(text(""))
        self.addPart(intBox("Inventory slot ID", "inventorySlot"))
        self.addPart(textBox("Item", "itemName"))
        self.addPart(text(""))
        self.addPart(output("Target", "targetDefault"))

class varVarStrNode(node):
    def populate(self):
        self.type = "varvarstr"
        self.addPart(text("Var1 == Var2 (Str)"))
        self.addPart(intBox("Str variable ID 1", "var1id"))
        self.addPart(intBox("Str variable ID 2", "var2id"))
        self.addPart(output("True", "target1", "nextType1"))
        self.addPart(output("True", "target2", "nextType2"))

class varVarIntNode(node):
    def populate(self):
        self.type = "varvarint"
        self.addPart(text("Var1 == Var2 (Int)"))
        self.addPart(intBox("Int variable ID 1", "var1id"))
        self.addPart(intBox("Int variable ID 2", "var2id"))
        self.addPart(output("True", "target1", "nextType1"))
        self.addPart(output("True", "target2", "nextType2"))

class varVarFloatNode(node):
    def populate(self):
        self.type = "varvarflt"
        self.addPart(text("Var1 == Var2 (Float)"))
        self.addPart(intBox("Float variable ID 1", "var1id"))
        self.addPart(intBox("Float variable ID 2", "var2id"))
        self.addPart(output("True", "target1", "nextType1"))
        self.addPart(output("True", "target2", "nextType2"))

class varVarBoolNode(node):
    def populate(self):
        self.type = "varvarbol"
        self.addPart(text("Var1 == Var2 (Bool)"))
        self.addPart(intBox("Bool variable ID 1", "var1id"))
        self.addPart(intBox("Bool variable ID 2", "var2id"))
        self.addPart(output("True", "target1", "nextType1"))
        self.addPart(output("True", "target2", "nextType2"))

class varVarInvNode(node):
    def populate(self):
        self.type = "varvarinv"
        self.addPart(text("Var1 == Var2 (Invetory)"))
        self.addPart(intBox("Slot ID 1", "var1id"))
        self.addPart(intBox("Slot ID 2", "var2id"))
        self.addPart(output("True", "target1", "nextType1"))
        self.addPart(output("True", "target2", "nextType2"))

class varValStrNode(node):
    def populate(self):
        self.addPart(text("Var == Value (Str)"))
        self.addPart(intBox("Str variable ID", "var"))
        self.addPart(textBox("Value", "value"))
        self.addPart(output("True", "target1", "nextType1"))
        self.addPart(output("True", "target2", "nextType2"))

class varValIntNode(node):
    def populate(self):
        self.type = "varvalint"
        self.addPart(text("Var == Value (Int)"))
        self.addPart(intBox("Int variable ID", "var"))
        self.addPart(intBox("Value", "value"))
        self.addPart(output("True", "target1", "nextType1"))
        self.addPart(output("True", "target2", "nextType2"))

class varValFloatNode(node):
    def populate(self):
        self.type = "varvalflt"
        self.addPart(text("Var == Value (Float)"))
        self.addPart(intBox("Float variable ID", "var"))
        self.addPart(floatBox("Value", "value"))
        self.addPart(output("True", "target1", "nextType1"))
        self.addPart(output("True", "target2", "nextType2"))

class varValBoolNode(node):
    def populate(self):
        self.type = "varvalbol"
        self.addPart(text("Var == Value (Bool)"))
        self.addPart(intBox("Bool variable ID", "var"))
        self.addPart(boolBox("Value", "value"))
        self.addPart(output("True", "target1", "nextType1"))
        self.addPart(output("True", "target2", "nextType2"))

class varValInvNode(node):
    def populate(self):
        self.type = "varvalinv"
        self.addPart(text("Var == Value (Inventory)"))
        self.addPart(intBox("Slot ID", "var"))
        self.addPart(textBox("Item", "value"))
        self.addPart(output("True", "target1", "nextType1"))
        self.addPart(output("True", "target2", "nextType2"))

class dayNode(node):
    def populate(self):
        self.type = "day"
        self.addPart(text("Day cutscene"))
        self.addPart(textBox("Title", "title"))
        self.addPart(textBox("Subtitle", "subtitle"))
        self.addPart(intBox("Day number", "dayNumber"))
        self.addPart(textBox("Weather", "weather"))
        self.addPart(output("Target", "targetDefault"))

class sceneNode(node):
    def populate(self):
        self.type = "scene"
        self.addPart(text("Scene transition"))
        self.addPart(textBox("Scene", "scene"))
        self.addPart(textList("Characters", "characters"))
        self.addPart(boolList("Sides", "sides"))
        self.addPart(output("Target", "targetDefault"))

class musicNode(node):
    def populate(self):
        self.type = "music"
        self.addPart(text("Music transition"))
        self.addPart(floatBox("Fade out", "fadeout"))
        self.addPart(floatBox("Fade in", "fadein"))
        self.addPart(textBox("Track", "track"))
        self.addPart(output("Target", "targetDefault"))

class chapterNode(node):
    def populate(self):
        self.type = "chapter"
        self.addPart(text("Go to chapter"))
        self.addPart(textBox("Chapter", "chapter"))