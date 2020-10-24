import pygame
import sys
from time import sleep, time
from functools import wraps
import GameEngine.GameEngine.ColorLib as colors

pygame.init()
clock = pygame.time.Clock()
FPS = 60
TICK = 0
PREFABS = []

def Tick(fps=FPS):
    clock.tick(fps)
def Clamp(n, minValue, maxValue):
    if (n < minValue):
        n = minValue
    if (n > maxValue):
        n = maxValue
    return n
def Quit():
    pygame.quit()
    sys.exit()
def Time(function):
    @wraps
    def get(*args, **kwargs):
        t = 0
        for i in range(2500):
            t1 = time()
            function(*args, **kwargs)
            t2 = time()
            t += (t2-t1)
        return t / 2500
    return get
def Instantiate():
    pass
def Coroutuine(ticks):
    global TICK
    TICK += 1
    if TICK >= ticks:
        TICK = 0
        print("!!!")
        return True

class Renderer:
    def __init__(self, img_path, alpha_color=None):
        self.path = img_path
        self.image = pygame.image.load(self.path)
        self.alpha_color = alpha_color
        if (self.alpha_color != None):
            self.image.set_colorkey(self.alpha_color)

    def setAlpha(self, alpha=None):
        if alpha == None:
            alpha = self.alpha_color
        self.image.set_colorkey(alpha)

    def draw(self):
        pass
    def fill(self):
        pass

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPos(self):
        return (self.x, self.y)

    def __str__(self):
        return str(self.getPos())
class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def getSize(self):
        return (self.width, self.height)
class Transform:
    def __init__(self, position, rotation, size):
        self.position = position
        self.size = size
        self.rotation = rotation # x

class Screen:
    def __init__(self, width, height, background=None, color=colors.WHITE, title="Default Name", icon=None, resizeable=False):
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
        gameobj._PrepForFrame()
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
    def __init__(self, renderer, transform, camera, phisical_obj=None):

        self.transform = transform
        self.x = transform.position.x
        self.y = transform.position.y
        self.position = transform.position

        self.width = transform.size.width
        self.height = transform.size.height
        self.size = transform.size
        self.renderer = renderer

        self.image = self.renderer.image.convert()
        self.__img = self.image

        self.__rotate()
        if (self.transform.size != (1,1)):
            self.Scale(transform.size.width, transform.size.height)

        self.camera = camera
        self.phisical_obj = phisical_obj

        self.camera.objects_on_scene.append(self)

    def __rotate(self):
        self.image = pygame.transform.rotate(self.__img, self.transform.rotation)
        self.__img = self.image
        self.renderer.setAlpha()

    def __scale(self):
        self.image = pygame.transform.scale(self.image, (self.transform.size.width, self.transform.size.height))
        self.__img = self.image
        self.renderer.setAlpha()

    def Rotate(self, angle):
        self.transform.rotation += angle
        self.image = pygame.transform.rotate(self.__img, self.transform.rotation)
        self.renderer.setAlpha()

    def Scale(self, width, height):
        self.transform.size.width += width
        self.transform.size.height += height
        self.image = pygame.transform.scale(self.__img, (self.transform.size.width, self.transform.size.height))
        self.renderer.setAlpha()

    def draw(self):
        self.camera.screen.blit(self, [self.x, self.y])

    def _PrepForFrame(self):
        if self.phisical_obj != None:
            self.phisical_obj.AddForce(self.phisical_obj._v, self.phisical_obj._f, self.phisical_obj._m)
            self.phisical_obj.Gravity()

    def move(self, x=0, y=0):
        self.x += x
        self.y += y
        self.transform.position.x = self.x
        self.transform.position.y = self.y

    def moveAt(self, x, y):
        self.transform.position = Position(x, y)

    def MoveTo(self, x, y):
        pass

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

KINEMATIC = -1
STATIC = 0

class Phisics:
    def __init__(self, gameobj, weight, mode = KINEMATIC, collider=None):
        self.obj = gameobj
        self.weight = weight
        self.obj = gameobj
        self.downVelocity = 0
        self.fallVelocity = 9.81
        self.g = 0.2
        self.collider = collider
        self.mass_center = Position(self.obj.transform.size.width / 2, self.obj.transform.size.height / 2)

        self.mode = mode

        self.velocity = Vector(0, 0)

        self.forceG = 0.04
        self.force = 0

        self.__i = 0
        self._breaked = False

        self._f = 0
        self._m = ""
        self._v = Vector(0, 0)

    def Break(self):
        self.velocity = Vector(0, 0)
        self.downVelocity = 0

    def StopPhisics(self):
        self.Break()
        self._breaked = True

    def StartPhisics(self):
        self._breaked = False

    def Gravity(self):
        if not self._breaked and self.mode == KINEMATIC:
            self.downVelocity += self.fallVelocity
            vel = (self.weight * (self.fallVelocity + self.downVelocity) * self.g)
            self.obj.move( 0,  vel )
            self.velocity.y += vel
            #print("vel = ", self.velocity)
        #print("Now is", self.obj.transform.position)

    def AddForce(self, vector, force, mode="Force"):
        self._f = force
        self._v = vector
        self._m = mode
        return self._addForce(vector, force, mode)

    def _addForce(self, vector, force, mode="Force"):
        self.force = force
        self.__i += 1

        addforcecore = (lambda curforce, n : curforce * (lambda n: 1 if n > 0 else (-1 if n < 0 else 0))(n)) # if not self._breaked else 0
        def Force(curforce):
            if mode == 'Linear':
                self.obj.move( addforcecore(curforce ,vector.x) )
                self.obj.move( 0, addforcecore(curforce, vector.y) )
            elif mode == 'Force':
                self.obj.move( addforcecore(curforce, vector.x) )
                self.obj.move(0, addforcecore(curforce, vector.y) )
                curforce -= self.forceG
                # if (curforce <= 0):
                #     curforce = 0
                curforce = (curforce ** 2) ** 0.5

        self.force -= self.forceG * self.__i
        self.force = Clamp(self.force, 0, 999)
        #print(self.force)
        self.velocity.x += addforcecore(self.force, vector.x)
        self.velocity.y += addforcecore(self.force, vector.y)
        #print("vel = ", self.velocity)
        return Force(self.force)

COLLIDERS = []
class Collider:
    def __init__(self, object, size=None, position=None):
        self.object = object
        self.transform = object.transform
        self.size = self.transform.size
        if (size != None):
            self.transform.size = size
        self.position = self.transform.position
        if (position != None):
            self.transform.position = position

        self.pos = self.__getPoint()
        self.__collided = False
        COLLIDERS.append(self)
        self._other = None

        # points = {1 : (self.transform.position.x, self.transform.position.y), 2 : (self.transform.position.x + self.transform.size.width, self.transform.position.y), 3 :
        #       (self.transform.position.x, self.transform.position.y + self.transform.size.height),
        #       4 : (self.transform.position.x + self.transform.size.width, self.transform.position.y + self.transform.size.height)}
        #
        # for i in range(1, 5):
        #     pygame.draw.circle(self.object.camera.screen.screen, colors.BLUE, [points[i][0], points[i][1]], 2, 0)
        #
        # self.object.draw()
        # self.object.camera.screen.flip()
        # sleep(3)

    def __getPoint(self):
        p = self.object.transform.position
        return p

    def __overLapped(self, other):
        """
        other is collider
        """
        """ .     .
        .     .
            .     .
        .     .
        
        func(a,b)
        a.x >= b.x and a.x <= b.x1
        a.x <= b.x and a.x >= b.x1
        """
        self.pos = self.__getPoint()
        def collision():
            return (
            (self.pos.x >= other.pos.x and self.pos.x <= other.pos.x + other.size.width) or
            (self.pos.x + self.size.width >= other.pos.x and self.pos.x + self.size.width <= other.pos.x + other.size.width)) and \
                \
            ((self.pos.y >= other.pos.y and self.pos.y <= other.pos.y + other.size.height) or
            (self.pos.y + self.size.height >= other.pos.y and self.pos.y + self.size.height <= other.pos.y + other.size.height)
                    )
        if (
                collision()
        ):
            return True
        return False

    def OnCollisionEnterAt(self, collider):
        if not self.__collided:
            self.__collided = True
            r = self.__overLapped(collider)
            if not r:
                self.__collided = False
            else:
                self._other = collider
                print("--- collided")
            return r

    def __onCollisionEnter(self):
        for collider in COLLIDERS:
            if collider != self:
                if (self.OnCollisionEnterAt(collider)):
                    print("--- collided -")
                    self._other = collider
                    return True
        return False

    def OnCollisionEnter(self):
        if self.__onCollisionEnter():
            if (self.object.phisical_obj.mass_center.x < self._other.object.x or self.object.phisical_obj.mass_center.x > self._other.object.x + self._other.object.size.width and
            self.object.phisical_obj.mass_center.y < self._other.object.y):
                print("STOP!")
                #print()
                self.object.phisical_obj.StopPhisics()
                #self.object.Rotate(45)
                self._other.object.phisical_obj.StopPhisics()

    def __onCollisionExit(self):
        pass


class ParticleSystem:
    def __init__(self, prefab, quantity):
        self.count = quantity
        self.prefab = prefab

    def __createPart(self):
        pass

