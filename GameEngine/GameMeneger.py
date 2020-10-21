import pygame
import sys
import time
from functools import wraps

pygame.init()

def Clamp(n, minValue, maxValue):
    if (n < minValue):
        n = minValue
    if (n > maxValue):
        n = maxValue

    return n
def Quit():
    pygame.quit()
    sys.exit()
def SetFPS(fps):
    clock = pygame.time.Clock()
    clock.tick(fps)
def Time(count=1000):
    def inner(function):
        #@wraps
        def get(*args, **kwargs):
            t = 0
            for i in range(count):
                t1 = time.time()
                function(*args, **kwargs)
                t2 = time.time()
                t += (t2-t1)
            return t
        return get
    return inner

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPos(self):
        return (self.x, self.y)
class Transform:
    def __init__(self, position, rotation, size):
        self.position = position
        self.x = position.x
        self.y = position.y
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.rotation = rotation

class Screen:
    def __init__(self, width, height, background=None, color=[255,255,255], title="Default Name", icon=None, resizeable=False):
        """
        width, height - scale
        color - background
        title - window title
        icon - path
        resizeable - resizeable
        """
        self.width = width
        self.height = height
        self.color = color
        self.back = background
        if (background != None) : self.back = pygame.image.load(str(background))
        self.title = title
        self.icon = None
        if (icon != None) : self.icon = pygame.image.load(icon)
        self.resizeable = resizeable
        self.screen = self.createScreen()

    def createScreen(self):
        sc = pygame.display.set_mode([self.width, self.height], (lambda resize: pygame.RESIZABLE if resize else False)(self.resizeable))
        sc.fill(self.color)
        pygame.display.set_caption(self.title)
        if (self.icon != None):
            pygame.display.set_icon(self.icon)
        pygame.display.flip()
        return sc

    def getInfo(self):
        return {"size" : (self.width, self.height),
                "color" : self.color,
                "icon" : self.icon,
                "title" : self.title,
                "resizeable" : self.resizeable}

    def setTitle(self, newTitle):
        pygame.display.set_caption(str(newTitle))

    def setIcon(self, newIcon):
        pygame.display.set_icon(pygame.image.load(str(newIcon)))

    def rescale(self, newWidth, newHeight):
        self.width = newWidth
        self.height = newHeight
        return self.createScreen()

    def drawBackGround(self):
        if self.back != None:
            self.blit(self.back, [0, 0])
        else:
            self.fill()

    def blit(self, obj, position):
        self.screen.blit(obj.image, position)

    def fill(self, color=None):
        if color == None : color = self.color
        self.screen.fill(color)

    def flip(self):
        pygame.display.flip()

class Camera:
    def __init__(self, screen):
        self.objects_on_scene = []
        self.screen = screen

    def draw(self, gameobj):
        if (
                (gameobj.x + gameobj.width >= 0 or gameobj.x >= 0) and
                (gameobj.y + gameobj.height >= 0 or gameobj.y >= 0)
        ):
            gameobj.draw()

    def drawAll(self):
        self.screen.drawBackGround()
        for gameobj in self.objects_on_scene:
            self.draw(gameobj)
        self.screen.flip()

    def drawSome(self, objects):
        self.screen.drawBackGround()
        for gameobj in objects:
            self.draw(gameobj)
        self.screen.flip()

class GameObject:
    def __init__(self, transform, image_path, camera, phisical_obj=None):

        self.transform = transform
        self.x = transform.x
        self.y = transform.y
        self.position = transform.position

        self.width = transform.width
        self.height = transform.height
        self.size = transform.size

        self.img_path = str(image_path)
        self.image = pygame.image.load(self.img_path)
        self.camera = camera
        self.phisical_obj = phisical_obj

        self.camera.objects_on_scene.append(self)

    def draw(self):
        self.camera.screen.blit(self, [self.x, self.y])

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Phisics:
    def __init__(self, gameobj, weight, collider=None):
        self.weight = weight
        self.obj = gameobj
        self.downVelocity = 0
        self.fallVelocity = 9.81
        self.g = 0.2
        self.collider = collider

        self.forceG = 0.04
        self.force = 0

        self.__i = 0

    def usePhisics(self):
        self.downVelocity += self.fallVelocity
        self.obj.y += (self.weight * (self.fallVelocity + self.downVelocity) * self.g)

    def addForce(self, vector, force, mode="Linear"):
        self.force = force
        self.__i += 1
        def Force(curforce):
            if mode == 'Linear':
                self.obj.x += curforce * (lambda x: 1 if x > 0 else (-1 if x < 0 else 0))(vector.x)
                self.obj.y += curforce * (lambda y: 1 if y > 0 else (-1 if y < 0 else 0))(vector.y)
            elif mode == 'Force':
                self.obj.x += curforce * (lambda x: 1 if x > 0 else (-1 if x < 0 else 0))(vector.x)
                self.obj.y += curforce * (lambda y: 1 if y > 0 else (-1 if y < 0 else 0))(vector.y)
                curforce -= self.forceG
                if (curforce <= 0):
                    curforce = 0

        self.force -= self.forceG * self.__i
        self.force = Clamp(self.force, 0, 999)
        #print(self.force)
        return Force(self.force)

class Collider:
    def __init__(self, object, size=None, position=None):
        self.transform = object.transform
        self.size = self.transform.size
        if (size != None):
            self.transform.size = size
        self.position = self.transform.position
        if (position != None):
            self.transform.position = position

        self.points = self.addSquareCollider()

    def addSquareCollider(self):
        p = []
        x = self.transform.position.x
        y = self.transform.position.y
        w = self.transform.size[0]
        h = self.transform.size[1]
        p.append((x, y))
        p.append((x + w, y))
        p.append((x, y + h))
        p.append((x + w, y + h))
        return p

    def overLapped(self, other):
        """
        other is collider
        """
        for Otherpoint in other.points:
            for Selfpoint in self.points:
                if Otherpoint in self.points:
                    return True
                else:
                    if (Otherpoint.transform.x >= Selfpoint.transform.x and Otherpoint.transform.x + self.size[0] <= Selfpoint.transform.x) or \
                       (Otherpoint[0] + self.size[0], Otherpoint[0] + self.size[1]) in self.points or \
                       (Otherpoint[0] + self.size[0]) in self.points:
                        return True
        return False