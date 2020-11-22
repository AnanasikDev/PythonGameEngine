# Import libs
import pygame
import sys
from time import sleep, time
from functools import wraps
import GameEngine.ColorLib as colors
import keyboard
import platform

assert not platform.python_compiler() is None

pygame.init()
PREFABS = []

mainCamera = None
mainScreen = None

false = False
true = True

# FPS control

clock = pygame.time.Clock()

FPS = 60
delta = 0  # Time between frames
last = time()


def Tick(fps=FPS):
    clock.tick(fps)


INFINITY = "infinity"


def Clamp(n, minValue = INFINITY, maxValue = INFINITY):
    if (minValue != INFINITY and n < minValue):
        n = minValue
    if (maxValue != INFINITY and n > maxValue):
        n = maxValue
    return n


def Quit(code=0):
    """
    :param code: exit code
    Quits program
    """
    pygame.quit()
    sys.exit(code)


def Time(function):
    @wraps
    def get(*args, **kwargs):
        t = 0
        for i in range(2500):
            t1 = time()
            function(*args, **kwargs)
            t2 = time()
            t += (t2 - t1)
        return t / 2500

    return get


def Instantiate():
    pass


def Coroutuine(seconds):
    pass


class Vector:
    def __init__(self, x, y):
        '''
        Vector of moving relatively to itself position

        x - vector of moving by x axis
        y - vector of moving by y axis

        1 0 - right
        -1 0 - left
        0 1 - down
        1 0 - up
        '''
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def get(self):
        m = (lambda x : 1 if x > 1 else (-1 if x < 0 else 0))(self.x)
        n = (lambda y: 1 if y > 1 else (-1 if y < 0 else 0))(self.y)
        v = Vector(m, n)
        return v

    # @property
    # def zero(self):
    #     return Vector(0, 0)
    #
    # @zero.getter
    # def zero(self):
    #     return Vector(0, 0)

    @staticmethod
    def zero():
        return Vector(0, 0)
    #__get = (lambda n: 1 if n > 0 else (-1 if n < 0 else 0))


class Renderer:
    def __init__(self, img_path, alpha_color=None):
        self.path = img_path
        self.image = pygame.image.load(self.path)
        self.alpha_color = alpha_color
        self.size = Vector(self.image.get_width(), self.image.get_height())
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


class Transform:
    def __init__(self, position, size=None, rotation=0):
        self.position = position
        self.size = size
        self.rotation = rotation

    def Translate(self, x_offset, y_offset):
        self.position.x += x_offset * delta
        self.position.y += y_offset * delta
        return self.position

    def Rescale(self, width, height):
        self.size.x = width
        self.size.y = height
        return self.size

    def Rotate(self, angle):
        self.rotation += angle
        return self.rotation


class Screen:
    def __init__(self, width = 800, height = 800, background=None, color=colors.WHITE, title="Default Name", icon=None,
                 resizeable=False, showFps=True):

        global mainScreen

        """
        width, height - scale
        color - background image (path)
        title - window title
        icon - path of icon
        resizeable - resizeable
        
        Game window can be created with no arguments. Default size is 800x800
        """
        self.width = width
        self.height = height
        self.color = color # [r, g, b]
        self.back = background
        if (background != None): self.back = pygame.image.load(str(background))
        self.__title = title
        self.__icon = None
        if (icon != None): self.icon = pygame.image.load(icon) 
        self.resizeable = resizeable
        self.showFps = showFps

        self.screen = self.createScreen()

        mainScreen = self

    def createScreen(self):
        sc = pygame.display.set_mode([self.width, self.height],
                                     (lambda resize: pygame.RESIZABLE if resize else False)(self.resizeable))
        sc.fill(self.color)
        pygame.display.set_caption(self.__title)
        if (self.__icon != None):
            pygame.display.set_icon(self.icon)
        pygame.display.flip()
        return sc

    def getInfo(self):
        return {"size": (self.width, self.height),
                "color": self.color,
                "icon": self.icon,
                "title": self.title,
                "resizeable": self.resizeable}

    def setTitle(self, newTitle):
        self.__title = str(newTitle)
        pygame.display.set_caption(str(newTitle))

    def setIcon(self, newIcon):
        self.__icon = newIcon
        pygame.display.set_icon(pygame.image.load(str(newIcon)))

    def rescale(self, newWidth, newHeight):
        self.width = newWidth
        self.height = newHeight
        return self.createScreen()

    def drawBackGround(self):
        if (type(self.back) == GameObject):
            self.draw(self.back)
        elif (type(self.back) == str):
            self.blit(self.back, [0, 0])
        else:
            self.fill()

    def draw(self, obj, position):
        """
        Draws gameobject on screen
        """
        self.screen.blit(obj.image, position)

    def blit(self, image, position):
        """
        Draws image on screen
        image - is path of image
        """
        self.screen.blit(image, position)

    def fill(self, color=None):
        """
        Fills whole window by color
        """
        if color == None: color = self.color
        self.screen.fill(color)

    def flip(self):
        pygame.display.flip()

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, newTitle):
        self.setTitle(newTitle)

    @title.getter
    def title(self):
        return self.__title

    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, newIcon):
        self.setIcon(newIcon)

    @icon.getter
    def icon(self):
        return self.__icon


class Camera:
    def __init__(self, screen):
        global mainCamera

        self.objects_on_scene = []
        self.screen = screen
        mainCamera = self

    def draw(self, gameobj):
        gameobj._PrepForFrame()
        if (
                (gameobj.transform.position.x + gameobj.transform.size.x >= 0 or gameobj.transform.position.x >= 0) and
                (gameobj.transform.position.y + gameobj.transform.size.y >= 0 or gameobj.transform.position.y >= 0)
        ):
            gameobj.draw()

    def drawAll(self):
        """
        Draws all gameobjects that can be seen.
        """
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
    def __init__(self, renderer, transform, rigidbody=None):

        self.transform = transform

        self.renderer = renderer

        if self.transform.size is None:
            self.transform.size = self.renderer.size

        self.image = self.renderer.image.convert()
        self.__img = self.image
        self.Scale(transform.size.x, transform.size.y)

        self.camera = mainCamera
        self.rigidbody = rigidbody

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
        self.transform.size.x += width
        self.transform.size.y += height
        self.image = pygame.transform.scale(self.__img, (self.transform.size.x, self.transform.size.y))
        self.renderer.setAlpha()

    def draw(self):
        self.camera.screen.draw(self, [self.transform.position.x, self.transform.position.y])

    def _PrepForFrame(self):
        if self.rigidbody != None:
            self.rigidbody._addForce()
            self.rigidbody.Gravity()

    def move(self, x=0, y=0):
        # self.transform.position.x += x * delta
        # self.transform.position.y += y * delta
        self.transform.position += Vector(x * delta, y * delta)

    def moveAt(self, x, y):
        self.transform.position = Vector(x, y)

    def MoveTo(self, x, y):
        pass


KINEMATIC = -1
STATIC = 0


class Rigidbody:
    def __init__(self, gameobj, mass=0.05, mode=KINEMATIC, collider=None):
        """
        :param gameobj: object for attach rigidbody to
        :param mass: the mass of object (0.05 normally)
        :param mode: KINEMATIC is able to fall by gravity force; STATIC is static object, that does not use gravity
        :param collider: attached collider (optional)

        The attached rigidbody to some object gives ability to use force and gravity.
        --------
        Settings
        --------
        weight - the mass of object (0.05 normally)
        fallVelocity - fall acceleration
        downVelocity - current fall velocity by gravity force
        """
        self.obj = gameobj
        self.mass = mass
        self.obj = gameobj
        self.downVelocity = 0
        self.fallVelocity = 9.81
        self.g = 0.2
        self.collider = collider
        self.mass_center = Vector(self.obj.transform.size.x / 2, self.obj.transform.size.y / 2)

        self.mode = mode

        self.velocity = Vector(0, 0)

        self.forceG = 0.04
        self.force = 0

        self.__i = 0
        self._broken = False

        self._forces = []

    def Break(self):
        self.velocity = Vector(0, 0)
        self.downVelocity = 0

    def StopPhysics(self):
        self.Break()
        self._broken = True

    def StartPhysics(self):
        self._broken = False

    def Gravity(self):
        if not self._broken and self.mode == KINEMATIC and not self.collider.OnCollisionEnter():
            self.downVelocity += self.fallVelocity
            vel = (self.mass * (self.fallVelocity + self.downVelocity) * self.g)
            self.obj.move(0, vel)
            self.velocity.y += vel

    def AddForce(self, vector, force=1):
        self._forces.append(vector * force)
        return self._addForce()

    def _addForce(self):

        def Addforce(vector):
            self.obj.transform.Translate(vector.x, vector.y)
            vector.x *= (9/10)
            vector.y *= (9/10)

        for f in self._forces:
            Addforce(f)


COLLIDERS = []


class Collider:
    def __init__(self, object, size=None, position=None):
        """
        Detector of collisions to other colliders
        p1
        o-------o
        |       |
        |       |
        o-------o
                p4
        p1 - left-up point
        p4 - right-bottom point
        """
        self.object = object
        self.transform = object.transform

        """Size initialization"""
        self.size = self.transform.size
        if (size != None):
            self.transform.size = size

        """Position initialization"""
        self.position = self.transform.position
        if (position != None):
            self.transform.position = position

        self.pos = self.__getPoint()
        self.__collided = False
        COLLIDERS.append(self)
        self._other = None

        """Collision points initialization"""
        self.p1 = self.pos
        self.p4 = self.pos + self.size

    def getFreshData(self):
        """Updates info about collider"""
        self.pos = self.__getPoint()
        self.p1 = self.pos
        self.p4 = self.pos + self.size

    def __get_vector(self):
        r = {True: 1, False: -1}
        vector = Vector(r[self.p4.x <= self._other.p1.x], r[self.p4.y >= self._other.p1.y])
        return vector

    def __getPoint(self):
        p = self.object.transform.position
        self.pos = p
        return self.pos

    def __overLapped(self, other):
        """
        other is collider
            .     .
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
               (self.pos.x >= other.pos.x and self.pos.x <= other.pos.x + other.size.x) or
               (self.pos.x + self.size.x >= other.pos.x and self.pos.x + self.size.x <= other.pos.x + other.size.x)) and \
\
                ((self.pos.y >= other.pos.y and self.pos.y <= other.pos.y + other.size.y) or
                (self.pos.y + self.size.y >= other.pos.y and self.pos.y + self.size.y <= other.pos.y + other.size.y))

        return collision()

    def OnCollisionEnterAt(self, collider):
        if not self.__collided:
            self.__collided = True
            r = self.__overLapped(collider)
            if not r:
                self.__collided = False
            # else:
            #
            #     vector = (0, 0)
            #
            #     if self.pos.y + self.transform.size.height < \
            #         collider.pos.y + collider.transform.size.height and \
            #         self.pos.y + self.transform.size.height < \
            #         collider.pos.y:
            #         vector = (0, 1)
            #
            #     elif self.pos.y > \
            #         collider.pos.y + collider.transform.size.height and \
            #         self.pos.y + self.transform.size.height < \
            #         collider.pos.y + collider.transform.size:
            #         vector = (0, 1)
            #
            #         self._other = collider
            #     print("--- collided")
            return r    # overlapped, collider, vector

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
            # if (
            #         self.object.rigidbody.mass_center.x < self._other.object.x or
            #         self.object.rigidbody.mass_center.x > self._other.object.x + self._other.object.size.width and
            #         self.object.rigidbody.mass_center.y < self._other.object.y):
            #     print("STOP!")

            # print(self.pos, self.size, self._other.pos, self._other.size)
            # print((self.pos + (self.size / 2)))
            # print((self._other.pos + (self._other.size / 2)))
            # vector = (self.pos + (self.size / 2)) - (self._other.pos + (self._other.size / 2))
            # print(vector)

            vector = self.__get_vector()
            # vector = Vector(0, -1)
            print("Collided", vector)
            if vector.y == -1:
                print("STOP PHYS")
                self.object.rigidbody.StopPhysics()
                # self.object.transform.position.y = self._other.p1.y - self.object.transform.size.y - 5
                self.object.moveAt(self.object.transform.position.x, self._other.p1.y - self.object.transform.size.y)
                # self.object.move(0, -4)

            return True
        return False

    def __onCollisionExit(self):
        pass


class ParticleSystem:
    def __init__(self, prefab, quantity):
        self.count = quantity
        self.prefab = prefab

    def __createPart(self):
        pass


def init():
    if mainScreen is None:
        screen = Screen()
    if mainCamera is None:
        camera = Camera(mainScreen)


def run(update):

    def inner():
        global delta, last, mainCamera, mainScreen

        while True:

            delta = time() - last
            delta *= 60
            last = time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Quit()

            update()
            if (mainScreen.showFps): mainScreen.title = clock.get_fps()
            mainCamera.drawAll()

            clock.tick(FPS)

    return inner


class Input:

    __pressed = false
    @staticmethod
    def GetKey(key):
        if type(key) is str:
            return keyboard.is_pressed(key)
        return false

    @staticmethod
    def GetKeyDown(key):
        if type(key) is str:
            pressed = keyboard.is_pressed(key)
            if not Input.__pressed:
                if pressed:
                    Input.__pressed = true
                    return true
            if not pressed:
                Input.__pressed = False

        return false

    @staticmethod
    def GetAnyKey():

       # return keyboard.on_press()
        pass


class Text:
    def __init__(self, text, position, font_size=30,  color=colors.BLACK):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.pos = position

        self.transform = Transform(self.pos, Vector(self.font_size * len(self.text), self.font_size))
        mainCamera.objects_on_scene.append(self)

    def _PrepForFrame(self):
        pass

    def draw(self):
        """
        available fonts:
        "18177.otf"
        "19319.ttf"
        """
        font_type = pygame.font.Font("18177.otf", self.font_size)
        text = font_type.render(self.text, True, self.color)
        mainScreen.blit(text, [self.pos.x, self.pos.y])