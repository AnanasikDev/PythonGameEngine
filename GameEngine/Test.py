import pygame
from GameEngine.GameManager import *
import GameEngine.ColorLib as colors

init()
screen = Screen(1000, 300, color=colors.BLACK)
cam = Camera(screen)

ball = GameObject(Renderer(r"C:\GitArchive\Archive\Code\Successful projects\Python\Snake\Apple0.png", colors.WHITE),
                          Transform(Vector(200, 180), rotation=0, size=Vector(20, 20)))
ball.rigidbody = Rigidbody(ball, 0.05)
ball.rigidbody.collider = Collider(ball)


b = GameObject(Renderer(r"C:\GitArchive\Archive\Code\Successful projects\Python\Snake\Apple1.png", colors.WHITE),
                          Transform(Vector(100, 500), rotation=0, size=Vector(100, 20)))
b.rigidbody = Rigidbody(b, 0.05, mode=STATIC)
b.rigidbody.collider = Collider(b)

b = GameObject(Renderer(r"C:\GitArchive\Archive\Code\Successful projects\Python\Snake\Apple1.png", colors.WHITE),
                          Transform(Vector(500, 200), rotation=0, size=Vector(20, 100)))
b.rigidbody = Rigidbody(b, 0.05, mode=STATIC)
b.rigidbody.collider = Collider(b)
ball.rigidbody.AddForce(Vector(1, 0), 0)

ball.rigidbody.AddForce(Vector(1, 1), 2.5)
@run
def run():
    pass

run()